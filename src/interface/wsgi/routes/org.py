import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src import PROJECT_ENVS
from src.interface.wsgi.auth.dependencies import Authenticator
from src.interface.wsgi.setup import get_db
from src.repository.org import OrgRepository
from src.schema.org import OrgSchema

org_route = APIRouter(
    prefix="/org",
    tags=["org"],
    responses={404: {"description": "Not Found"}},
    dependencies=[Depends(Authenticator())],
)

# Set up logger
logger = logging.getLogger(__name__)


@org_route.get("/{org_id}", response_model=OrgSchema, response_description="Retrieve a org by ID")
def get(org_id: str, db: Session = Depends(get_db)):
    try:
        org = OrgRepository(db).read(_id=org_id)
        if not org:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Org not found")
        return org
    except Exception as e:
        logger.error(f"Error retrieving org with ID {org_id}: {e}", exc_info=PROJECT_ENVS.DEBUG)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@org_route.post("/", response_model=OrgSchema, response_description="Create a new org")
def post(model: OrgSchema, db: Session = Depends(get_db)):
    try:
        return OrgRepository(db).upsert(data=model)
    except Exception as e:
        logger.error(f"Error creating org: {e}", exc_info=PROJECT_ENVS.DEBUG)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@org_route.delete("/{org_id}", response_description="Delete a org by ID")
def delete(org_id: str, db: Session = Depends(get_db)):
    try:
        result = OrgRepository(db).delete(_id=org_id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Org not found")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"detail": "Org deleted successfully"},
        )
    except Exception as e:
        logger.error(f"Error deleting org with ID {org_id}: {e}", exc_info=PROJECT_ENVS.DEBUG)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@org_route.patch("/", response_model=OrgSchema, response_description="Update an existing org")
def patch(model: OrgSchema, db: Session = Depends(get_db)):
    try:
        updated_org = OrgRepository(db).update(_id=model.id, data=model)
        if not updated_org:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Org not found")
        return updated_org
    except Exception as e:
        logger.error(f"Error updating org with ID {model.id}: {e}", exc_info=PROJECT_ENVS.DEBUG)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
