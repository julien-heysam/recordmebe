import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
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
def get(request: Request, user_id: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Retrieve a user by its ID.

    - **user_id**: ID of the user to retrieve. If not provided, defaults to the ID from request state.
    - Returns the `UserSchema` if successful.
    - **200 OK** if the user is retrieved successfully.
    - **404 Not Found** if the user with the specified ID does not exist.
    - **500 Internal Server Error** if an unexpected error occurs during retrieval.
    """
    user_id = user_id or request.state.user.id
    try:
        user = UserRepository(db).read(_id=user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    except Exception as e:
        logger.error(f"Error retrieving user with ID {user_id}: {e}", exc_info=PROJECT_ENVS.DEBUG)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@user_route.post(
    "/", response_model=UserSchema, status_code=status.HTTP_201_CREATED, response_description="Create a new user"
)
def post(request: Request, model: UserSchema, db: Session = Depends(get_db)):
    """
    Create a new user or return the existing user.

    - **model**: `UserSchema` containing the user data to create.
    - Returns the created `UserSchema`.
    - **201 Created** if the user is created successfully.
    - **500 Internal Server Error** if an unexpected error occurs during creation.
    """
    user = UserSchema(
        org_id=model.org_id or request.state.org_name,
        auth0_user_id=model.auth0_user_id or request.state.auth0_user_id,
        email=model.email or request.state.email,
        role=model.role,
    )
    try:
        user = UserRepository(db).readsert(data=user)
        return user
    except Exception as e:
        logger.error(f"Error creating user: {e}", exc_info=PROJECT_ENVS.DEBUG)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@user_route.delete("/{user_id}", response_description="Delete a user by ID")
def delete(request: Request, user_id: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Delete a user by its ID.

    - **user_id**: ID of the user to delete. If not provided, defaults to the ID from request state.
    - Returns a message indicating the result of the deletion.
    - **200 OK** if the user is deleted successfully.
    - **404 Not Found** if no user exists with the specified ID.
    - **500 Internal Server Error** if an unexpected error occurs during deletion.
    """
    user_id = user_id or request.state.user.id
    try:
        result = UserRepository(db).delete(_id=user_id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return {"detail": "User deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting user with ID {user_id}: {e}", exc_info=PROJECT_ENVS.DEBUG)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@user_route.patch("/", response_model=UserSchema, response_description="Update an existing user")
def patch(request: Request, model: UserSchema, db: Session = Depends(get_db)):
    """
    Update an existing user.

    - **model**: `UserSchema` containing updated user data.
    - Returns the updated `UserSchema`.
    - **200 OK** if the user is updated successfully.
    - **404 Not Found** if no user exists with the specified ID.
    - **500 Internal Server Error** if an unexpected error occurs during update.
    """
    user = UserSchema(
        org_id=model.org_id or request.state.token_org_name,
        auth0_user_id=model.auth0_user_id or request.state.token_owner_id,
        email=model.email or request.state.token_user_email,
    )
    try:
        updated_user = UserRepository(db).update(_id=user.id, data=user, fields=["role", "name", "meta"])
        if not updated_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return updated_user
    except Exception as e:
        logger.error(f"Error updating user with ID {user.id}: {e}", exc_info=PROJECT_ENVS.DEBUG)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
