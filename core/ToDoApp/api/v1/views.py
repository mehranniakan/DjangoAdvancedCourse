from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from ToDoApp.api.v1.permission import OwnerOnly
from ToDoApp.api.v1.serializers import TaskSerializer
from .paginations import DefaultPaginationApp
from ...models import Task


class TaskApi(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, OwnerOnly]
    pagination_class = DefaultPaginationApp
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ("status",)
    search_fields = ("title", "description")
    ordering_fields = ("created_date",)
