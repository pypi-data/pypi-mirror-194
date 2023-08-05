"""
start flask development server
"""

import asyncio
import re
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger
from renumics.spotlight.backend.exceptions import Problem

from renumics.spotlight.licensing import spotlight_license
from renumics.spotlight.layout.nodes import Layout
from renumics.spotlight.plugin_loader import load_plugins
from renumics.spotlight.licensing.verification import LicensedFeature
from renumics.spotlight.backend.data_source import DataSource
from renumics.spotlight.typing import PathType
from renumics.spotlight.settings import settings

from .apis import websocket

from .tasks.task_manager import TaskManager
from .middlewares.timing import add_timing_middleware
from .config import Config
from .websockets import WebsocketManager


class SpotlightApp(FastAPI):
    """
    Custom FastAPI Application class
    Provides typing support for our custom app attributes
    """

    # pylint: disable=too-many-instance-attributes

    spotlight_license: LicensedFeature
    data_source: Optional[DataSource]
    task_manager: TaskManager
    websocket_manager: WebsocketManager
    layout: Optional[Layout]
    config: Config
    project_root: PathType


def create_app() -> SpotlightApp:
    """
    create app
    """

    app = SpotlightApp()

    app.spotlight_license = spotlight_license
    app.data_source = None
    app.task_manager = TaskManager()
    app.config = Config()
    app.layout = None
    app.project_root = Path.cwd()

    # setup websocket route
    app.include_router(websocket.router, prefix="/api")

    @app.exception_handler(Exception)
    async def _(_: Request, e: Exception) -> JSONResponse:
        if settings.dev:
            logger.exception(e)
        else:
            logger.info(e)
        class_name = type(e).__name__
        title = re.sub(r"([a-z])([A-Z])", r"\1 \2", class_name)
        return JSONResponse(
            {"title": title, "detail": str(e), "type": class_name},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @app.exception_handler(Problem)
    async def _(_: Request, problem: Problem) -> JSONResponse:
        if settings.dev:
            logger.exception(problem)
        else:
            logger.info(problem)
        return JSONResponse(
            {
                "title": problem.title,
                "detail": problem.detail,
                "type": type(problem).__name__,
            },
            status_code=problem.status_code,
        )

    plugins = load_plugins()
    for plugin in plugins.values():
        if hasattr(plugin, "on_startup"):
            plugin.on_startup(app)

    @app.on_event("startup")
    def _() -> None:
        loop = asyncio.get_running_loop()
        app.websocket_manager = WebsocketManager(loop)

    @app.on_event("shutdown")
    def _() -> None:
        app.task_manager.shutdown()

    try:
        app.mount(
            "/",
            StaticFiles(packages=["renumics.spotlight.backend"], html=True),
        )
    except AssertionError:
        logger.warning("Frontend folder does not exist. No frontend will be served.")

    if settings.dev:
        logger.info("Running in dev mode")
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        add_timing_middleware(app)

    return app
