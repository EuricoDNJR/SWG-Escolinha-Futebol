import os
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


os.environ["TEST"] = "ON" 

@pytest.fixture
def test_jwt_token():
    return "test"

@pytest.mark.asyncio
async def test_signup_route(test_jwt_token):
    transport = ASGITransport(app=app)

    
    user_data = {
        "email": "example@example.com",
        "password": "password123",
        "cargo": "Professor",
        "nome": "Testador"
    }

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        
        headers = {"jwt-token": test_jwt_token}
        response = await ac.post("/v1/signup/", json=user_data, headers=headers)
        print(response.text)
    assert response.status_code == 201 

@pytest.mark.asyncio
async def test_login_route():
    transport = ASGITransport(app=app)

    
    user_data = {
        "email": "joaocesar@gmail.com",
        "password": "bombadorato1"
    }

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/v1/login/", json=user_data)

    assert response.status_code == 200  
    assert "token" in response.json() 

@pytest.mark.asyncio
async def test_get_all_users_route(test_jwt_token):
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/v1/all_users/", headers={"jwt-token": test_jwt_token})

    assert response.status_code == 200  


@pytest.mark.asyncio
async def test_get_all_teachers_route(test_jwt_token):
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/v1/all_teachers/", headers={"jwt-token": test_jwt_token})

    assert response.status_code == 200  


@pytest.mark.asyncio
async def test_get_user_by_id_route(test_jwt_token):
    user_id = "a8ae4464-fd9d-4d68-a815-41e8e613b10b"
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(f"/v1/user_by_id/{user_id}", headers={"jwt-token": test_jwt_token})

    assert response.status_code == 200  


@pytest.mark.asyncio
async def test_update_user_route(test_jwt_token):
    user_id = "a8ae4464-fd9d-4d68-a815-41e8e613b10b"
    update_data = {
        "email": "updated_email@example.com",
        "cargo": "updated_cargo",
        "nome": "updated_name"
    }

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.patch(f"/v1/update_user/{user_id}", json=update_data, headers={"jwt-token": test_jwt_token})

    assert response.status_code == 200  
    assert "firebaseId" in response.json()  



