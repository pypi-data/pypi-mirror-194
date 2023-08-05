"""
access h5 table data
"""
from typing import Any, Dict, List, cast

from renumics.spotlight.dataset.exceptions import InvalidIndexError
from renumics.spotlight.dtypes import Category
from renumics.spotlight.dtypes.typing import (
    get_column_type,
)

from renumics.spotlight.backend.data_source import (
    CellsUpdate,
    Column,
)
from renumics.spotlight.backend.exceptions import (
    NoRowFound,
    ColumnNotEditable,
    InvalidCategory,
)

from renumics.spotlight.backend import datasource
from renumics.spotlight.plugins.core.hdf5_data_source import Hdf5DataSource


@datasource(".h5")
class EditableHdf5DataSource(Hdf5DataSource):
    """
    access h5 table data
    """

    def replace_cells(
        self, column_name: str, indices: List[int], value: Any
    ) -> CellsUpdate:
        """
        replace multiple cell's value
        """

        with self._open_table("r+") as dataset:
            # we can't assign an int value to a float cell in spotlight atm
            # but json numbers don't have distinct float and int types,
            # so we convert ints to float values for now
            attrs = dataset.read_attrs(column_name)
            if not attrs.editable:
                raise ColumnNotEditable(column_name)
            if value is not None:
                if attrs.type is float:
                    value = float(value)
                elif attrs.type is Category:
                    categories = cast(Dict, attrs.categories)
                    if value == -1:
                        value = None
                    else:
                        try:
                            value = list(categories.keys())[
                                list(categories.values()).index(value)
                            ]
                        except ValueError as e:
                            raise InvalidCategory() from e

            try:
                dataset[column_name, indices] = value
                new_value = dataset.read_value(column_name, indices[0])
            except IndexError as e:
                raise NoRowFound(indices[0] if len(indices) == 1 else None) from e

            edited_at = dataset.read_value("__last_edited_at__", indices[0])
            author = dataset.read_value("__last_edited_by__", indices[0])

            author = cast(str, author)
            edited_at = cast(str, edited_at)
            return CellsUpdate(value=new_value, author=author, edited_at=edited_at)

    def delete_column(self, name: str) -> None:
        """
        remove a column from the table
        """
        with self._open_table("r+") as dataset:
            del dataset[name]

    def delete_row(self, index: int) -> None:
        """
        remove a row from the table
        """

        with self._open_table("r+") as dataset:
            try:
                del dataset[index]
            except InvalidIndexError as e:
                raise NoRowFound(index) from e

    def duplicate_row(self, index: int) -> int:
        """
        duplicate a row in the table
        """

        with self._open_table("r+") as dataset:
            try:
                dataset.duplicate_row(index, index + 1)
                return index + 1
            except InvalidIndexError as e:
                raise NoRowFound(index) from e

    def append_column(self, name: str, dtype_name: str) -> Column:
        """
        add a column to the table
        """

        with self._open_table("r+") as dataset:
            dtype = get_column_type(dtype_name)
            order = dataset.min_order() - 1

            if dtype is int:
                dataset.append_column(
                    name,
                    dtype,
                    optional=True,
                    editable=True,
                    default=0,
                    order=order,
                )
            elif dtype is bool:
                dataset.append_column(
                    name,
                    dtype,
                    optional=True,
                    editable=True,
                    default=False,
                    order=order,
                )
            else:
                dataset.append_column(
                    name, dtype, optional=True, editable=True, order=order
                )

            return dataset.read_column(name)
