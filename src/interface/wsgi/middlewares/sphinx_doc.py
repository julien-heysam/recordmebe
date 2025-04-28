import importlib.util
import logging
import os
import shlex
import subprocess

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src import PROJECT_PATHS


def setup_sphinx_doc(app: FastAPI) -> None:
    if os.path.exists(PROJECT_PATHS.SPHINX_PATH):
        app.mount(
            "/sphinx",
            StaticFiles(directory=PROJECT_PATHS.SPHINX_PATH, html=True),
            name="sphinx",
        )
    elif importlib.util.find_spec("sphinx"):
        subprocess.run(shlex.split("make build_doc"))
        app.mount(
            "/sphinx",
            StaticFiles(directory=PROJECT_PATHS.SPHINX_PATH, html=True),
            name="sphinx",
        )
    else:
        logging.warning("Can't build/display the sphinx documentation")
