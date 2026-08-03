from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from ToDoApp.api.v1.permission import OwnerOnly
from ToDoApp.api.v1.serializers import TaskSerializer

from ...models import Task
from .paginations import DefaultPaginationApp


class TaskApi(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, OwnerOnly]  # noqa: RUF012
    pagination_class = DefaultPaginationApp
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ("status",)
    search_fields = ("title", "description")
    ordering_fields = ("created_date",)
