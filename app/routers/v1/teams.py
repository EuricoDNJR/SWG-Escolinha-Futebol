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

class SignUpTeamSchema(BaseModel):
    nome:str
    idade_minima:int
    idade_maxima:int
    professor:str
    horario_inicio:str
    horario_fim:str
    dias_semana:str


@router.post('/team', dependencies=[Depends(get_token_header)])
async def create_Team(team_data:SignUpTeamSchema, jwt_token:str = Header(...)):
    """
    Create a Team.
    E.g:

        {
            "nome": "Grupo 1",
            "idade_minima": 10,
            "idade_maxima": 15,
            "professor": "cb4819da-c310-4cd4-8132-f9a786844610",
            "horario_inicio": "14:00",
            "horario_fim": "16:00",
            "dias_semana": "Segunda, Terça, Quarta"
        }
    
    """

    try: 
        logging.info("Creating Team by user: " + jwt_token)

        Team = crud.create_team(
            nome = team_data.nome,
            idade_minima = team_data.idade_minima,
            idade_maxima = team_data.idade_maxima,
            professor = team_data.professor,
            horario_inicio = team_data.horario_inicio,
            horario_fim = team_data.horario_fim,
            dias_semana = team_data.dias_semana
        )

        logging.info("Team created successfully")

        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"uuid": str(Team.id), "message": "Turma criada com sucesso"})
    
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Erro ao criar a turma: " + str(e)})