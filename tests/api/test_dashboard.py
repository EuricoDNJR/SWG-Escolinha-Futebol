import os
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app  # Certifique-se de que esta importação está correta para o seu aplicativo FastAPI

# Carrega as variáveis de ambiente para teste
os.environ["TEST"] = "ON"  # Define a variável de ambiente TEST para teste

# Função auxiliar para obter um token JWT válido para testes
@pytest.fixture
def test_jwt_token():
    return "test"

# Teste para rota de pagamentos a receber no mês
@pytest.mark.asyncio
async def test_payments_receivable_month(test_jwt_token):
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = {"jwt-token": test_jwt_token}
        response = await ac.get("/v1/payments_receivable_month/", headers=headers)

    assert response.status_code == 200  # Verifica se o código de status é 200 (OK)
    assert "total" in response.json()  # Verifica se a resposta contém o campo esperado

# Teste para rota de pagamentos a receber em atraso
@pytest.mark.asyncio
async def test_payments_receivable_overdue(test_jwt_token):
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = {"jwt-token": test_jwt_token}
        response = await ac.get("/v1/payments_receivable_overdue/", headers=headers)

    assert response.status_code == 200  # Verifica se o código de status é 200 (OK)
    assert "total" in response.json()  # Verifica se a resposta contém o campo esperado

# Teste para rota de pagamentos recebidos no mês
@pytest.mark.asyncio
async def test_payments_received_month(test_jwt_token):
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = {"jwt-token": test_jwt_token}
        response = await ac.get("/v1/payments_received_month/", headers=headers)

    assert response.status_code == 200  # Verifica se o código de status é 200 (OK)
    assert "total" in response.json()  # Verifica se a resposta contém o campo esperado

# Teste para rota de estudantes por equipe
@pytest.mark.asyncio
async def test_students_per_team(test_jwt_token):
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = {"jwt-token": test_jwt_token}
        response = await ac.get("/v1/students_per_team/", headers=headers)

    assert response.status_code == 200  # Verifica se o código de status é 200 (OK)
    assert response.json()  # Verifica se há estudantes retornados

# Teste para rota de estudantes ativos e inativos
@pytest.mark.asyncio
async def test_students_active_inactive(test_jwt_token):
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = {"jwt-token": test_jwt_token}
        response = await ac.get("/v1/students_active_inactive/", headers=headers)

    assert response.status_code == 200  # Verifica se o código de status é 200 (OK)
    assert response.json()  # Verifica se há estudantes retornados
