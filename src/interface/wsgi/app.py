import logging

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from src import PROJECT_ENVS
from src.constants import Envs
from src.interface.wsgi.middlewares.setup import setup_middleware
from src.interface.wsgi.routes.probes import probes_route
from src.interface.wsgi.routes.user import user_route
from src.interface.wsgi.setup import setup_datadog

# from fastapi_pagination import add_pagination as setup_pagination


logger = logging.getLogger(__name__)
setup_datadog()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.cache = {}
    logger.info("App ready")
    yield


def build_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        docs_url=None if PROJECT_ENVS.ENV_STATE == Envs.PROD.value else "/docs",
        redoc_url=None if PROJECT_ENVS.ENV_STATE == Envs.PROD.value else "/redoc",
    )

    # Apps
    # setup_sphinx_doc(app)
    setup_middleware(app)
    # routes
    routes = [
        probes_route,
        user_route,
    ]
    for route in routes:
        app.include_router(route)
    # setup_pagination(app)

    return app


app = build_app()
