from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

app_name = 'api-v1'

router = DefaultRouter()
router.register('post',PostApi,basename='post')
router.register('category',CategoryApi,basename='category')
urlpatterns = router.urls

# urlpatterns = [
    # path('post', posts, name='views_post'),
    # path('PostApi/', PostListCreateApi.as_view(), name='views_PostApi'),
    # path('PostApi/<uuid:pk>/',PostRetrieveUpdateDestroyApi.as_view(), name='views_PostApi'),
# ]