from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .pagination import DefaultPagination
from .serializers import CategorySerializer, PostSerializer
from ...models import Posts, Category

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
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly, OwnerOnlyPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    )
    pagination_class = DefaultPagination
    filterset_fields = ["category", "status", "author"]
    search_fields = ("title", "content")
    ordering_fields = ("created_date",)


class CategoryApi(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
