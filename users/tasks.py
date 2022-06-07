from django.core.mail import send_mail
from goodreads.celery import app


@app.task()
def send_email_celery(subject, message, email_from, receipent_list):
    send_mail(subject, message, email_from, receipent_list)