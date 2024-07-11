import os
import dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from peewee import OperationalError
from contextlib import asynccontextmanager

from .utils.db.crud import update_payment_status_overdue
from .routers.v1 import teams, users, responsibles, students, payments, notifications
from .utils.helper import logging, db as database
from .utils.notification_manager import notification_manager

dotenv.load_dotenv()

ENV = os.getenv("ENV")
EMAIL_NOTIFICATIONS = os.getenv("EMAIL_NOTIFICATIONS")

api_version = "v0.1.0"
route_version = "v1"

api_metadata = {
    "title": "SWG - Escolhinha de Futebol FARP",
    "description": "API de gerenciamento da escolhinha de futebol FARP",
    "version": api_version,
}

if ENV == "dev":
    app = FastAPI(
        title=api_metadata["title"],
        description=api_metadata["description"],
        version=api_metadata["version"],
    )
else:
    app = FastAPI(
        title=api_metadata["title"],
        description=api_metadata["description"],
        version=api_metadata["version"],
        # docs_url=None,
        # redoc_url=None,
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

response_404 = {404: {"description": "Not found"}}

app.include_router(
    users.router,
    prefix=f"/{route_version}",
    tags=["users"],
    responses=response_404,
)

app.include_router(
    responsibles.router,
    prefix=f"/{route_version}",
    tags=["responsibles"],
    responses=response_404,
)

app.include_router(
    teams.router,
    prefix=f"/{route_version}",
    tags=["teams"],
    responses=response_404,
)

app.include_router(
    students.router,
    prefix=f"/{route_version}",
    tags=["students"],
    responses=response_404,
)

app.include_router(
    payments.router,
    prefix=f"/{route_version}",
    tags=["payments"],
    responses=response_404,
)

app.include_router(
    notifications.router,
    prefix=f"/{route_version}",
    tags=["notifications"],
    responses=response_404,
)

@app.get(
    "/",
    responses={
        200: {
            "description": "Root",
            "content": {"application/json": {"example": {"api-version": api_version}}},
        }
    },
)
async def root():
    logging.info("Receiving request to root")
    return {"api-version": api_version}

# Função de ping ao banco de dados
def ping_db():
    print("Iniciando ping_db...")
    try:
        if database.is_closed():
            database.connect()
        database.execute_sql('SELECT 1')
        print("Ping bem-sucedido!")
    except OperationalError as e:
        print(f"Erro ao pingar o banco de dados: {e}")
    finally:
        if not database.is_closed():
            database.close()

# Gerenciador de ciclo de vida `lifespan`
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Inicializando lifespan context...")
    scheduler = AsyncIOScheduler()
    scheduler.add_job(ping_db, "interval", seconds=60)  # Intervalo de 1 minuto
    scheduler.add_job(update_payment_status_overdue, "cron", hour=0)  # Executa diariamente à meia-noite
    scheduler.start()
    print("Scheduler iniciado...")
    
    # Inicializa o gerenciador de notificações de acordo com a variável de ambiente
    if EMAIL_NOTIFICATIONS == "ON":
        print("Iniciando gerenciador de notificações...")
        notification_manager.start()
    
    yield
    
    print("Encerrando lifespan context...")
    scheduler.shutdown()
    print("Scheduler desligado...")
    
    # Desliga o gerenciador de notificações
    notification_manager.stop()
    print("Gerenciador de notificações desligado.")
app.router.lifespan_context = lifespan
