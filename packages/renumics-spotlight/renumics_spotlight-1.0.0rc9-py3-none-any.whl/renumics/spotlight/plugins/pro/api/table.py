"""
Additional API Endpoints for editing
"""

from datetime import datetime
from typing import Any, List, Optional
from fastapi import APIRouter, Request
from pydantic import BaseModel  # pylint: disable=no-name-in-module

from renumics.spotlight.backend.data_source import DataSource, sanitize_values
from renumics.spotlight.licensing.verification import LicensedFeature

from renumics.spotlight.plugins.core.api.table import Column


# pylint: disable=too-few-public-methods
router = APIRouter()


class MutationResponse(BaseModel):
    """
    Common response model for all mutational endpoints.
    """

    generation_id: int


class Cells(BaseModel):
    """
    Multiple Cells with the same value
    """

    column: str
    rows: List[int]
    value: Any


class CellsUpdateResponse(Cells):
    """
    A cell update (cell + edit information)
    """

    author: str
    edited_at: Optional[datetime]
    generation_id: int


class CellsUpdateRequest(BaseModel):
    """
    Table Cell update request model
    """

    rows: List[int]
    value: Any


class AddColumnRequest(BaseModel):
    """
    Add Column request model
    """

    dtype: str


class AddColumnResponse(MutationResponse):
    """
    Add column response model.
    """

    column: Column


class DuplicateRowResponse(MutationResponse):
    """
    Duplicate row response model.
    """

    row: int


@router.put(
    "/{column}",
    response_model=CellsUpdateResponse,
    tags=["table"],
    operation_id="put_cells",
)
async def put_table_cells(
    column: str,
    generation_id: int,
    update_request: CellsUpdateRequest,
    request: Request,
) -> CellsUpdateResponse:
    """
    replace multiple cell's data

    :raises NoColumnFound: if the column was not found in the dataset
    :raises NoRowFound: if one of the rows was not found in the dataset
    """
    table: DataSource = request.app.data_source
    table.check_generation_id(generation_id)

    cells_update = table.replace_cells(
        column, update_request.rows, update_request.value
    )

    return CellsUpdateResponse(
        column=column,
        rows=update_request.rows,
        value=sanitize_values(cells_update.value),
        author=sanitize_values(cells_update.author),
        edited_at=sanitize_values(cells_update.edited_at),
        generation_id=table.get_generation_id(),
    )


@router.post(
    "/{column}",
    response_model=AddColumnResponse,
    tags=["table"],
    operation_id="add_column",
)
async def add_column(
    column: str,
    generation_id: int,
    add_column_request: AddColumnRequest,
    request: Request,
) -> AddColumnResponse:
    """
    add an editable column

    :raises ColumnExistsError: if a column with the same name exists in the dataset
    """
    table: DataSource = request.app.data_source
    table.check_generation_id(generation_id)

    new_column = table.append_column(column, add_column_request.dtype)

    spotlight_license: LicensedFeature = request.app.spotlight_license

    if (
        spotlight_license.row_limit is not None
        and len(table) > spotlight_license.row_limit
    ):
        new_column.values = new_column.values[: spotlight_license.row_limit]
        if new_column.references is not None:
            new_column.references = new_column.references[: spotlight_license.row_limit]

    return AddColumnResponse(
        generation_id=table.get_generation_id(),
        column=Column.from_dataset_column(new_column),
    )


@router.delete(
    "/rows/{row}",
    response_model=MutationResponse,
    tags=["table"],
    operation_id="delete_row",
)
async def delete_row(
    row: int, generation_id: int, request: Request
) -> MutationResponse:
    """
    remove a row from the datasets

    :raises NoRowFound: if a row is not found
    """
    table: DataSource = request.app.data_source
    table.check_generation_id(generation_id)

    table.delete_row(row)

    return MutationResponse(generation_id=table.get_generation_id())


@router.post(
    "/rows/{row}",
    response_model=DuplicateRowResponse,
    tags=["table"],
    operation_id="create_row",
)
async def insert_row(
    row: int, generation_id: int, request: Request
) -> DuplicateRowResponse:
    """
    create a new row in the dataset by duplicating a given row

    :raises NoRowFound: if a row is not found
    """
    table: DataSource = request.app.data_source
    table.check_generation_id(generation_id)

    row_index = table.duplicate_row(row)

    return DuplicateRowResponse(generation_id=table.get_generation_id(), row=row_index)


@router.delete(
    "/{column}",
    response_model=MutationResponse,
    tags=["table"],
    operation_id="delete_column",
)
async def delete_column(
    column: str, generation_id: int, request: Request
) -> MutationResponse:
    """
    remove a column from the datasets

    :raises NoColumnFound: if a column with the name does not exist
    """
    table: DataSource = request.app.data_source
    table.check_generation_id(generation_id)

    table.delete_column(column)

    return MutationResponse(generation_id=table.get_generation_id())
