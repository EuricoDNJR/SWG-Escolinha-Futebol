import os
import dotenv
from typing import List, Optional
from pydantic import BaseModel
from fastapi.responses import JSONResponse, StreamingResponse
from ...dependencies import get_token_header
from ...utils.db import crud
from ...utils.helper import logging
from fastapi import (
    APIRouter,
    status,
    Header,
    Depends,
    Query,
    File,
    UploadFile
)
from ...utils.google_drive import upload_file, download_file

dotenv.load_dotenv()

TEST = os.getenv("TEST")

router = APIRouter()

class GeneratePaymentSchema(BaseModel):
    valor: float
    aluno: str

class PaymentOut(BaseModel):
    id: str
    valor: float
    data_pagamento: Optional[str]
    data_vencimento: str
    status: str
    comprovante: Optional[str]
    parcela: int
    aluno: str

    class Config:
        from_attributes = True

class PaginatedPayments(BaseModel):
    total: int
    page: int
    page_size: int
    payments: List[PaymentOut]

@router.post('/payment_generate/', dependencies=[Depends(get_token_header)])
def payment_generate(payment_data: GeneratePaymentSchema, jwt_token: str = Header(...)):
    """
    Generate a payment for a student.
    E.g:
        
        {
            "valor": 100.00,
            "aluno": "uuid"
        }

    """
    try:
        logging.info("Generating payment by user: " + jwt_token)

        payment = crud.generate_payments(
            valor=payment_data.valor,
            aluno=payment_data.aluno
        )
        if payment is None:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Error generating payment"})

        logging.info("Payment generated successfully")
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Parcelas geradas com sucesso!"})
    except Exception as e:
        logging.error("Error generating payment: " + str(e))
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Error generating payment: " + str(e)})

@router.get('/list_by_id/{id}', dependencies=[Depends(get_token_header)])
def list_by_id(id:str, jwt_token:str = Header(...)):
    """
    List all payments by student id.
    """

    try:
        logging.info("Listing payments by user: " + jwt_token)

        payments = crud.get_all_payments_by_student(id)
        if payments is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Payments not found"})
        
        logging.info("Payments listed successfully")
        return JSONResponse(status_code=status.HTTP_200_OK, content=payments)
    except Exception as e:
        logging.error("Error listing payments: " + str(e))
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Error listing payments" + str(e)})

@router.get('/list_all/', response_model=PaginatedPayments, dependencies=[Depends(get_token_header)])
def list_all_payments(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    jwt_token: str = Header(...)
):
    """
    List all payments with pagination.
    """
    try:
        logging.info("Listing all payments by user: " + jwt_token)

        offset = (page - 1) * page_size
        payments = crud.get_all_payments_with_pagination(offset, page_size)
        total_payments = crud.count_all_payments()

        if not payments:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Nenhum pagamento foi encontrado"})

        logging.info("Payments listed successfully")
        return {
            "total": total_payments,
            "page": page,
            "page_size": page_size,
            "payments": payments
        }
    except Exception as e:
        logging.error("Error listing all payments: " + str(e))
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Erro ao listar todos os pagamentos: " + str(e)})

@router.patch("/update_status/{id}", dependencies=[Depends(get_token_header)])
async def update_status(id: str, file: UploadFile = File(...), jwt_token: str = Header(...)):
    try:
        logging.info("File received")
        # Ensure the temp directory exists
        if not os.path.exists('temp'):
            os.makedirs('temp')

        file_location = f"temp/{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        file_id = upload_file(file_location, file.content_type)
        os.remove(file_location)

        logging.info("Finding the first payment not paid")

        payment_find = crud.find_first_payment_not_paid(student_id=id)
        if payment_find is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Nenhum pagamento foi encontrado"})
        
        logging.info("Updating payment status")
        payment = crud.update_payment_status(payment_find.id, file_id)

        if payment is None:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Error updating payment status"})
        logging.info("Payment status updated successfully")
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Status do pagamento atualizado com sucesso!"})
    except Exception as e:
        logging.error("Error at: " + str(e))
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Error listing payments: " + str(e)})

@router.get("/download_comprovante/{id}", dependencies=[Depends(get_token_header)])
async def download_comprovante(id: str, jwt_token: str = Header(...)):
    try:
        logging.info("Downloading comprovante by user: " + jwt_token)

        payment = crud.get_payment_by_id(id)
        if payment is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Payment not found"})

        logging.info("Downloading comprovante")
        file_stream = download_file(payment['comprovante'])

        return StreamingResponse(file_stream, media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={payment['comprovante']}"})
    except Exception as e:
        logging.error("Error downloading comprovante: " + str(e))
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Error downloading comprovante: " + str(e)})
#Essa rota é para baixar para a sua máquina
# @router.get("/download_comprovante/{id}", dependencies=[Depends(get_token_header)])
# def download_comprovante(id: str, jwt_token: str = Header(...)):
#     try:
#         logging.info("Downloading comprovante by user: " + jwt_token)

#         payment = crud.get_payment_by_id(id)
#         if payment is None:
#             return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Payment not found"})

#         logging.info("Downloading comprovante")
#         file_location = f"temp/{payment['comprovante']}"
#         download_file(payment['comprovante'], file_location)

#         return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Comprovante baixado com sucesso!"})
#     except Exception as e:
#         logging.error("Error downloading comprovante: " + str(e))
#         return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Error downloading comprovante: " + str(e)})