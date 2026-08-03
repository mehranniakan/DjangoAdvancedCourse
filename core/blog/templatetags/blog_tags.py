# templatetags/blog_tags.py
from blog.models import Category
from django import template
from django.shortcuts import get_object_or_404


register = template.Library()


@register.filter
def get_category_name(category_id):
        category = get_object_or_404(Category, id=category_id)
        return category.name
