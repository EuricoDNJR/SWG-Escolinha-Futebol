import os
import time
import dotenv
from peewee import Model, PostgresqlDatabase
from psycopg2 import OperationalError

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


def reconnect_db(func):
    def wrapper(*args, **kwargs):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if db.is_closed():
                    db.connect()
                return func(*args, **kwargs)
            except OperationalError as e:
                if "SSL connection has been closed unexpectedly" in str(e):
                    print("Connection closed unexpectedly. Reconnecting...")
                    if not db.is_closed():
                        db.close()
                    time.sleep(2**attempt)
                    db.connect()
                else:
                    raise
        raise Exception("Max retries reached")

    return wrapper
