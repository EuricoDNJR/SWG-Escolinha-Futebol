from .db.crud import get_all_payments_due_soon

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
    

def notify_due_payments():
    payments_due_soon = get_all_payments_due_soon()
    for payment in payments_due_soon:
        to_email = payment.aluno.responsavel.email
        subject = "Aviso de Vencimento de Parcela"
        body = f"""
        <p>Prezado {payment.aluno.responsavel.nome},</p>
        <p>Informamos que a parcela de {payment.valor} do aluno {payment.aluno.nome} está próxima do vencimento, no dia {payment.data_vencimento}.</p>
        <p>Por favor, efetue o pagamento o quanto antes.</p>
        <p>Atenciosamente,</p>
        <p>Equipe FARP</p>
        """
        send_email(to_email, subject, body)


def send_notifications_now():
    notify_due_payments()
    return {"message": "Email notifications sent successfully."}

