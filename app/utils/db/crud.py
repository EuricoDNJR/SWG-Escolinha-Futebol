from . import models

def create_user(firebaseId: str, firebaseIdWhoCreated: str, email: str, cargo: str):
    return models.User.create(firebaseId=firebaseId, firebaseIdWhoCreated=firebaseIdWhoCreated, email=email, cargo=cargo)

def create_responsible(nome: str, cpf: str, contato: str, data_nascimento: str, email: str):
    return models.Responsible.create(nome=nome, cpf=cpf, contato=contato, data_nascimento=data_nascimento, email=email)

def create_team(nome: str, idade_minima: int, idade_maxima: int, professor: str, horario_inicio: str, horario_fim: str, dias_semana: str):
    return models.Team.create(nome=nome, idade_minima=idade_minima, idade_maxima=idade_maxima, professor=professor, horario_inicio=horario_inicio, horario_fim=horario_fim, dias_semana=dias_semana)

def create_student(nome: str, idade: int, cpf: str, contato: str, data_nascimento: str, email: str, especial: bool, time: str, situacao: str, responsavel: str):
    return models.Student.create(nome=nome, idade=idade, cpf=cpf, contato=contato, data_nascimento=data_nascimento, email=email, especial=especial, time=time, situacao=situacao, responsavel=responsavel)