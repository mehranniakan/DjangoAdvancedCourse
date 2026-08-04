from celery import shared_task
from functions import send_email_function
from ToDoApp.models import Task

from account.models import User


@shared_task
def send_email(to: list,
               sender: str,
               subject: str,
               message: str,
               email_type="txt",
               template=None,
               context=None, ):
    if email_type == "txt":
        send_email_function(
            to=to,
            sender=sender,
            subject=subject,
            message=message,
            email_type=email_type,
        )
    elif email_type == "html":
        send_email_function(
            to=to,
            sender=sender,
            subject=subject,
            message=message,
            email_type=email_type,
            template=template,
            context=context,
        )

    return "Email sent successfully"


@shared_task
def clear_tasks():
    Task.objects.all().delete()
    return "Tasks deleted successfully"


@shared_task
def clear_unverified_accounts():
    User.objects.filter(is_verified=False).delete()
    return "Unverified accounts deleted successfully"
