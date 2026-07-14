from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter

from ToDoApp.api.v1.permission import OwnerOnly
from ToDoApp.api.v1.serializers import TaskSerializer
from ...models import Task


class TaskApi(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, OwnerOnly]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ("status",)
    search_fields = ("title", "description")
    ordering_fields = ("created_date",)
