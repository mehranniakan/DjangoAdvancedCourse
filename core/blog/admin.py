from django.contrib import admin

from blog.models import Posts, Category


# Register your models here.


@admin.register(Posts)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "content",
        "status",
        "created_date",
        "updated_date",
    )
    search_fields = ("title", "content")
    list_filter = ("status", "author", "category")
    date_hierarchy = "created_date"
    ordering = ("-created_date",)
    readonly_fields = ("id", "created_date", "updated_date")
    fieldsets = (
        (
            "Post Details",
            {
                "fields": (
                    "title",
                    "author",
                    "content",
                    "category",
                    "status",
                    "created_date",
                    "updated_date",
                )
            },
        ),
        ("Identifier Info", {"fields": ("id", "slug")}),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "created_date", "updated_date")
    search_fields = ("name",)
    list_filter = ("status",)
    date_hierarchy = "created_date"
    ordering = ("-created_date",)
    fieldsets = (("Category Details", {"fields": ("name", "status")}),)
