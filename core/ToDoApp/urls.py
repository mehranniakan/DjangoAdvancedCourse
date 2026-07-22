from django.urls import path, include

from . import views
from .views import update_task_status

app_name = "ToDoApp"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("tasks/create/", views.CreateTasksView.as_view(), name="add_task"),
    path("tasks/edit/<uuid:pk>/", views.UpdateTasksView.as_view(), name="edit_task"),
    path("tasks/edit/done/<uuid:pk>/", update_task_status, name="complete_task"),
    path(
        "tasks/delete/<uuid:pk>/", views.DeleteTasksView.as_view(), name="delete_task"
    ),
    path("api/v1/", include("ToDoApp.api.v1.urls")),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
