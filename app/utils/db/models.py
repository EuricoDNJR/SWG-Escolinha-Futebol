import uuid


from peewee import DateTimeField, TextField

from app.utils.db.database import BaseModel



class User(BaseModel):
    id = TextField(primary_key=True, default=uuid.uuid4)
    firebaseId = TextField(unique=True, column_name="firebaseId")
    createdAt = DateTimeField(column_name="createdAt")

    class Meta:
        table_name = "User"