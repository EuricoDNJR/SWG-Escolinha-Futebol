import os
import dotenv
from peewee import Model, PostgresqlDatabase

dotenv.load_dotenv()

DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASS = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")

if DATABASE_PORT:
    DATABASE_PORT = int(DATABASE_PORT)
else:
    DATABASE_PORT = 5432

db = PostgresqlDatabase(
    DATABASE_NAME,
    user=DATABASE_USER,
    password=DATABASE_PASS,
    host=DATABASE_HOST,
    port=DATABASE_PORT,
)


class BaseModel(Model):
    class Meta:
        database = db

