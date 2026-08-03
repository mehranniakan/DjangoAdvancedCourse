import hashlib

from blog.models import Comments, CommentsReplies, Posts
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, permissions, status, viewsets
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from ...models import Category
from .pagination import DefaultPagination
from .permissions import (
    IsActiveUser,
    OwnerOnlyPostPermission
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    CommentVerifySerializer,
    PostSerializer,
    ReplySerializer,
)

# @api_view(['POST', 'GET', 'PUT', 'DELETE'])
# def posts(request):
#     if request.method == 'POST':
#         serialized_data = PostSerializer(data=request.data)
#
#         serialized_data.is_valid(raise_exception=True)
#         serialized_data.save()
#         return Response(serialized_data.data)
#
#     elif request.method == 'GET':
#         show_type = request.query_params.get('type')
#
#         if show_type == 'Single':
#             post_id = request.query_params.get('id')
#
#             if is_valid_uuid(post_id):
#                 post_obj = get_object_or_404(Posts, pk=post_id)
#                 post_serializer = PostSerializer(post_obj)
#                 return Response(post_serializer.data)
#             else:
#                 return Response(status=status.HTTP_400_BAD_REQUEST)
#
#         elif show_type == 'All':
#             post_obj = Posts.objects.all()
#             post_serializer = PostSerializer(post_obj, many=True)
#             return Response(post_serializer.data)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'PUT':
#         post_id = request.data.get('id')
#
#         if is_valid_uuid(post_id):
#             post_obj = get_object_or_404(Posts, pk=post_id)
#             post_serializer = PostSerializer(post_obj, data=request.data)
#             post_serializer.is_valid(raise_exception=True)
#             post_serializer.save()
#             return Response(post_serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         post_id = request.query_params.get('id')
#         if is_valid_uuid(post_id):
#             post_obj = get_object_or_404(Posts, pk=post_id)
#             post_obj.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


"""API Views"""
# class PostApi(APIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     serializer_class = PostSerializer
#
#     def get(self, request):
#         post_obj = Posts.objects.all()
#         serializer = PostSerializer(post_obj, many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)
#
#
#     def post(self, request):
#         post_serializer = PostSerializer(data=request.data)
#         post_serializer.is_valid(raise_exception=True)
#         post_serializer.save()

"""Generic Api View"""
# class PostListCreateApi(ListAPIView,CreateAPIView):
#
#     queryset = Posts.objects.filter(status=True)
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
# class PostRetrieveUpdateDestroyApi(RetrieveUpdateDestroyAPIView):
#     queryset = Posts.objects.filter(status=True)
#     serializer_class = PostSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def patch(self, request, *args, **kwargs):
#         return self.partial_update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

"""View Sets"""


# class PostApi(viewsets.ViewSet):
#     queryset = Posts.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#
#     def list(self, request):
#         post_serializer = PostSerializer(self.queryset,many=True)
#         return Response(post_serializer.data,status=status.HTTP_200_OK)
#
#     def create(self, request):
#         post_serializer = PostSerializer(data=request.data)
#         post_serializer.is_valid(raise_exception=True)
#         post_serializer.save()
#         return Response(post_serializer.data, status=status.HTTP_201_CREATED)
#
#     def retrieve(self, request, pk=None):
#         post_obj = get_object_or_404(self.queryset, pk=pk)
#         serializer = PostSerializer(post_obj)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def update(self, request, pk=None):
#         post_obj = get_object_or_404(self.queryset, pk=pk)
#         post_serializer = PostSerializer(post_obj,data=request.data)
#         post_serializer.is_valid(raise_exception=True)
#         post_serializer.save()
#         return Response(post_serializer.data, status=status.HTTP_200_OK)
#
#     def partial_update(self, request, pk=None):
#         post_obj = get_object_or_404(self.queryset, pk=pk)
#         post_serializer= PostSerializer(post_obj, data=request.data, partial=True)
#         post_serializer.is_valid(raise_exception=True)
#         post_serializer.save()
#         return Response(post_serializer.data, status=status.HTTP_200_OK)
#
#     def destroy(self, request, pk=None):
#         post_obj = get_object_or_404(self.queryset, pk=pk)
#         post_obj.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class PostApi(viewsets.ModelViewSet):
    queryset = Posts.objects.filter(
        author__user__is_active=True, author__user__is_verified=True
    )
    serializer_class = PostSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    )
    pagination_class = DefaultPagination
    filterset_fields = ["category", "status", "author"]
    search_fields = ("title", "content")
    ordering_fields = ("created_date",)

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [
                IsAuthenticated,
                IsActiveUser,
                OwnerOnlyPostPermission,
            ]

        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):
        post_pk = kwargs.get("pk")
        cache_key = f"api:post:detail:{post_pk}"

        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        cache.set(cache_key, data, timeout=300)
        return Response(data)

    def list(self, request, *args, **kwargs):

        query_params = request.GET.urlencode()
        params_hash = hashlib.md5(query_params.encode("utf-8")).hexdigest()
        cache_key = f"api:post:list:{params_hash}"

        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.get_paginated_response(serializer.data).data
        else:
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data

        cache.set(cache_key, data, timeout=300)
        return Response(data)

    def _clear_related_caches(self, post_pk=None):

        if post_pk:
            cache.delete(f"api:post:detail:{post_pk}")

        if hasattr(cache, "delete_pattern"):
            cache.delete_pattern("api:post:list:*")
        else:
            cache.clear()

    def perform_create(self, serializer):
        serializer.save()
        self._clear_related_caches()

    def perform_update(self, serializer):
        instance = serializer.save()
        self._clear_related_caches(post_pk=instance.pk)

    def perform_destroy(self, instance):
        post_pk = instance.pk
        instance.delete()
        self._clear_related_caches(post_pk=post_pk)


