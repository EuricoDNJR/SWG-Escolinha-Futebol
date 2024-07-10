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
    Depends,
    Query
)

dotenv.load_dotenv()

TEST = os.getenv("TEST")

router = APIRouter()

from pydantic import BaseModel

class SignUpStudentSchema(BaseModel):
    nome:str
    idade:int
    cpf:str
    contato: Optional[str]
    data_nascimento:str
    email: Optional[str]
    especial: Optional[bool] = False
    equipe: str
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
            responsavel = student_data.responsavel
        )

        logging.info("Student created successfully")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"uuid": str(student.id), "message": "Aluno criado com sucesso"})
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Erro ao criar o aluno: " + str(e)})
    
@router.get('/student_by_id/{id}', dependencies=[Depends(get_token_header)])
async def get_student_by_id(id:str, jwt_token:str = Header(...)):
    """
    Get student by id.
    """
    try:
        logging.info("Getting student by id: " + id)

        student = crud.get_student_by_id(id)
        if student is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Aluno não encontrado"})

        logging.info("Student found successfully")
        return JSONResponse(status_code=status.HTTP_200_OK, content={"student": student})
    except Exception as e:
        logging.error(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Erro ao buscar o aluno: " + str(e)})
    
@router.get('/list_all_students/', dependencies=[Depends(get_token_header)])
async def list_all_students(page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    jwt_token: str = Header(...)):
    """
    List all students with pagination.
    """
    try:
        logging.info("Listing all students by user: " + jwt_token)

        offset = (page - 1) * page_size
        students = crud.get_all_students_with_pagination(offset, page_size)
        total_students = crud.count_all_students()

        if not students:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Nenhum aluno foi encontrado"})

        logging.info("Students listed successfully")
        return {
            "total": total_students,
            "page": page,
            "page_size": page_size,
            "students": students
        }
    except Exception as e:
        logging.error(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Erro ao listar todos os alunos: " + str(e)})

class UpdateStudentSchema(BaseModel):
    nome:Optional[str] = None
    idade:Optional[int] = None
    cpf:Optional[str] = None
    contato:Optional[str] = None
    data_nascimento:Optional[str] = None
    email: Optional[str] = None
    especial: Optional[bool] = False
    equipe: Optional[str] = None
    situacao: Optional[str] = None
    responsavel: Optional[str] = None
@router.patch('/update_student/{id}', dependencies=[Depends(get_token_header)])
async def update_student(id:str, student_data: UpdateStudentSchema, jwt_token:str = Header(...)):
    """
    Update student by id.
    E.g:

        {
            "nome": "João Filho",
            "idade": 10,
            "cpf": "12345678901",
            "contato": "123456789",
            "data_nascimento": "1999-01-01",
            "email": "exemplo@gmail.com",
            "especial": false,
            "equipe": "02bcca12-6f62-4671-84bb-141ee3a67e9d",
            "situacao": "Ativo",
            "responsavel": "24ac5412-af03-4ea0-9fb4-643ed93c9b8d"
        }

    """
    
    try:
        logging.info("Updating student by user: " + jwt_token)

        student = crud.update_student(
            id = id,
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

        if student is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Erro ao atualizar o aluno!"})

        logging.info("Student updated successfully")
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Aluno atualizado com sucesso"})
    except Exception as e:
        logging.error(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Erro ao atualizar o aluno: " + str(e)})