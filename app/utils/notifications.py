from .db.crud import get_all_payments_due_soon, get_all_payments_overdue
from .helper import logging
import smtplib
import email.message
import os
import dotenv

dotenv.load_dotenv()

def send_email(to_email, subject, body):
    msg = email.message.Message()
    msg['Subject'] = subject
    msg['From'] = os.getenv('EMAIL_SENDER')
    msg['To'] = to_email
    password = os.getenv('EMAIL_PASSWORD')
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(body)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado com sucesso!')
    s.quit()
    

def notify_due_soon_payments():
    logging.info("Sending notifications for payments due soon.")
    payments_due_soon = get_all_payments_due_soon()
    for payment in payments_due_soon:
        to_email = payment.aluno.responsavel.email
        
        if to_email is not None:
            subject = "Aviso de Vencimento de Parcela"
            data_vencimento_formatada = payment.data_vencimento.strftime('%d-%m-%Y')
            body = f"""
            <p>Prezado {payment.aluno.responsavel.nome},</p>
            <p>Informamos que a parcela de {payment.valor} do aluno {payment.aluno.nome} está próxima do vencimento, no dia {data_vencimento_formatada}.</p>
            <p>Por favor, efetue o pagamento o quanto antes.</p>
            <p>Atenciosamente,</p>
            <p>Equipe FARP</p>
            """
            send_email(to_email, subject, body)
        else:
            print(f"Responsável {payment.aluno.responsavel.nome} não tem um e-mail cadastrado. Não foi possível enviar a notificação.")

def notify_overdue_payments():
    logging.info("Sending notifications for overdue payments.")
    payments_overdue = get_all_payments_overdue()
    for payment in payments_overdue:
        to_email = payment.aluno.responsavel.email
        
        if to_email is not None:
            subject = "Aviso de Pagamento em Atraso"
            data_vencimento_formatada = payment.data_vencimento.strftime('%d-%m-%Y')
            body = f"""
            <p>Prezado {payment.aluno.responsavel.nome},</p>
            <p>Informamos que a parcela de {payment.valor} do aluno {payment.aluno.nome} está em atraso desde o dia {data_vencimento_formatada}.</p>
            <p>Por favor, efetue o pagamento o quanto antes para evitar o bloqueio da matricula.</p>
            <p>Atenciosamente,</p>
            <p>Equipe FARP</p>
            """
            send_email(to_email, subject, body)
        else:
            print(f"Responsável {payment.aluno.responsavel.nome} não tem um e-mail cadastrado. Não foi possível enviar a notificação.")


def send_notifications_now(due_soon: bool = True, overdue: bool = True):
    if due_soon:
        notify_due_soon_payments()
    if overdue:
        notify_overdue_payments()
    return {"message": "Email notifications sent successfully."}

