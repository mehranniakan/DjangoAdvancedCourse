from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "title",
        "description",
        "status",
        "created_date",
        "updated_date",
    )
    search_fields = (
        "title",
        "user",
    )
    list_filter = ("status",)
    date_hierarchy = "created_date"
    ordering = ("-created_date",)
    fieldsets = (
        ("User Info", {"fields": ("user",)}),
        (
            "Task Info",
            {
                "fields": (
                    "title",
                    "description",
                )
            },
        ),
        ("Task Status", {"fields": ("status",)}),
    )
