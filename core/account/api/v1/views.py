from blog.api.v1.pagination import DefaultPagination
from blog.api.v1.serializers import PostSerializer
from blog.models import Posts
from django.shortcuts import get_object_or_404
from jwt import exceptions
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from ...models import User, UserProfile
from .serializers import (
    AuthTokenSerializer,
    ChangePasswordSerializer,
    JwtSerializer,
    ProfileSerializer,
    RegisterSerializer,
)


class RegisterApi(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        user_serializer = RegisterSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return Response(user_serializer.validated_data, status=status.HTTP_201_CREATED)


class AuthTokenApi(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class JwtAuthToken(TokenObtainPairView):
    serializer_class = JwtSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


class DiscardTokenApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        tk = Token.objects.filter(user=request.user)
        if tk.exists():
            tk.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ChangePasswordApi(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"Msg": "Password Changed Successfully"}, status=status.HTTP_200_OK
        )


class ProfileApi(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()

    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)


class VerifyAccountApi(APIView):
    def get(self, request):

        token = request.query_params.get("token")

        if token:
            try:
                token = AccessToken(token)

            except exceptions.ExpiredSignatureError:
                return Response(
                    {"Msg": "Token Expired"}, status=status.HTTP_400_BAD_REQUEST
                )
            except exceptions.InvalidTokenError:
                return Response(
                    {"Msg": "Invalid Token"}, status=status.HTTP_400_BAD_REQUEST
                )

            user_id = token["user_id"]
            user_obj = get_object_or_404(User, id=user_id)

            if user_obj.is_verified:
                return Response(
                    {"Msg": "User is already verified"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                user_obj.is_verified = True
                user_obj.save()
                return Response({"Msg": "User is verified"}, status=status.HTTP_200_OK)

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class MyPostAPI(GenericAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        my_post = Posts.objects.filter(author__user=request.user)

        if my_post.exists():
            serializer = PostSerializer(
                my_post, many=True, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
