import os
import dotenv
from typing import Optional
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from ...dependencies import get_token_header
from ...utils.db import crud
from ...utils.helper import logging
from fastapi import (
    APIRouter,
    status,
    Header,
    Depends
)

dotenv.load_dotenv()

TEST = os.getenv("TEST")

router = APIRouter()

from pydantic import BaseModel

class SignUpResponsibleSchema(BaseModel):
    nome:str
    cpf:str
    contato:str
    data_nascimento:str
    email: Optional[str]


@router.post('/responsible', dependencies=[Depends(get_token_header)])
async def create_responsible_account(responsible_data:SignUpResponsibleSchema, jwt_token:str = Header(...)):
    """
    Create an account for the responsible.
    E.g:

        {
            "nome": "João",
            "cpf": "12345678901",
            "contato": "123456789",
            "data_nascimento": "1999-01-01",
            "email": "jose123@gmail.com"
        }
    
    """

    try: 
        logging.info("Creating responsible by user: " + jwt_token)

        responsible = crud.create_responsible(
            nome = responsible_data.nome,
            cpf = responsible_data.cpf,
            contato = responsible_data.contato,
            data_nascimento = responsible_data.data_nascimento,
            email = responsible_data.email
        )

        logging.info("Responsible created successfully")

        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"uuid": str(responsible.id), "message": "Responsible created successfully"})
    
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Erro ao criar o responsavel: " + str(e)})