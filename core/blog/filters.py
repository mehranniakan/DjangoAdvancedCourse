from django.db.models import Q
from django_filters import CharFilter, FilterSet

from blog.models import Category, Posts


class PostFilters(FilterSet):
    q = CharFilter(method="filter_post_name", label="نام پزشک")
    category = CharFilter(
        method="filter_post_category",
    )

    class Meta:
        model = Posts
        fields = ["category"]

    def filter_post_name(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(content__icontains=value))

    def filter_post_category(self, queryset, name, value):
        return queryset.filter(category=Category.objects.get(pk=value))
