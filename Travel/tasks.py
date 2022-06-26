from asyncio import tasks
from datetime import datetime, timedelta
from time import time
from celery import shared_task
from django.core.mail import send_mail
from django.template import loader, loaders
from django.contrib.auth import get_user_model
from TravelAndLogistic.celery import app

User = get_user_model()

@shared_task
@app.task
def CostructEmail(data):
    user = User.objects.get(id = data["user"])
    data["user"] = user
    data["email"] = user.email
    context = loader.render_to_string("email.html", data)
    subject = "Travel Ticket Detail"
    send_mail(
        subject=subject,
        message="",
        html_message=context,
        recipient_list=[user.email],
        from_email=  "haryournifejt@gmail.com"
    )

