import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src import PROJECT_ENVS
from src.interface.wsgi.auth.dependencies import Authenticator
from src.interface.wsgi.setup import get_db
from src.repository.deal import DealRepository
from src.schema.deal import DealSchema

deal_route = APIRouter(
    prefix="/deal",
    tags=["deal"],
    responses={404: {"description": "Not Found"}},
    dependencies=[Depends(Authenticator())],
)

# Set up logger
logger = logging.getLogger(__name__)


@deal_route.get(
    "/{deal_id}",
    response_model=DealSchema,
    response_description="Retrieve a deal by ID",
)
def get(deal_id: str, db: Session = Depends(get_db)):
    try:
        deal = DealRepository(db).read(_id=deal_id)
        if not deal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deal not found")
        return deal
    except Exception as e:
        logger.error(f"Error retrieving deal with ID {deal_id}: {e}", exc_info=PROJECT_ENVS.DEBUG)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@deal_route.post("/", response_model=DealSchema, response_description="Create a new deal")
def post(model: DealSchema, db: Session = Depends(get_db)):
    try:
        return DealRepository(db).upsert(data=model)
    except Exception as e:
        logger.error(f"Error creating deal: {e}", exc_info=PROJECT_ENVS.DEBUG)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@deal_route.delete("/{deal_id}", response_description="Delete a deal by ID")
def delete(deal_id: str, db: Session = Depends(get_db)):
    try:
        result = DealRepository(db).delete(_id=deal_id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deal not found")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"detail": "Deal deleted successfully"},
        )
    except Exception as e:
        logger.error(f"Error deleting deal with ID {deal_id}: {e}", exc_info=PROJECT_ENVS.DEBUG)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@deal_route.patch("/", response_model=DealSchema, response_description="Update an existing deal")
def patch(model: DealSchema, db: Session = Depends(get_db)):
    try:
        updated_deal = DealRepository(db).update(_id=model.id, data=model)
        if not updated_deal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deal not found")
        return updated_deal
    except Exception as e:
        logger.error(f"Error updating deal with ID {model.id}: {e}", exc_info=PROJECT_ENVS.DEBUG)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
