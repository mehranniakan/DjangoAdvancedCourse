from django.contrib import admin

from account.models import User


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_superuser', 'is_active', 'created_date', 'updated_date')
    search_fields = ('email',)
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    date_hierarchy = 'created_date'
    ordering = ('-created_date',)
    fieldsets = (
        ('User Info', {'fields': ('email', 'password')}),
        ('User Status',{'fields': ('is_staff', 'is_superuser', 'is_active')}),
        ('Permissions & Group', {'fields': ('groups', 'user_permissions')}),
    )