import logging

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

probes_route = APIRouter(
    tags=["probes"],
    responses={404: {"description": "Not found"}},
)
logger = logging.getLogger(__name__)


@probes_route.get("/healthcheck", response_description="Health check")
def get():
    """
    Health check endpoint.
    - Returns `200 OK` if the service is up and running.
    """
    return JSONResponse(content={"status": "OK"}, status_code=status.HTTP_200_OK)


@probes_route.get("/startup", response_description="Startup probe")
def get_startup(request: Request):
    """
    Startup probe to check if the application has started.
    - Returns `200 OK` if startup is complete.
    - Returns `503 Service Unavailable` if startup is incomplete.
    """
    try:
        _ = request.app.state  # Accessing app state to check if it's initialized
        return JSONResponse(content={"status": "OK"}, status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.warning(f"Startup incomplete: {e}")
        return JSONResponse(content={"status": "Service Unavailable"}, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


@probes_route.get("/readiness", response_description="Readiness probe")
def get_readiness(request: Request):
    """
    Readiness probe to check if the application is ready to serve requests.
    - Returns `200 OK` if the application is ready.
    - Returns `425 Too Early` if the application is not ready.
    - Returns `503 Service Unavailable` if an error occurs.
    """
    try:
        if request.app.state:
            return JSONResponse(content={"status": "Ready"}, status_code=status.HTTP_200_OK)
        else:
            logger.warning("App is not ready")
            return JSONResponse(content={"status": "Too Early"}, status_code=status.HTTP_425_TOO_EARLY)
    except Exception as e:
        logger.warning(f"Readiness check failed: {e}")
        return JSONResponse(content={"status": "Service Unavailable"}, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
