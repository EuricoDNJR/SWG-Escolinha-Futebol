import os
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


os.environ["TEST"] = "ON"


@pytest.fixture
def test_jwt_token():
    return "test"


@pytest.mark.asyncio
async def test_add_installments_route(test_jwt_token):
    transport = ASGITransport(app=app)

    payment_data = {
        "valor": 0.00,
        "aluno": "3c406223-a9d3-4787-aa1f-d40b9d93fbc3",
        "quant_parcelas": 1
    }

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = {"jwt-token": test_jwt_token}
        response = await ac.post("/v1/add_installments/", json=payment_data, headers=headers)

    assert response.status_code == 200 
    assert "message" in response.json() 


@pytest.mark.asyncio
async def test_list_payments_by_id_route(test_jwt_token):
    student_id = "3c406223-a9d3-4787-aa1f-d40b9d93fbc3"
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = {"jwt-token": test_jwt_token}
        response = await ac.get(f"/v1/list_by_id/{student_id}", headers=headers)

    assert response.status_code == 200
    assert response.json() 


@pytest.mark.asyncio
async def test_list_all_payments_route(test_jwt_token):
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = {"jwt-token": test_jwt_token}
        response = await ac.get("/v1/list_all/", headers=headers, params={"page": 1, "page_size": 10})

    assert response.status_code == 200 
    json_response = response.json()
    assert "payments" in json_response 
    assert "total" in json_response 
    assert json_response["total"] > 0
