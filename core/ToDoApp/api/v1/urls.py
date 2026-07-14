from rest_framework.routers import DefaultRouter

from ToDoApp.api.v1.views import TaskApi

router = DefaultRouter()
router.register("Task", TaskApi, basename="Task")
urlpatterns = router.urls
