import os
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app  


os.environ["TEST"] = "ON"  


@pytest.fixture
def test_jwt_token():
    return "test"


@pytest.mark.asyncio
async def test_create_team_route(test_jwt_token):
    transport = ASGITransport(app=app)

    
    team_data = {
        "nome": "Grupo Teste",
        "idade_minima": 10,
        "idade_maxima": 15,
        "professor": "a8ae4464-fd9d-4d68-a815-41e8e613b10b",
        "horario_inicio": "14:00",
        "horario_fim": "16:00",
        "dias_semana": "Segunda, Terça, Quarta"
    }

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = {"jwt-token": test_jwt_token}
        response = await ac.post("/v1/team/", json=team_data, headers=headers)

    assert response.status_code == 201  

@pytest.mark.asyncio
async def test_get_team_by_id_route(test_jwt_token):
    team_id = "a08cef4f-82ac-40b9-82e6-ca997392f4da"
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = {"jwt-token": test_jwt_token}
        response = await ac.get(f"/v1/team_by_id/{team_id}", headers=headers)

    assert response.status_code == 200  


@pytest.mark.asyncio
async def test_get_all_teams_route(test_jwt_token):
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = {"jwt-token": test_jwt_token}
        response = await ac.get("/v1/all_teams/", headers=headers)

    assert response.status_code == 200 


@pytest.mark.asyncio
async def test_update_team_route(test_jwt_token):
    team_id = "a08cef4f-82ac-40b9-82e6-ca997392f4da"
    update_data = {
        "nome": "Grupo 1 Atualizado",
        "idade_minima": 12,
        "idade_maxima": 17,
        "professor": "a8ae4464-fd9d-4d68-a815-41e8e613b10b",
        "horario_inicio": "15:00",
        "horario_fim": "17:00",
        "dias_semana": "Segunda, Quarta, Sexta"
    }

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = {"jwt-token": test_jwt_token}
        response = await ac.patch(f"/v1/update_team/{team_id}", json=update_data, headers=headers)

    assert response.status_code == 200  
