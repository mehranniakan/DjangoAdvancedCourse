import uuid

from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework_simplejwt.tokens import RefreshToken


def is_valid_uuid(uuid_to_test, version=4):
    try:
        # check for validity of Uuid
        uuid_obj = uuid.UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return True


def send_email_function(
        to: list,
        sender: str,
        subject: str,
        message: str,
        email_type="txt",
        template=None,
        context=None,
):
    if email_type == "txt":
        send_mail(
            subject,
            message,
            sender,
            to,
            fail_silently=False,
        )
    elif email_type == "html":
        html = render_to_string(template, context)

        email = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=sender,
            to=to,
        )

        email.attach_alternative(html, "text/html")
        email.send()


def generate_token(user: object):
    token = RefreshToken.for_user(user)
    token = token.access_token
    return token
