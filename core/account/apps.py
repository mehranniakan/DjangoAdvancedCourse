from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "account"

    def ready(self):
        # این خط باعث می‌شود سیگنال‌ها هنگام شروع به کار جنگو ثبت شوند
        import account.signals
