from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from functions import generate_token, send_email_function


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def send_account_verification_email(sender, instance, created, **kwargs):

    if not created:
        return
    else:
        token = generate_token(instance)
        host_name = "https://127.0.0.1:8000"
        verify_url = reverse("account:api-v1:account_verify_jwt")

        verify_url = f"{host_name}{verify_url}?token={token}"
        
        send_email_function(
            to=[instance.email],
            sender="blog@info.com",
            subject="verification email",
            message="please verify your email address",
            email_type="html",
            template="emails/account_verify.tpl",
            context={
                "user": instance,
                "activation_link": verify_url,
            },
        )
