from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryApi,
    CommentApi,
    CommentVerifyApi,
    PostApi,
    PostCommentApi,
    ReplyApi,
    ReplyCommentApi,
)

app_name = "api-v1"

router = DefaultRouter()
router.register("post", PostApi, basename="post")
router.register("category", CategoryApi, basename="category")
router.register("comment", CommentApi, basename="comment")
router.register("reply", ReplyApi, basename="reply")

post_comment_list = PostCommentApi.as_view(
    {
        "get": "list",
    }
)
post_comment_detail = PostCommentApi.as_view(
    {
        "get": "retrieve",
    }
)
reply_comment_list = ReplyCommentApi.as_view(
    {
        "get": "list",
    }
)

reply_comment_detail = ReplyCommentApi.as_view(
    {
        "get": "retrieve",
    }
)

urlpatterns = [
    path("post/<uuid:post_pk>/comments/", post_comment_list, name="post-comments-list"),
    path(
        "post/<uuid:post_pk>/comments/<uuid:pk>/",
        post_comment_detail,
        name="post-comments-detail",
    ),
    path(
        "comment/<uuid:comment_pk>/reply/",
        reply_comment_list,
        name="comment-reply-list",
    ),
    path(
        "comment/<uuid:comment_pk>/reply/<uuid:pk>/",
        reply_comment_detail,
        name="comment-reply-detail",
    ),
    path(
        "comment/verify/",
        CommentVerifyApi.as_view(),
        name="comment-verify",
    ),
    path("", include(router.urls)),
]
