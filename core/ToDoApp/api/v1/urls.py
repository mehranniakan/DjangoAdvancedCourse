from rest_framework.routers import DefaultRouter

from ToDoApp.api.v1.views import TaskApi
from blog.api.v1.views import PostApi

router = DefaultRouter()
router.register('Task',TaskApi,basename='Task')
urlpatterns = router.urls