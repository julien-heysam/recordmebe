import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src import PROJECT_ENVS
from src.interface.wsgi.auth.dependencies import Authenticator
from src.interface.wsgi.setup import get_db
from src.schema.user import UserSchema

recorder_route = APIRouter(
    prefix="/recorder",
    tags=["recorder"],
    responses={404: {"description": "Not Found"}},
    dependencies=[Depends(Authenticator())],
)

# Set up logger
logger = logging.getLogger(__name__)


@recorder_route.get("/{org_id}/{email}", response_model=UserSchema, response_description="Retrieve recordings by org_id and email")
def get(org_id: str, email: str, db: Session = Depends(get_db)):
    try:
        records = None
        if not records:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return records
    except Exception as e:
        logger.error(f"Error retrieving user with email {email}: {e}", exc_info=PROJECT_ENVS.DEBUG)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@recorder_route.post(
    "/", response_model=UserSchema, status_code=status.HTTP_201_CREATED, response_description="Create a new recording"
)
def post(model: UserSchema, db: Session = Depends(get_db)):
    try:
        return None
    except Exception as e:
        logger.error(f"Error creating recording: {e}", exc_info=PROJECT_ENVS.DEBUG)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@recorder_route.delete("/{recording_id}", response_description="Delete a recording")
def delete(recording_id: str, db: Session = Depends(get_db)):
    try:
        result = None
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recording not found")
        return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "Recording deleted successfully"})
    except Exception as e:
        logger.error(f"Error deleting recording with ID {recording_id}: {e}", exc_info=PROJECT_ENVS.DEBUG)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@recorder_route.patch("/", response_model=UserSchema, response_description="Update an existing recording")
def patch(recording: UserSchema, db: Session = Depends(get_db)):
    try:
        updated_recording = None
        if not updated_recording:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recording not found")
        return updated_recording
    except Exception as e:
        logger.error(f"Error updating recording with ID {recording.id}: {e}", exc_info=PROJECT_ENVS.DEBUG)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
