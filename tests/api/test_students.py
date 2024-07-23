import os
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app  


os.environ["TEST"] = "ON" 


@pytest.fixture
def test_jwt_token():
    return "test"


@pytest.mark.asyncio
async def test_create_student_route(test_jwt_token):
    transport = ASGITransport(app=app)

    
    student_data = {
        "nome": "Teste Aluno",
        "idade": 10,
        "cpf": "12345678901",
        "contato": "123456789",
        "data_nascimento": "2014-01-01",
        "email": "testezin@gmail.com",
        "especial": False,
        "ano_escolar": "5º ano teste",
        "equipe": "466a233b-9c5c-48b1-8f5b-2683e0710df2",
        "responsavel": "e3dc932c-278f-411c-87e6-31d945529b17"
    }

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = {"jwt-token": test_jwt_token}
        response = await ac.post("/v1/student", json=student_data, headers=headers)

    assert response.status_code == 201  
    assert "uuid" in response.json()


@pytest.mark.asyncio
async def test_get_student_by_id_route(test_jwt_token):
    student_id = "3c406223-a9d3-4787-aa1f-d40b9d93fbc3"
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = {"jwt-token": test_jwt_token}
        response = await ac.get(f"/v1/student_by_id/{student_id}", headers=headers)

    assert response.status_code == 200 


@pytest.mark.asyncio
async def test_search_students_by_name_route(test_jwt_token):
    student_name = "Teste Aluno"
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = {"jwt-token": test_jwt_token}
        response = await ac.get(f"/v1/search_students_by_name/{student_name}", headers=headers)

    assert response.status_code == 200  


@pytest.mark.asyncio
async def test_list_all_students_route(test_jwt_token):
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = {"jwt-token": test_jwt_token}
        response = await ac.get("/v1/list_all_students/", headers=headers, params={"page": 1, "page_size": 10})

    assert response.status_code == 200 
    json_response = response.json()
    assert "students" in json_response  
    assert "total" in json_response  
    assert json_response["total"] > 0  


@pytest.mark.asyncio
async def test_update_student_route(test_jwt_token):
    student_id = "3c406223-a9d3-4787-aa1f-d40b9d93fbc3"
    update_data = {
        "nome": "Teste Aluno Atualizado",
        "idade": 11,
        "cpf": "11111111111",
        "contato": "11111111111",
        "data_nascimento": "2013-01-01",
        "email": "testezin_atualizado@gmail.com",
        "especial": True,
        "ano_escolar": "6º ano",
        "equipe": "466a233b-9c5c-48b1-8f5b-2683e0710df2",
        "situacao": "Ativo",
        "responsavel": "e3dc932c-278f-411c-87e6-31d945529b17"
    }

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = {"jwt-token": test_jwt_token}
        response = await ac.patch(f"/v1/update_student/{student_id}", json=update_data, headers=headers)

    assert response.status_code == 200 
