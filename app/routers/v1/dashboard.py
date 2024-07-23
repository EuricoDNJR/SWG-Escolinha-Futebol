import os
import dotenv
from ...dependencies import get_token_header
from ...utils.db import crud
from ...utils.helper import logging
from fastapi import (
    APIRouter,
    status,
    Header,
    Depends,
    Query
)
from pydantic import BaseModel
from fastapi.responses import JSONResponse

dotenv.load_dotenv()

TEST = os.getenv("TEST")

router = APIRouter()

@router.get('/payments_receivable_month/', dependencies=[Depends(get_token_header)])
def payments_receivable_month(jwt_token: str = Header(...)):
    """
    Get all pending receivable payments in month.
    """
    try:
        payments = crud.get_payments_receivable_in_a_month()
        return JSONResponse(status_code=status.HTTP_200_OK, content={"total": payments})
    except Exception as e:
        logging.error(f"Error getting payments: {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Internal server error."})
    
@router.get('/payments_receivable_overdue/', dependencies=[Depends(get_token_header)])
def payments_receivable_overdue(jwt_token: str = Header(...)):
    """
    Get all receivable payments overdue.
    """
    try:
        payments = crud.get_payments_receivable_overdue()
        return JSONResponse(status_code=status.HTTP_200_OK, content={"total": payments})
    except Exception as e:
        logging.error(f"Error getting payments: {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Internal server error."})
    
@router.get('/payments_received_month/', dependencies=[Depends(get_token_header)])
def payments_received_month(jwt_token: str = Header(...)):
    """
    Get all payments received in month.
    """
    try:
        payments = crud.get_payments_received_in_a_month()
        return JSONResponse(status_code=status.HTTP_200_OK, content={"total": payments})
    except Exception as e:
        logging.error(f"Error getting payments: {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Internal server error."})
    
@router.get('/students_per_team/', dependencies=[Depends(get_token_header)])
def students_per_team(jwt_token: str = Header(...)):
    """
    Get all students per team.
    """
    try:
        students = crud.get_students_per_team()
        if not students:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No students found."})
        return JSONResponse(status_code=status.HTTP_200_OK, content=students)
    except Exception as e:
        logging.error(f"Error getting students: {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Internal server error."})

@router.get('/students_active_inactive/', dependencies=[Depends(get_token_header)])
def students_active_inactive(jwt_token: str = Header(...)):
    """
    Get all students active and inactive.
    """
    try:
        students = crud.get_students_active_inactive()
        if not students:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No students found."})
        return JSONResponse(status_code=status.HTTP_200_OK, content=students)
    except Exception as e:
        logging.error(f"Error getting students: {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Internal server error."})