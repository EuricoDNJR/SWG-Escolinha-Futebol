from datetime import date, timedelta, datetime
import uuid
from typing import List
from peewee import fn
from . import models
from ...utils.helper import logging


def create_user(firebaseId: str, firebaseIdWhoCreated: str, email: str, cargo: str, nome: str):
    return models.User.create(firebaseId=firebaseId, firebaseIdWhoCreated=firebaseIdWhoCreated, email=email, cargo=cargo, nome=nome)

def create_responsible(nome: str, cpf: str, contato: str, data_nascimento: str, email: str = None, endereco: str = None):
    return models.Responsible.create(nome=nome, cpf=cpf, contato=contato, data_nascimento=data_nascimento, email=email, endereco=endereco)

def create_team(nome: str, idade_minima: int, idade_maxima: int, professor: str, horario_inicio: str, horario_fim: str, dias_semana: str):
    return models.Team.create(nome=nome, idade_minima=idade_minima, idade_maxima=idade_maxima, professor=professor, horario_inicio=horario_inicio, horario_fim=horario_fim, dias_semana=dias_semana)

def create_student(nome: str, idade: int, cpf: str, data_nascimento: str, especial: bool, time: str, responsavel: str, contato: str = None, email: str = None, ano_escolar: str = None):
    return models.Student.create(nome=nome, idade=idade, cpf=cpf, contato=contato, data_nascimento=data_nascimento, email=email, especial=especial, time=time, situacao='Ativo', responsavel=responsavel, ano_escolar=ano_escolar)

def generate_payments(valor: float, aluno: str, quant_parcelas: int = 1):
    try:
        hoje = date.today()
        proximo_vencimento = hoje

        for i in range(1,quant_parcelas+1):
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

def get_last_due(student_id: str):
    try:
        return models.Payment.select().where(models.Payment.aluno == student_id).order_by(models.Payment.parcela.desc()).first()
    except Exception as e:
        logging.error("Error getting last due: " + str(e))
        return None
    
def add_installments(valor: float, aluno_id: str, quant_parcelas: int = 1):
    try:
        hoje = date.today()
        proximo_vencimento = hoje
        last_due = get_last_due(aluno_id)
        if last_due.status == "Pendente":
            proximo_vencimento = last_due.data_vencimento
        for i in range(last_due.parcela + 1, last_due.parcela + quant_parcelas + 1):
            proximo_vencimento += timedelta(days=30)
            payment = models.Payment.create(
                id=uuid.uuid4(),
                valor=valor,  # Defina o valor adequado aqui
                data_pagamento=None,
                data_vencimento=proximo_vencimento,
                status="Pendente",  # Defina o status inicial adequado aqui
                comprovante=None,
                aluno=aluno_id,
                parcela=i
            )
            payment.save()
        return True
    except Exception as e:
        logging.error("Error adding installments: " + str(e))
        return None

def get_all_users():
    users = models.User.select()

    if users.exists():
        return [
            {
                "id": str(user.id),
                "firebaseId": user.firebaseId,
                "firebaseIdWhoCreated": user.firebaseIdWhoCreated,
                "email": user.email,
                "cargo": user.cargo,
                "nome": user.nome
            }
            for user in users
        ]
    else:
        return None

def get_all_teachers():
    teachers = models.User.select().where(models.User.cargo == "Professor")

    if teachers.exists():
        return [
            {
                "id": str(teacher.id),
                "firebaseId": teacher.firebaseId,
                "firebaseIdWhoCreated": teacher.firebaseIdWhoCreated,
                "email": teacher.email,
                "cargo": teacher.cargo,
                "nome": teacher.nome
            }
            for teacher in teachers
        ]
    else:
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
                "email": responsible.email if responsible.email is not None else None,
                "endereco": responsible.endereco if responsible.endereco is not None else None
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
                "professor_id": team.professor.id,
                "professor": team.professor.nome,
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
        payments = models.Payment.select().order_by(
            models.Payment.status.desc()
        ).offset(offset).limit(limit)
        
        return [
            {
                "id": str(payment.id),
                "valor": payment.valor,
                "data_pagamento": str(payment.data_pagamento) if payment.data_pagamento is not None else None,
                "data_vencimento": str(payment.data_vencimento),
                "status": payment.status,
                "comprovante": payment.comprovante if payment.comprovante is not None else None,
                "parcela": payment.parcela,
                "aluno_id": payment.aluno.id,
                "aluno": payment.aluno.nome
            }
            for payment in payments
        ]
    except Exception as e:
        logging.error("Error getting payments with pagination: " + str(e))
        return []

