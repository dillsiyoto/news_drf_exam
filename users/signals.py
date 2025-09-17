from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import Client


@receiver(post_save, sender=Client)
def send_activation_email(sender, instance: Client, created: bool, **kwargs):
    if instance.is_superuser:
        return
    
    if created:
        subject = "Активация аккаунта"
        message = (
            f"Здравствуйте!\n\n"
            f"Ваш код активации: {instance.activation_code}\n\n"
            f"Используйте его на /auth/activate/ вместе с вашим email."
        )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],             
            fail_silently=False,
        )
