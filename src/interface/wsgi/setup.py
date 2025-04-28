from typing import Iterator

from datadog import initialize
from ddtrace import patch_all, tracer
from sqlalchemy.orm import Session

from src import DATABASE_URI, PROJECT_ENVS
from src.constants import Envs
from src.db.db import FastAPISessionMaker

# Automatically patch libraries for tracing
patch_all()

if PROJECT_ENVS.ENV_STATE not in [Envs.PROD.value, Envs.STAGING.value]:
    tracer.enabled = False
else:
    tracer.configure(
        hostname=PROJECT_ENVS.DD_AGENT_HOST,
        port=PROJECT_ENVS.DD_TRACE_AGENT_PORT,
        https=False,
    )


def _get_fastapi_sessionmaker() -> FastAPISessionMaker:
    return FastAPISessionMaker(DATABASE_URI)


def get_db() -> Iterator[Session]:
    yield from _get_fastapi_sessionmaker().get_db()


def setup_datadog() -> None:
    initialize(
        statsd_host=PROJECT_ENVS.DD_AGENT_HOST,
        statsd_port=PROJECT_ENVS.DD_TRACE_AGENT_PORT,
    )
