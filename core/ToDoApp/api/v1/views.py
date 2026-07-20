from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend

from .paginations import DefaultPagination
from ...models import Task
from ToDoApp.api.v1.permission import OwnerOnly
from ToDoApp.api.v1.serializers import TaskSerializer
from rest_framework.filters import SearchFilter, OrderingFilter

class TaskApi(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = DefaultPagination
    permission_classes = [permissions.IsAuthenticated,OwnerOnly]
    filter_backends = (DjangoFilterBackend,SearchFilter,OrderingFilter)
    filterset_fields = ('status',)
    search_fields = ('title','description')
    ordering_fields = ('created_date',)