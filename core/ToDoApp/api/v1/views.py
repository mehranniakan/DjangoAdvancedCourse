from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter

from ToDoApp.api.v1.permission import OwnerOnly
from ToDoApp.api.v1.serializers import TaskSerializer
from .paginations import DefaultPagination
from ...models import Task


class TaskApi(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    pagination_class = DefaultPagination
    permission_classes = [permissions.IsAuthenticated, OwnerOnly]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ("status",)
    search_fields = ("title", "description")
    ordering_fields = ("created_date",)

    def get_queryset(self):
        tasks = Task.objects.filter(user__user = self.request.user)
        return tasks

