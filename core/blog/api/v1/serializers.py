from rest_framework import serializers

from account.models import UserProfile
from blog.models import Posts, Category


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
