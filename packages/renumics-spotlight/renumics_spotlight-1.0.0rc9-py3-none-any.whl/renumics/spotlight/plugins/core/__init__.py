"""
    Spotlight core plugin
    Provides core datatypes and sources.
"""

from fastapi import FastAPI
from .api import (
    table as table_api,
    user as user_api,
    filebrowser as file_api,
    config as config_api,
    layout as layout_api,
)


__version__ = "0.0.1"
__priority__ = 0


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
    app.include_router(layout_api.router, prefix="/api/layout")
    app.include_router(table_api.router, prefix="/api/table")
    app.include_router(file_api.router, prefix="/api/browse")
    app.include_router(user_api.router, prefix="/api/user")
    app.include_router(config_api.router, prefix="/api/config")
