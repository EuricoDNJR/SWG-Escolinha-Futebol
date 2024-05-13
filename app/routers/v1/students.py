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

class SignUpStudentSchema(BaseModel):
    nome:str
    idade:int
    cpf:str
    contato:str
    data_nascimento:str
    email: Optional[str]
    especial: Optional[bool] = False
    equipe: str
    situacao: Optional[str]
    responsavel: str


@router.post('/student', dependencies=[Depends(get_token_header)])
async def create_student_account(student_data:SignUpStudentSchema, jwt_token:str = Header(...)):
    """
    Create an account for the student.
    E.g:

        {
            "nome": "João Filho",
            "idade": 10,
            "cpf": "12345678901",
            "contato": "123456789",
            "data_nascimento": "1999-01-01",
            "email": "joazin@gmail.com",
            "especial": false,
            "equipe": "02bcca12-6f62-4671-84bb-141ee3a67e9d",
            "situacao": "Ativo",
            "responsavel": "24ac5412-af03-4ea0-9fb4-643ed93c9b8d"
        }

    """

    try:
        logging.info("Creating student by user: " + jwt_token)

        student = crud.create_student(
            nome = student_data.nome,
            idade = student_data.idade,
            cpf = student_data.cpf,
            contato = student_data.contato,
            data_nascimento = student_data.data_nascimento,
            email = student_data.email,
            especial = student_data.especial,
            time = student_data.equipe,
            situacao = student_data.situacao,
            responsavel = student_data.responsavel
        )

        logging.info("Student created successfully")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"uuid": str(student.id), "message": "Aluno criado com sucesso"})
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Erro ao criar o aluno: " + str(e)})