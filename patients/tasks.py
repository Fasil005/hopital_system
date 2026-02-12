from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_welcome_email(fhir_id, email):
    send_mail(
        subject="Welcome",
        message=f"Patient {fhir_id} registered successfully.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )