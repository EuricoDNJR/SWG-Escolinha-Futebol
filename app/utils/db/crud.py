from datetime import date, timedelta
import uuid
from typing import List
from peewee import fn
from . import models
from ...utils.helper import logging


def create_user(firebaseId: str, firebaseIdWhoCreated: str, email: str, cargo: str):
    return models.User.create(firebaseId=firebaseId, firebaseIdWhoCreated=firebaseIdWhoCreated, email=email, cargo=cargo)

def create_responsible(nome: str, cpf: str, contato: str, data_nascimento: str, email: str):
    return models.Responsible.create(nome=nome, cpf=cpf, contato=contato, data_nascimento=data_nascimento, email=email)

def create_team(nome: str, idade_minima: int, idade_maxima: int, professor: str, horario_inicio: str, horario_fim: str, dias_semana: str):
    return models.Team.create(nome=nome, idade_minima=idade_minima, idade_maxima=idade_maxima, professor=professor, horario_inicio=horario_inicio, horario_fim=horario_fim, dias_semana=dias_semana)

def create_student(nome: str, idade: int, cpf: str, contato: str, data_nascimento: str, email: str, especial: bool, time: str, situacao: str, responsavel: str):
    return models.Student.create(nome=nome, idade=idade, cpf=cpf, contato=contato, data_nascimento=data_nascimento, email=email, especial=especial, time=time, situacao=situacao, responsavel=responsavel)

def generate_payments(valor: float, aluno: str):
    try:
        hoje = date.today()
        proximo_vencimento = hoje

        for i in range(1,13):
            proximo_vencimento += timedelta(days=30)
            models.Payment.create(
                id=uuid.uuid4(),
                valor=valor,  # Defina o valor adequado aqui
                data_pagamento=None,
                data_vencimento=proximo_vencimento,
                status="Pendente",  # Defina o status inicial adequado aqui
                comprovante=None,
                aluno=aluno,
                parcela=i
            )
        return True
    except Exception as e:
        logging.error("Error generating payments: " + str(e))
        return None

def get_all_responsibles():
    responsibles = models.Responsible.select()

    if responsibles.exists():
        return [
            {
                "id": str(responsible.id),
                "nome": responsible.nome,
                "cpf": responsible.cpf,
                "contato": responsible.contato,
                "data_nascimento": str(responsible.data_nascimento),
                "email": responsible.email if responsible.email is not None else None
            }
            for responsible in responsibles
        ]
    else:
        return None
    
def get_all_teams():
    teams = models.Team.select()

    if teams.exists():
        return [
            {
                "id": str(team.id),
                "nome": team.nome,
                "idade_minima": team.idade_minima,
                "idade_maxima": team.idade_maxima,
                "professor": team.professor.id,
                "horario_inicio": team.horario_inicio,
                "horario_fim": team.horario_fim,
                "dias_semana": team.dias_semana
            }
            for team in teams
        ]
    else:
        return None
    
def get_all_payments_by_student(aluno: str):
    try:
        payments = models.Payment.select().where(models.Payment.aluno == aluno)

        if payments.exists():
            return [
                {
                    "id": str(payment.id),
                    "valor": payment.valor,
                    "data_pagamento": str(payment.data_pagamento) if payment.data_pagamento is not None else None,
                    "data_vencimento": str(payment.data_vencimento),
                    "status": payment.status,
                    "comprovante": payment.comprovante if payment.comprovante is not None else None,
                    "parcela": payment.parcela,
                    "aluno": payment.aluno.id
                }
                for payment in payments
            ]
        else:
            return None
    except Exception as e:
        logging.error("Error getting payments: " + str(e))
        return None
    
def get_all_payments_with_pagination(offset: int, limit: int) -> List[dict]:
    try:
        payments = models.Payment.select().offset(offset).limit(limit)
        return [
            {
                "id": str(payment.id),
                "valor": payment.valor,
                "data_pagamento": str(payment.data_pagamento) if payment.data_pagamento is not None else None,
                "data_vencimento": str(payment.data_vencimento),
                "status": payment.status,
                "comprovante": payment.comprovante if payment.comprovante is not None else None,
                "parcela": payment.parcela,
                "aluno": payment.aluno.id
            }
            for payment in payments
        ]
    except Exception as e:
        logging.error("Error getting payments with pagination: " + str(e))
        return []

def count_all_payments() -> int:
    try:
        return models.Payment.select().count()
    except Exception as e:
        logging.error("Error counting payments: " + str(e))
        return 0

def find_first_payment_not_paid(student_id: str):
    try:
        return models.Payment.select().where(models.Payment.aluno == student_id, models.Payment.status == "Pendente").order_by(models.Payment.data_vencimento).first()
    except Exception as e:
        logging.error("Error finding first payment not paid: " + str(e))
        return None
    
def update_payment_status(pagamento_id: str, comprovante_id: str):
    try:
        hoje = date.today()
        payment = models.Payment.get(models.Payment.id == pagamento_id)
        payment.data_pagamento = hoje
        payment.status = "Pago"
        payment.comprovante = comprovante_id
        payment.save()
        return True
    except Exception as e:
        logging.error("Error updating payment status: " + str(e))
        return None
    
def get_payment_by_id(pagamento_id: str):
    try:
        payment = models.Payment.get(models.Payment.id == pagamento_id)
        return {
            "id": str(payment.id),
            "valor": payment.valor,
            "data_pagamento": str(payment.data_pagamento) if payment.data_pagamento is not None else None,
            "data_vencimento": str(payment.data_vencimento),
            "status": payment.status,
            "comprovante": payment.comprovante if payment.comprovante is not None else None,
            "parcela": payment.parcela,
            "aluno": payment.aluno.id
        }
    except Exception as e:
        logging.error("Error getting payment by id: " + str(e))
        return None