def get_all_students_with_pagination(offset: int, limit: int) -> List[dict]:
    try:
        students = models.Student.select().offset(offset).limit(limit)
        return [
            {
                "id": str(student.id),
                "nome": student.nome,
                "idade": student.idade,
                "cpf": student.cpf,
                "contato": student.contato,
                "data_nascimento": str(student.data_nascimento),
                "email": student.email if student.email is not None else None,
                "especial": "Sim" if student.especial else "Não" ,
                "equipe": student.time.nome,
                "situacao": student.situacao,
                "ano_escolar": student.ano_escolar,
                "responsavel": student.responsavel.nome,
                "email_responsavel": student.responsavel.email,
                "endereco_responsavel": student.responsavel.endereco
            }
            for student in students
        ]
    except Exception as e:
        logging.error("Error getting students with pagination: " + str(e))
        return []

def search_students_by_name(name: str) -> List[dict]:
    try:
        students = models.Student.select().where(
            models.Student.nome.contains(name)
        ).limit(10)

        return [
            {
                "id": str(student.id),
                "nome": student.nome,
                "idade": student.idade,
                "cpf": student.cpf,
                "contato": student.contato,
                "data_nascimento": str(student.data_nascimento),
                "email": student.email,
                "especial": student.especial,
                "time_id": student.time.id,
                "time_nome": student.time.nome,
                "situacao": student.situacao,
                "ano_escolar": student.ano_escolar,
                "responsavel_id": student.responsavel.id,
                "responsavel_nome": student.responsavel.nome
            }
            for student in students
        ]
    
    except Exception as e:
        logging.error("Error searching students by name: " + str(e))
        return []

def count_all_payments() -> int:
    try:
        return models.Payment.select().count()
    except Exception as e:
        logging.error("Error counting payments: " + str(e))
        return 0

def count_all_students() -> int:
    try:
        return models.Student.select().count()
    except Exception as e:
        logging.error("Error counting students: " + str(e))
        return 0

def find_first_payment_not_paid(student_id: str):
    try:
        return models.Payment.select().where(models.Payment.aluno == student_id, models.Payment.status == "Pendente").order_by(models.Payment.data_vencimento).first()
    except Exception as e:
        logging.error("Error finding first payment not paid: " + str(e))
        return None

def update_user(id: str, email=None, cargo=None, nome=None):
    try:
        user = models.User.get(models.User.id == id)
        if email is not None:
            user.email = email
        if cargo is not None:
            user.cargo = cargo
        if nome is not None:
            user.nome = nome
        user.save()
        return {
            "id": str(user.id),
            "firebaseId": user.firebaseId,
            "firebaseIdWhoCreated": user.firebaseIdWhoCreated,
            "email": user.email,
            "cargo": user.cargo,
            "nome": user.nome
        }
    except Exception as e:
        logging.error("Error updating user: " + str(e))
        return None

def update_student(id: str, nome=None, idade=None, cpf=None, contato=None, data_nascimento=None, email=None, especial=False, time=None, situacao=None, ano_escolar=None, responsavel=None):
    try:
        student = models.Student.get(models.Student.id == id)
        if nome is not None:
            student.nome = nome
        if idade is not None:
            student.idade = idade
        if cpf is not None:
            student.cpf = cpf
        if contato is not None:
            student.contato = contato
        if data_nascimento is not None:
            student.data_nascimento = data_nascimento
        if email is not None:
            student.email = email
        if especial is not None:
            student.especial = especial
        if time is not None:
            student.time = time
        if situacao is not None:
            student.situacao = situacao
        if ano_escolar is not None:
            student.ano_escolar = ano_escolar
        if responsavel is not None:
            student.responsavel = responsavel
        student.save()
        return True
    except Exception as e:
        logging.error("Error updating student: " + str(e))
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

def update_responsible(id: str, nome=None, cpf=None, contato=None, data_nascimento=None, email=None, endereco=None):
    try:
        responsible = models.Responsible.get(models.Responsible.id == id)
        if nome is not None:
            responsible.nome = nome
        if cpf is not None:
            responsible.cpf = cpf
        if contato is not None:
            responsible.contato = contato
        if data_nascimento is not None:
            responsible.data_nascimento = data_nascimento
        if email is not None:
            responsible.email = email
        if endereco is not None:
            responsible.endereco = endereco
        responsible.save()
        return True
    except Exception as e:
        logging.error("Error updating responsible: " + str(e))
        return None

def update_team(id: str, nome=None, idade_minima=None, idade_maxima=None, professor=None, horario_inicio=None, horario_fim=None, dias_semana=None):
    try:
        team = models.Team.get(models.Team.id == id)
        if nome is not None:
            team.nome = nome
        if idade_minima is not None:
            team.idade_minima = idade_minima
        if idade_maxima is not None:
            team.idade_maxima = idade_maxima
        if professor is not None:
            team.professor = professor
        if horario_inicio is not None:
            team.horario_inicio = horario_inicio
        if horario_fim is not None:
            team.horario_fim = horario_fim
        if dias_semana is not None:
            team.dias_semana = dias_semana
        team.save()
        return True
    except Exception as e:
        logging.error("Error updating team: " + str(e))
        return None

