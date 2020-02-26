import os
import smtplib, ssl


def send_confirmation_email(receiver_email, alumni_uuid):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = os.getenv('SENDER_EMAIL')
    password = os.getenv('EMAIL_ACCOUNT_PASSWORD')

    confirmation_link = f"https://alumni-frontend.herokuapp.com/signup/{alumni_uuid}/"

    message = f"""Subject: NaUKMA Alumni service

        Please, follow the link to finish your registration in NaUKMA alumni service {confirmation_link} ."""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

    return 
