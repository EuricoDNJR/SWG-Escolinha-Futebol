import os
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app  


os.environ["TEST"] = "ON" 


@pytest.fixture
def test_jwt_token():
    return "test"


@pytest.mark.asyncio
async def test_create_responsible_route(test_jwt_token):
    transport = ASGITransport(app=app)

    responsible_data = {
        "nome": "Tester",
        "cpf": "00000000000",
        "contato": "00000000000",
        "data_nascimento": "1999-01-01",
        "email": "testeempresadef@gmail.com",
        "endereco": "Rua 1, 123"
    }

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = {"jwt-token": test_jwt_token}
        response = await ac.post("/v1/responsible/", json=responsible_data, headers=headers)

    assert response.status_code == 201  

@pytest.mark.asyncio
async def test_get_responsible_by_id_route(test_jwt_token):
    responsible_id = "e3dc932c-278f-411c-87e6-31d945529b17"
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = {"jwt-token": test_jwt_token}
        response = await ac.get(f"/v1/responsible_by_id/{responsible_id}", headers=headers)

    assert response.status_code == 200  


@pytest.mark.asyncio
async def test_get_all_responsible_route(test_jwt_token):
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = {"jwt-token": test_jwt_token}
        response = await ac.get("/v1/all_responsible/", headers=headers)

    assert response.status_code == 200  

@pytest.mark.asyncio
async def test_update_responsible_route(test_jwt_token):
    responsible_id = "e3dc932c-278f-411c-87e6-31d945529b17"
    update_data = {
        "nome": "Tester Atualizado",
        "cpf": "11111111111",
        "contato": "1111111111",
        "data_nascimento": "1999-01-02",
        "email": "testeempresadef@gmail.com",
        "endereco": "Rua 123, 321"
    }

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = {"jwt-token": test_jwt_token}
        response = await ac.patch(f"/v1/update_responsible/{responsible_id}", json=update_data, headers=headers)

    assert response.status_code == 200
