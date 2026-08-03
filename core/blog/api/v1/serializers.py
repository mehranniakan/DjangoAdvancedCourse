from account.api.v1.serializers import ProfileSerializer
from account.models import UserProfile
from blog.models import Category, Comments, CommentsReplies, Posts
from django.shortcuts import get_object_or_404
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    snippet = serializers.ReadOnlyField(source="get_snippet", read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    url = serializers.SerializerMethodField(method_name="get_url")

    def get_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)

        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("url", None)
            rep.pop("snippet", None)
        else:
            rep["author"] = ProfileSerializer(instance.author).data
            rep.pop("content", None)
            rep["category"] = CategorySerializer(instance.category).data
        return rep

    def create(self, validated_data):
        validated_data["author"] = UserProfile.objects.get(
            user__id=self.context.get("request").user.id
        )
        return super().create(validated_data)

    class Meta:
        model = Posts
        read_only_fields = ("id", "author", "created_date", "updated_date")
        fields = (
            "id",
            "title",
            "author",
            "content",
            "snippet",
            "category",
            "slug",
            "url",
            "created_date",
            "updated_date",
        )


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    status = serializers.BooleanField()

    # created_date = serializers.DateTimeField(read_only=True)
    # updated_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Category
        read_only_fields = ("id",)
        fields = ("id", "name", "status")


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Comments
        read_only_fields = (
            "id",
            "author",
            "is_approved",
            "created_date",
            "updated_date",
        )
        fields = (
            "id",
            "content",
            "author",
            "post",
            "is_approved",
            "created_date",
            "updated_date",
        )

    def create(self, validated_data):
        validated_data["author"] = UserProfile.objects.get(
            user__id=self.context.get("request").user.id
        )
        return super().create(validated_data)


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentsReplies
        read_only_fields = ("id", "author", "created_date", "updated_date")
        fields = ("id", "content", "author", "comment", "created_date", "updated_date")

    def validate(self, attrs):
        request = self.context.get("request")
        comment = attrs.get("comment")

        profile = UserProfile.objects.get(user=request.user)

        if comment and comment.post.author != profile.user:
            raise serializers.ValidationError(
                "شما نویسنده پست اصلی نیستید و نمی‌توانید به کامنت‌های آن پاسخ دهید."
            )

        return attrs

    def create(self, validated_data):
        validated_data["author"] = UserProfile.objects.get(
            user__id=self.context.get("request").user.id
        )
        return super().create(validated_data)


class CommentVerifySerializer(serializers.Serializer):
    comment_pk = serializers.UUIDField(required=True)

    def validate(self, attrs):
        request = self.context.get("request")
        comment_pk = attrs.get("comment_pk")

        profile = UserProfile.objects.get(user=request.user)
        comment = get_object_or_404(
            Comments,
            pk=comment_pk,
        )

        if comment_pk and comment.post.author != profile:
            raise serializers.ValidationError(
                "فقط نویسنده پست میتواند کامنت را تایید کند"
            )

        return attrs
