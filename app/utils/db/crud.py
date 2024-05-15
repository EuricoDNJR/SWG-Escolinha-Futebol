from . import models

def create_user(firebaseId: str, firebaseIdWhoCreated: str, email: str, cargo: str):
    return models.User.create(firebaseId=firebaseId, firebaseIdWhoCreated=firebaseIdWhoCreated, email=email, cargo=cargo)

def create_responsible(nome: str, cpf: str, contato: str, data_nascimento: str, email: str):
    return models.Responsible.create(nome=nome, cpf=cpf, contato=contato, data_nascimento=data_nascimento, email=email)

def create_team(nome: str, idade_minima: int, idade_maxima: int, professor: str, horario_inicio: str, horario_fim: str, dias_semana: str):
    return models.Team.create(nome=nome, idade_minima=idade_minima, idade_maxima=idade_maxima, professor=professor, horario_inicio=horario_inicio, horario_fim=horario_fim, dias_semana=dias_semana)

def create_student(nome: str, idade: int, cpf: str, contato: str, data_nascimento: str, email: str, especial: bool, time: str, situacao: str, responsavel: str):
    return models.Student.create(nome=nome, idade=idade, cpf=cpf, contato=contato, data_nascimento=data_nascimento, email=email, especial=especial, time=time, situacao=situacao, responsavel=responsavel)

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