class CategoryApi(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class CommentApi(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    pagination_class = DefaultPagination
    serializer_class = CommentSerializer
    http_method_names = ["post", "put", "patch", "delete", "head", "options"]  # noqa: RUF012

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.AllowAny]

        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [
                IsAuthenticated,
                IsActiveUser,
                OwnerOnlyPostPermission,
            ]
        else:
            permission_classes = [IsAuthenticated, IsActiveUser]

        return [permission() for permission in permission_classes]

    def _clear_related_caches(self, comment_pk=None):

        if comment_pk:
            cache.delete(f"api:post:comment:detail:{comment_pk}")

        if hasattr(cache, "delete_pattern"):
            cache.delete_pattern("api:post:comment:detail:*")
        else:
            cache.clear()

    def perform_create(self, serializer):
        serializer.save()
        self._clear_related_caches()

    def perform_update(self, serializer):
        instance = serializer.save()
        self._clear_related_caches(comment_pk=instance.pk)

    def perform_destroy(self, instance):
        comment_pk = instance.pk
        instance.delete()
        self._clear_related_caches(comment_pk=comment_pk)


class ReplyApi(viewsets.ModelViewSet):
    queryset = CommentsReplies.objects.all()
    pagination_class = DefaultPagination
    serializer_class = ReplySerializer
    http_method_names = ["post", "put", "patch", "delete", "head", "options"]  # noqa: RUF012

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.AllowAny]

        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [
                IsAuthenticated,
                IsActiveUser,
            ]
        else:
            permission_classes = [IsAuthenticated, IsActiveUser]

        return [permission() for permission in permission_classes]

    def _clear_related_caches(self, reply_pk=None):

        if reply_pk:
            cache.delete(f"api:comment:reply:{reply_pk}")

        if hasattr(cache, "delete_pattern"):
            cache.delete_pattern("api:comment:reply:*")
        else:
            cache.clear()

    def perform_create(self, serializer):
        serializer.save()
        self._clear_related_caches()

    def perform_update(self, serializer):
        instance = serializer.save()
        self._clear_related_caches(reply_pk=instance.pk)

    def perform_destroy(self, instance):
        reply_pk = instance.pk
        instance.delete()
        self._clear_related_caches(reply_pk=reply_pk)


class CommentVerifyApi(APIView):
    serializer_class = CommentVerifySerializer
    permission_classes = [IsAuthenticated]  # noqa: RUF012
    http_method_names = ["post"]  # noqa: RUF012

    @swagger_auto_schema(request_body=CommentVerifySerializer)
    def post(self, request):

        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        comment_pk = serializer.validated_data["comment_pk"]

        comment = get_object_or_404(
            Comments,
            pk=comment_pk,
        )

        self.check_object_permissions(request, comment)

        comment.is_approved = True
        comment.save(update_fields=["is_approved"])

        if cache.get(f"api:post:comment:{comment.post.id}"):
            cache.delete(f"api:post:comment:{comment.post.id}")

        return Response(
            {"detail": "کامنت با موفقیت تأیید شد."},
            status=status.HTTP_200_OK,
        )


class PostCommentApi(viewsets.ReadOnlyModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    pagination_class = DefaultPagination

    def get_queryset(self):
        post_id = self.kwargs.get("post_pk")
        return (
            Comments.objects.filter(post_id=post_id, is_approved=True)
            .select_related("author")
            .order_by("-created_date")
        )

    def list(self, request, *args, **kwargs):
        post_id = self.kwargs.get("post_pk")
        cache_key = f"api:post:comment:{post_id}"

        if cache.get(cache_key):
            return Response(cache.get(cache_key), status=status.HTTP_200_OK)
        else:
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                data = self.get_paginated_response(serializer.data).data
            else:
                serializer = self.get_serializer(queryset, many=True)
                data = serializer.data

            cache.set(cache_key, data, 300)
            return Response(data, status=status.HTTP_200_OK)


class ReplyCommentApi(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReplySerializer
    permission_classes = [AllowAny]
    pagination_class = DefaultPagination

    def get_queryset(self):
        comment_id = self.kwargs.get("comment_pk")
        return (
            CommentsReplies.objects.filter(
                comment_id=comment_id, comment__is_approved=True
            )
            .select_related("author")
            .order_by("-created_date")
        )

    def list(self, request, *args, **kwargs):
        comment_id = self.kwargs.get("comment_pk")
        cache_key = f"api:comment:replies:{comment_id}"

        if cache.get(cache_key):
            return Response(cache.get(cache_key), status=status.HTTP_200_OK)
        else:
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                data = self.get_paginated_response(serializer.data).data
            else:
                serializer = self.get_serializer(queryset, many=True)
                data = serializer.data

            cache.set(cache_key, data, 300)
            return Response(data, status=status.HTTP_200_OK)
