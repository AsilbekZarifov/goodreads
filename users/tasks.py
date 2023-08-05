from django.core.mail import send_mail
from goodreads.celery import app


@app.task()
def send_eamil(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        "asilprogrammer@gmail.com",
        recipient_list
    )