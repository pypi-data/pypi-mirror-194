"""
access pandas DataFrame table data
"""
from typing import Any, List

import numpy as np
import pandas as pd
from loguru import logger

from renumics.spotlight.dataset import get_current_datetime
from renumics.spotlight.dtypes import Category, Window
from renumics.spotlight.dtypes.typing import get_column_type
from renumics.spotlight.io.pandas import infer_dtype
from renumics.spotlight.licensing import username
from renumics.spotlight.backend.data_source import sanitize_values, CellsUpdate, Column
from renumics.spotlight.backend import datasource
from renumics.spotlight.plugins.core.pandas_data_source import PandasDataSource


@datasource(pd.DataFrame)
@datasource(".csv")
class EditablePandasDataSource(PandasDataSource):
    """
    access pandas DataFrame table data
    """

    def replace_cells(
        self, column_name: str, indices: List[int], value: Any
    ) -> CellsUpdate:
        """
        replace multiple cell's value
        """
        self._generation_id += 1
        self._assert_column_exists(column_name)
        self._assert_indices_exist(indices)

        column_index = self._df.columns.get_loc(column_name)
        old_values = self._df.iloc[indices, column_index]
        dtype = self._inferred_dtype[column_name]

        categories = None
        if dtype is Category:
            # Convert category code to category.
            categories = self._get_column_categories(column_name)
            value = next((cat for cat, i in categories.items() if i == value), np.nan)
        elif value is None:
            value = self._get_default_value(dtype)

        try:
            self._df.iloc[indices, column_index] = pd.Series([value] * len(indices))
        except Exception as e:
            self._df.iloc[indices, column_index] = old_values
            raise e

        new_value = self._df.iloc[indices[0], column_index]
        if dtype is Category:
            # Back-project category onto its code.
            new_value = -1 if categories is None else categories.get(new_value, -1)

        return CellsUpdate(
            value=sanitize_values(new_value),
            author=username,
            edited_at=get_current_datetime().isoformat(),
        )

    def delete_column(self, name: str) -> None:
        """
        remove a column from the table
        """
        self._generation_id += 1
        self._assert_column_exists(name)
        del self._df[name]
        del self._inferred_dtype[name]

    def delete_row(self, index: int) -> None:
        """
        remove a row from the table
        """
        self._generation_id += 1
        self._assert_index_exists(index)
        self._df = self._df.drop(index=self._df.index[index], axis=0)

    def duplicate_row(self, index: int) -> int:
        """
        duplicate a row in the table
        """
        self._generation_id += 1
        self._assert_index_exists(index)
        self._df = pd.concat(
            [
                self._df.iloc[:index],
                self._df.iloc[index : index + 1],
                self._df.iloc[index:],
            ]
        )
        return index + 1

    def append_column(self, name: str, dtype_name: str) -> Column:
        """
        add a column to the table
        """
        self._generation_id += 1
        self._assert_column_not_exists(name)
        dtype = get_column_type(dtype_name)

        value = self._get_default_value(dtype)
        if dtype is Window:
            self._df[name] = [value] * len(self)
            self._dtype[name] = Window
        else:
            self._df[name] = value
            inferred_dtype = infer_dtype(self._df[name])
            if inferred_dtype is not dtype:
                logger.warning(
                    f"Newly added column {name} has type {dtype}, but "
                    f"automatically inferred type would be {inferred_dtype}."
                )
        self._inferred_dtype[name] = dtype
        try:
            return self.get_column(name, None)
        except Exception as e:
            del self._df[name]
            self._dtype.pop(name, None)
            del self._inferred_dtype[name]
            raise e
