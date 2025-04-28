import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src import PROJECT_ENVS
from src.interface.wsgi.auth.dependencies import Authenticator
from src.interface.wsgi.setup import get_db
from src.repository.user import UserRepository
from src.schema.user import UserSchema

user_route = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not Found"}},
    dependencies=[Depends(Authenticator())],
)

# Set up logger
logger = logging.getLogger(__name__)


@user_route.get("/", response_model=UserSchema, response_description="Retrieve a user by ID")
def get(user_id: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        user = UserRepository(db).read(_id=user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    except Exception as e:
        logger.error(f"Error retrieving user with ID {user_id}: {e}", exc_info=PROJECT_ENVS.DEBUG)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@user_route.post("/", response_model=UserSchema, response_description="Create a new user")
def post(model: UserSchema, db: Session = Depends(get_db)):
    try:
        return UserRepository(db).upsert(data=model)
    except Exception as e:
        logger.error(f"Error creating user: {e}", exc_info=PROJECT_ENVS.DEBUG)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@user_route.delete("/{user_id}", response_description="Delete a user by ID")
def delete(user_id: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        result = UserRepository(db).delete(_id=user_id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"detail": "User deleted successfully"},
        )
    except Exception as e:
        logger.error(f"Error deleting user with ID {user_id}: {e}", exc_info=PROJECT_ENVS.DEBUG)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@user_route.patch("/", response_model=UserSchema, response_description="Update an existing user")
def patch(model: UserSchema, db: Session = Depends(get_db)):
    try:
        updated_user = UserRepository(db).update(_id=model.id, data=model)
        if not updated_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return updated_user
    except Exception as e:
        logger.error(f"Error updating user with ID {model.id}: {e}", exc_info=PROJECT_ENVS.DEBUG)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
