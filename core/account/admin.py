from django.contrib import admin

from account.models import User, UserProfile


# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "is_staff",
        "is_superuser",
        "is_active",
        "is_verified",
        "created_date",
        "updated_date",
    )
    search_fields = ("email",)
    list_filter = ("is_staff", "is_superuser", "is_active")
    date_hierarchy = "created_date"
    ordering = ("-created_date",)
    fieldsets = (
        ("User Info", {"fields": ("email", "password")}),
        ("User Status", {"fields": ("is_staff", "is_superuser", "is_active","is_verified")}),
        ("Permissions & Group", {"fields": ("groups", "user_permissions")}),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "first_name",
        "last_name",
        "birth_date",
        "created_date",
        "updated_date",
    )
    search_fields = ("first_name", "last_name")
    list_filter = ("birth_date",)
    date_hierarchy = "created_date"
    ordering = ("-created_date",)
    fieldsets = (
        ("User Info", {"fields": ("user", "first_name", "last_name", "birth_date")}),
    )
