import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from users.models import Client


@receiver(post_save, sender=Client)
def send_activation_email(sender, instance: Client, created: bool, **kwargs):
    if instance.is_superuser:
        return
    
    if created:
        instance.activation_code = uuid.uuid4()
        instance.save(update_fields=["activation_code"])
        
        activation_link = "http://127.0.0.1:8000/auth/activate/"
        
        subject = "Активация аккаунта"
        message = (
            f"Здравствуйте!\n\n"
            f"Ваш код активации: {instance.activation_code}\n\n"
            f"Введите его по этой ссылке: {activation_link}"
        )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],             
            fail_silently=False,
        )
