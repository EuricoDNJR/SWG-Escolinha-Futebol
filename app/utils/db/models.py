import uuid


from peewee import *

from app.utils.db.database import BaseModel



class User(BaseModel):
    id = TextField(primary_key=True, default=uuid.uuid4)
    firebaseId = TextField(unique=True, column_name="firebaseId", null=False)
    createdAt = DateTimeField(column_name="createdAt")
    firebaseIdWhoCreated = TextField(column_name="firebaseIdWhoCreated", null=False)
    email = TextField(column_name="email", null=False, unique=True)
    cargo = TextField(column_name="cargo", default="Professor", null=False)

    class Meta:
        table_name = "User"

class Responsible(BaseModel):
    id = TextField(primary_key=True, default=uuid.uuid4)
    nome = TextField(column_name="nome", null=False)
    cpf = TextField(column_name="cpf", null=False, unique=True)
    contato = TextField(column_name="contato", null=False)
    data_nascimento = DateField(column_name="data_nascimento", null=False)
    email = TextField(column_name="email")

    class Meta:
        table_name = "Responsible"

class Team(BaseModel):
    id = TextField(primary_key=True, default=uuid.uuid4)
    nome = TextField(column_name="nome", null=False, unique=True)
    idade_minima = IntegerField(column_name="idade_minima", null=False)
    idade_maxima = IntegerField(column_name="idade_maxima", null=False)
    professor = ForeignKeyField(User, column_name="professor", backref="groups")
    horario_inicio = TextField(column_name="horario_inicio", null=False)
    horario_fim = TextField(column_name="horario_fim", null=False)
    dias_semana = TextField(column_name="dias_semana", null=False)

    class Meta:
        table_name = "Team"

class Student(BaseModel):
    id = TextField(primary_key=True, default=uuid.uuid4)
    nome = TextField(column_name="nome", null=False)
    idade = IntegerField(column_name="idade", null=False)
    cpf = TextField(column_name="cpf", null=False, unique=True)
    contato = TextField(column_name="contato", null=False)
    data_nascimento = DateField(column_name="data_nascimento", null=False)
    email = TextField(column_name="email")
    especial = BooleanField(column_name="especial", default=False)
    time = ForeignKeyField(Team, column_name="time", backref="students")
    situacao = TextField(column_name="situacao", default="Ativo")
    responsavel = ForeignKeyField(Responsible, column_name="responsavel", backref="students")
    class Meta:
        table_name = "Student"