def get_user_by_id(user_id: str):
    try:
        user = models.User.get(models.User.id == user_id)
        return {
            "id": str(user.id),
            "firebaseId": user.firebaseId,
            "firebaseIdWhoCreated": user.firebaseIdWhoCreated,
            "email": user.email,
            "cargo": user.cargo,
            "nome": user.nome
        }
    except Exception as e:
        logging.error("Error getting user by id: " + str(e))
        return None    
def get_responsible_by_id(responsible_id: str):
    try:
        responsible = models.Responsible.get(models.Responsible.id == responsible_id)
        return {
            "id": str(responsible.id),
            "nome": responsible.nome,
            "cpf": responsible.cpf,
            "contato": responsible.contato,
            "data_nascimento": str(responsible.data_nascimento),
            "email": responsible.email if responsible.email is not None else None,
            "endereco": responsible.endereco if responsible.endereco is not None else None
        }
    except Exception as e:
        logging.error("Error getting responsible by id: " + str(e))
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

def get_student_by_id(student_id: str):
    try:
        student = models.Student.get(models.Student.id == student_id)
        return {
            "id": str(student.id),
            "nome": student.nome,
            "idade": student.idade,
            "cpf": student.cpf,
            "contato": student.contato,
            "data_nascimento": str(student.data_nascimento),
            "email": student.email if student.email is not None else None,
            "especial": student.especial,
            "equipe": student.time.nome,
            "situacao": student.situacao,
            "ano_escolar": student.ano_escolar,
            "responsavel": student.responsavel.nome
        }
    except Exception as e:
        logging.error("Error getting student by id: " + str(e))
        return None

def get_team_by_id(team_id: str):
    try:
        team = models.Team.get(models.Team.id == team_id)
        return {
            "id": str(team.id),
            "nome": team.nome,
            "idade_minima": team.idade_minima,
            "idade_maxima": team.idade_maxima,
            "professor": team.professor.nome,
            "horario_inicio": team.horario_inicio,
            "horario_fim": team.horario_fim,
            "dias_semana": team.dias_semana
        }
    except Exception as e:
        logging.error("Error getting team by id: " + str(e))
        return None
    
def update_payment_status_overdue():
    today = datetime.today().date()
    query = (models.Payment
             .update(status="Em Atraso")
             .where((models.Payment.data_vencimento < today) & (models.Payment.status == "Pendente")))
    query.execute()
    print("Status dos pagamentos atualizado para 'Em Atraso'.")

def get_all_payments_due_soon():
    today = datetime.today()
    due_soon = today + timedelta(days=3)
    query = (models.Payment
             .select(models.Payment, models.Student, models.Responsible)
             .join(models.Student, on=(models.Payment.aluno == models.Student.id))
             .join(models.Responsible, on=(models.Student.responsavel == models.Responsible.id))
             .where((models.Payment.data_vencimento.between(today, due_soon)) & (models.Payment.status == "Pendente")))
    return query

def get_all_payments_overdue():
    today = datetime.today().date()
    query = (models.Payment
             .select(models.Payment, models.Student, models.Responsible)
             .join(models.Student, on=(models.Payment.aluno == models.Student.id))
             .join(models.Responsible, on=(models.Student.responsavel == models.Responsible.id))
             .where((models.Payment.data_vencimento < today) & (models.Payment.status == "Em Atraso")))
    return query

# Função para buscar todos os pagamentos pendentes do mes atual somados
def get_payments_receivable_in_a_month():
    today = datetime.today()
    first_day = today.replace(day=1)
    last_day = today.replace(day=1, month=today.month+1) - timedelta(days=1)
    query = (models.Payment
             .select(fn.SUM(models.Payment.valor).alias('total'))
             .where((models.Payment.data_vencimento.between(first_day, last_day)) & (models.Payment.status == "Pendente")))
    return query[0].total

def get_payments_received_in_a_month():
    today = datetime.today()
    first_day = today.replace(day=1)
    last_day = today.replace(day=1, month=today.month+1) - timedelta(days=1)
    query = (models.Payment
             .select(fn.SUM(models.Payment.valor).alias('total'))
             .where((models.Payment.data_pagamento.between(first_day, last_day)) & (models.Payment.status == "Pago")))
    return query[0].total

def get_payments_receivable_overdue():
    today = datetime.today().date()
    query = (models.Payment
             .select(fn.SUM(models.Payment.valor).alias('total'))
             .where((models.Payment.data_vencimento < today) & (models.Payment.status == "Em Atraso")))
    return query[0].total

def get_students_per_team():
    query = (models.Student
             .select(models.Student.time, fn.COUNT(models.Student.id).alias('total'))
             .group_by(models.Student.time))
    return [
        {
            "equipe": student.time.nome,
            "total": student.total
        }
        for student in query
    ]

def get_students_active_inactive():
    query = (models.Student
             .select(models.Student.situacao, fn.COUNT(models.Student.id).alias('total'))
             .group_by(models.Student.situacao))
    return [
        {
            "situacao": student.situacao,
            "total": student.total
        }
        for student in query
    ]