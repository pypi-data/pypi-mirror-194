"""
    Spotlight core plugin
    Provides core datatypes and sources.
"""

from fastapi import FastAPI
from .api.table import router

__version__ = "0.0.1"
__priority__ = 100


def __activate__() -> None:
    """
    register data sources
    """
    # pylint: disable=import-outside-toplevel, unused-import
    from . import pandas_data_source, hdf5_data_source


def on_startup(app: FastAPI) -> None:
    """
    register api routes on app startup
    """
    app.include_router(router, prefix="/api/table")
