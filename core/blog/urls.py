from django.urls import include, path

from .views import (
    CommentCreateView,
    CommentDeleteView,
    CommentUpdateView,
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    PostUpdateView,
    ReplyCreateView,
    ReplyDeleteView,
    ReplyUpdateView,
    approve_comment,
)

app_name = "blog"

urlpatterns = [
    path("", PostListView.as_view(), name="blog_main"),
    path("post/add/", PostCreateView.as_view(), name="add_post"),
    path("post/edit/<uuid:pk>/", PostUpdateView.as_view(), name="edit_post"),
    path("post/delete/<uuid:pk>/", PostDeleteView.as_view(), name="delete_post"),
    path("detail/<uuid:id>/", PostDetailView.as_view(), name="blog_detail"),
    path("detail/comment/verify/<uuid:pk>/", approve_comment, name="comment_verify"),
    path("detail/commnet/add/", CommentCreateView.as_view(), name="add_comment"),
    path("detail/reply/edit/<uuid:pk>", ReplyUpdateView.as_view(), name="edit_reply"),
    path("detail/reply/delete/<uuid:pk>", ReplyDeleteView.as_view(), name="delete_reply"),
    path("detail/reply/add/", ReplyCreateView.as_view(), name="add_reply"),
    path(
        "detail/comment/edit/<uuid:pk>/",
        CommentUpdateView.as_view(),
        name="edit_comment",
    ),
    path(
        "detail/comment/delete/<uuid:pk>/",
        CommentDeleteView.as_view(),
        name="delete_comment",
    ),
    path("api/v1/", include("blog.api.v1.urls"), name="api-v1"),
]
