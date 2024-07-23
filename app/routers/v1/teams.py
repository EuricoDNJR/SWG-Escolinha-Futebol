import os
import dotenv
from typing import Optional
from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)

@router.post('/team/', dependencies=[Depends(get_token_header)])
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

@router.get('/team_by_id/{id}', dependencies=[Depends(get_token_header)])
async def get_team_by_id(id:str, jwt_token:str = Header(...)):
    """
    Get a Team by id.
    """

    try:
        logging.info("Getting team by user: " + jwt_token)

        team = crud.get_team_by_id(id)

        if team is not None:
            logging.info("Team found successfully")
            return JSONResponse(status_code=status.HTTP_200_OK, content=team)
        else:
            logging.info("Team not found")
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Turma não encontrada"})
    
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Erro ao buscar a turma: " + str(e)})
    
@router.get('/all_teams/', dependencies=[Depends(get_token_header)])
async def get_all_teams(jwt_token:str = Header(...)):
    """
    Get all teams.
    """

    try:
        logging.info("Getting all teams by user: " + jwt_token)

        teams = crud.get_all_teams()

        if teams is not None:
            logging.info("Teams found successfully")
            return JSONResponse(status_code=status.HTTP_200_OK, content=teams)
        else:
            logging.info("No teams found")
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Nenhuma turma encontrada"})
    
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Erro ao buscar as turmas: " + str(e)})

class UpdateTeamSchema(BaseModel):
    nome:Optional[str] = None
    idade_minima:Optional[int] = None
    idade_maxima:Optional[int] = None
    professor:Optional[str] = None
    horario_inicio:Optional[str] = None
    horario_fim:Optional[str] = None
    dias_semana:Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

@router.patch('/update_team/{id}', dependencies=[Depends(get_token_header)])
async def update_team(id:str, team_data:UpdateTeamSchema, jwt_token:str = Header(...)):
    """
    Update a Team.
    E.g:

        {
            "nome": "Grupo 1",
            "idade_minima": 10,
            "idade_maxima": 15,
            "professor": "f796a1b5-e07c-4a39-9d94-a39c31154538",
            "horario_inicio": "14:00",
            "horario_fim": "16:00",
            "dias_semana": "Segunda, Terça, Quarta"
        }

    """

    try:
        logging.info("Updating team by user: " + jwt_token)

        team = crud.update_team(
            id = id,
            nome = team_data.nome,
            idade_minima = team_data.idade_minima,
            idade_maxima = team_data.idade_maxima,
            professor = team_data.professor,
            horario_inicio = team_data.horario_inicio,
            horario_fim = team_data.horario_fim,
            dias_semana = team_data.dias_semana
        )

        if team is not None:
            logging.info("Team updated successfully")
            return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Turma atualizada com sucesso"})
        else:
            logging.info("Team not found")
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Turma não encontrada"})
    
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Erro ao atualizar a turma: " + str(e)})