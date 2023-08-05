"""
table api endpoints
"""
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, List

from fastapi import APIRouter, Request
from fastapi.responses import Response, ORJSONResponse
from pydantic import BaseModel  # pylint: disable=no-name-in-module

from renumics.spotlight.dtypes.typing import get_column_type_name
from renumics.spotlight.licensing import (
    LicensedFeature,
    username,
    verify_license_or_exit,
)

from renumics.spotlight.typing import PathType

from renumics.spotlight.backend import create_datasource
from renumics.spotlight.backend.exceptions import InvalidPath
from renumics.spotlight.backend.data_source import (
    Column as DatasetColumn,
    DataSource,
    sanitize_values,
    idx_column,
    last_edited_at_column,
    last_edited_by_column,
)


class Column(BaseModel):
    """
    a single table column
    """

    # pylint: disable=too-few-public-methods

    name: str
    index: Optional[int]
    hidden: bool
    editable: bool
    optional: bool
    role: str
    values: List[Any]
    references: Optional[List[bool]]
    y_label: Optional[str]
    x_label: Optional[str]
    description: Optional[str]
    tags: Optional[List[str]]
    categories: Optional[Dict[str, int]]
    embedding_length: Optional[int]

    @classmethod
    def from_dataset_column(cls, column: DatasetColumn) -> "Column":
        """
        Instantiate column from a dataset column.
        """
        return cls(
            name=column.name,
            index=column.order,
            hidden=column.hidden,
            editable=column.editable,
            optional=column.optional,
            role=get_column_type_name(column.type),
            values=sanitize_values(column.values),
            references=sanitize_values(column.references),
            x_label=column.x_label,
            y_label=column.y_label,
            description=column.description,
            tags=column.tags,
            categories=column.categories,
            embedding_length=column.embedding_length,
        )


# pylint: disable=too-few-public-methods
class Table(BaseModel):
    """
    a table slice
    """

    uid: str
    filename: str
    columns: List[Column]
    max_rows_hit: bool
    max_columns_hit: bool
    generation_id: int


router = APIRouter()


@router.get(
    "/",
    response_model=Table,
    response_class=ORJSONResponse,
    tags=["table"],
    operation_id="get_table",
)
def get_table(request: Request) -> ORJSONResponse:
    """
    table slice api endpoint
    """
    table: Optional[DataSource] = request.app.data_source
    verify_license_or_exit()
    if table is None:
        return ORJSONResponse(
            Table(
                uid="",
                filename="",
                columns=[],
                max_rows_hit=False,
                max_columns_hit=False,
                generation_id=-1,
            ).dict()
        )
    spotlight_license: LicensedFeature = request.app.spotlight_license

    columns = table.get_columns()
    max_columns_hit = False
    if spotlight_license.column_limit is not None:
        if len(columns) > spotlight_license.column_limit:
            max_columns_hit = True
            columns = columns[: spotlight_license.column_limit]

    columns.extend(table.get_internal_columns())

    max_rows_hit = False
    row_count = len(table)
    if spotlight_license.row_limit is not None:
        if len(table) > spotlight_license.row_limit:
            max_rows_hit = True
            row_count = spotlight_license.row_limit
            for column in columns:
                column.values = column.values[: spotlight_license.row_limit]
                if column.references is not None:
                    column.references = column.references[: spotlight_license.row_limit]

    columns.append(idx_column(row_count))
    if not any(column.name == "__last_edited_at__" for column in columns):
        columns.append(last_edited_at_column(row_count, datetime.now()))
    if not any(column.name == "__last_edited_by__" for column in columns):
        columns.append(last_edited_by_column(row_count, username))

    return ORJSONResponse(
        Table(
            uid=table.get_uid(),
            filename=table.get_name(),
            columns=[Column.from_dataset_column(column) for column in columns],
            max_rows_hit=max_rows_hit,
            max_columns_hit=max_columns_hit,
            generation_id=table.get_generation_id(),
        ).dict()
    )


@router.get(
    "/{column}/{row}",
    tags=["table"],
    operation_id="get_cell",
)
async def get_table_cell(
    column: str, row: int, generation_id: int, request: Request
) -> Any:
    """
    table cell api endpoint
    """
    table: DataSource = request.app.data_source
    table.check_generation_id(generation_id)

    cell_data = table.get_cell_data(column, row)
    value = sanitize_values(cell_data)

    if isinstance(value, (bytes, str)):
        return Response(value, media_type="application/octet-stream")

    return value


@router.get(
    "/{column}/{row}/waveform",
    response_model=Optional[List[float]],
    tags=["table"],
    operation_id="get_waveform",
)
async def get_waveform(
    column: str, row: int, generation_id: int, request: Request
) -> Optional[List[float]]:
    """
    table cell api endpoint
    """
    table: DataSource = request.app.data_source
    table.check_generation_id(generation_id)

    waveform = table.get_waveform(column, row)

    return sanitize_values(waveform)


class AddColumnRequest(BaseModel):
    """
    Add Column request model
    """

    dtype: str


def is_path_relative_to(path: PathType, parent: PathType) -> bool:
    """
    Is the path a subpath of the parent
    """
    try:
        Path(path).relative_to(parent)
        return True
    except ValueError:
        return False


@router.post("/open/{path:path}", tags=["table"], operation_id="open")
async def open_table(path: str, request: Request) -> None:
    """
    Open the specified table file

    :raises InvalidPath: if the supplied path is outside the project root
                         or points to an incompatible file
    """
    full_path = Path(request.app.project_root) / path

    # assert that the path is inside our project root
    if not is_path_relative_to(full_path, request.app.project_root):
        raise InvalidPath(path)

    request.app.data_source = create_datasource(full_path, dtype=None)
