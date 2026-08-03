# templatetags/blog_tags.py
from django import template
from django.shortcuts import get_object_or_404

from account.models import User, UserProfile

register = template.Library()


@register.filter
def get_user_profile(user_id):
    profile = get_object_or_404(UserProfile, user=User.objects.get(pk=user_id))
    return profile.pk
