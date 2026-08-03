from uuid import uuid4

import pytest
from account.models import UserProfile
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from blog.models import Category, Comments, CommentsReplies, Posts

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user(db):
    user = User.objects.create_user(
        email="test@test.com",
        password="Mn00137400",
        is_verified=True,
    )
    UserProfile.objects.create(
        user=user,
        first_name="tester",
        last_name="tester",
    )
    return user


@pytest.fixture
def another_user(db):
    user = User.objects.create_user(
        email="another@example.com",
        password="password123",
        is_verified=True,
    )
    UserProfile.objects.create(
        user=user,
        first_name="another",
        last_name="user",
    )
    return user


@pytest.fixture
def inactive_user(db):
    user = User.objects.create_user(
        email="inactive@example.com",
        password="password123",
        is_verified=True,
        is_active=False,
    )
    UserProfile.objects.create(
        user=user,
        first_name="inactive",
        last_name="user",
    )
    return user


@pytest.fixture
def test_category(db):
    return Category.objects.create(name="Funny", status=True)


@pytest.fixture
def another_category(db):
    return Category.objects.create(name="Science", status=True)


@pytest.fixture
def test_post(db, test_user, test_category):
    return Posts.objects.create(
        title="test post",
        author=test_user.userprofile,
        content="test content",
        category=test_category,
        slug="test-post",
        status=True,
    )


@pytest.fixture
def another_post(db, another_user, another_category):
    return Posts.objects.create(
        title="another post",
        author=another_user.userprofile,
        content="another content",
        category=another_category,
        slug="another-post",
        status=True,
    )


@pytest.fixture
def comment(db, test_post, test_user):
    return Comments.objects.create(
        post=test_post,
        author=test_user.userprofile,
        content="a comment",
        is_approved=False,
    )


@pytest.fixture
def approved_comment(db, comment):
    comment.is_approved = True
    comment.save(update_fields=["is_approved"])
    return comment


@pytest.fixture
def comment_of_another_post(db, another_post, another_user):
    return Comments.objects.create(
        post=another_post,
        author=another_user.userprofile,
        content="comment of another post",
        is_approved=True,
    )


@pytest.fixture
def reply(db, approved_comment, test_user):
    return CommentsReplies.objects.create(
        comment=approved_comment,
        author=test_user.userprofile,
        content="a reply",
    )


@pytest.fixture
def reply_of_unapproved_comment(db, comment, test_user):
    return CommentsReplies.objects.create(
        comment=comment,
        author=test_user.userprofile,
        content="reply of unapproved comment",
    )


# Tests
@pytest.mark.django_db
class TestBlog:
    def test_blog_get_post_valid_data(self, api_client, test_user, test_post):
        api_client.force_authenticate(user=test_user)
        response = api_client.get(reverse("blog:api-v1:post-list"), {"page": 1})
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data

    def test_blog_get_post_invalid_page(self, api_client, test_user):
        api_client.force_authenticate(user=test_user)
        response = api_client.get(reverse("blog:api-v1:post-list"), {"page": 999})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_blog_get_post_valid_filter(self, api_client, test_user, test_post, test_category):
        api_client.force_authenticate(user=test_user)
        response = api_client.get(
            reverse("blog:api-v1:post-list"),
            {
                "author": str(test_user.userprofile.pk),
                "status": "True",
                "category": str(test_category.pk),
                "ordering": "-created_date",
            },
        )
        assert response.status_code == status.HTTP_200_OK

    def test_blog_get_post_invalid_filter(self, api_client, test_user):
        api_client.force_authenticate(user=test_user)
        response = api_client.get(
            reverse("blog:api-v1:post-list"),
            {"author": "not-a-valid-pk"},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_blog_create_post_without_login(self, api_client, test_category):
        payload = {
            "title": "test1",
            "content": "test text",
            "author": "1",
            "category": str(test_category.pk),
            "slug": "test1",
        }
        response = api_client.post(reverse("blog:api-v1:post-list"), payload, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_blog_create_post_with_login(self, api_client, test_user, test_category):
        api_client.force_authenticate(user=test_user)
        payload = {
            "title": "test1",
            "content": "test text",
            "category": str(test_category.pk),
            "slug": "test1",
        }
        response = api_client.post(reverse("blog:api-v1:post-list"), payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_blog_put_post_without_login(self, api_client, test_post, test_category):
        payload = {
            "title": "updated",
            "content": "updated content",
            "author": str(test_post.author.pk),
            "category": str(test_category.pk),
            "slug": "updated-slug",
        }
        response = api_client.put(
            reverse("blog:api-v1:post-detail", kwargs={"pk": test_post.pk}),
            payload,
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_blog_put_post_with_login(self, api_client, test_user, test_post, test_category):
        api_client.force_authenticate(user=test_user)
        payload = {
            "title": "updated",
            "content": "updated content",
            "author": str(test_post.author.pk),
            "category": str(test_category.pk),
            "slug": "updated-slug",
        }
        response = api_client.put(
            reverse("blog:api-v1:post-detail", kwargs={"pk": test_post.pk}),
            payload,
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_blog_patch_post_without_login(self, api_client, test_post):
        payload = {"title": "updated"}
        response = api_client.patch(
            reverse("blog:api-v1:post-detail", kwargs={"pk": test_post.pk}),
            payload,
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_blog_patch_post_with_login(self, api_client, test_user, test_post):
        api_client.force_authenticate(user=test_user)
        payload = {"title": "updated"}
        response = api_client.patch(
            reverse("blog:api-v1:post-detail", kwargs={"pk": test_post.pk}),
            payload,
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_blog_delete_post_without_login(self, api_client, test_post):
        response = api_client.delete(
            reverse("blog:api-v1:post-detail", kwargs={"pk": test_post.pk})
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_blog_delete_post_with_login(self, api_client, test_user, test_post):
        api_client.force_authenticate(user=test_user)
        response = api_client.delete(
            reverse("blog:api-v1:post-detail", kwargs={"pk": test_post.pk})
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT


# @pytest.mark.django_db
# class TestCategoryApi:
#     def test_list_is_public(self, api_client, test_category):
#         response = api_client.get(reverse("category-list"))
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data["results"][0]["id"] == test_category.pk
#
#     def test_create_requires_authentication(self, api_client):
#         payload = {"name": "Technology", "status": True}
#         response = api_client.post(reverse("category-list"), payload, format="json")
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#
#     def test_authenticated_user_can_create_category(self, api_client, test_user):
#         api_client.force_authenticate(user=test_user)
#         payload = {"name": "Technology", "status": True}
#         response = api_client.post(reverse("category-list"), payload, format="json")
#         assert response.status_code == status.HTTP_201_CREATED
#
#     def test_category_id_is_read_only(self, api_client, test_user, test_category):
#         api_client.force_authenticate(user=test_user)
#         payload = {
#             "id": str(uuid4()),
#             "name": "Updated",
#             "status": True,
#         }
#         response = api_client.put(
#             reverse("category-detail", kwargs={"pk": test_category.pk}),
#             payload,
#             format="json",
#         )
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data["id"] == test_category.pk
#         assert response.data["name"] == "Updated"
#
#     def test_update_category_requires_authentication(self, api_client, test_category):
#         payload = {"name": "Updated", "status": True}
#         response = api_client.patch(
#             reverse("category-detail", kwargs={"pk": test_category.pk}),
#             payload,
#             format="json",
#         )
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestCommentApi:
    def test_create_comment_requires_authentication(self, api_client, test_post):
        payload = {"post": str(test_post.pk), "content": "A comment"}
        response = api_client.post(reverse("blog:api-v1:comment-list"), payload, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authenticated_user_can_create_comment(self, api_client, test_user, test_post):
        api_client.force_authenticate(user=test_user)
        payload = {"post": str(test_post.pk), "content": "A comment"}
        response = api_client.post(reverse("blog:api-v1:comment-list"), payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_client_cannot_set_comment_author(self, api_client, test_user, another_user, test_post):
        api_client.force_authenticate(user=test_user)
        payload = {
            "post": str(test_post.pk),
            "content": "A comment",
            "author": str(another_user.userprofile.pk),
        }
        response = api_client.post(reverse("blog:api-v1:comment-list"), payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_non_owner_cannot_update_comment(self, api_client, another_user, comment):
        api_client.force_authenticate(user=another_user)
        payload = {"content": "updated"}
        response = api_client.patch(
            reverse("blog:api-v1:comment-detail", kwargs={"pk": comment.pk}),
            payload,
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_non_owner_cannot_delete_comment(self, api_client, another_user, comment):
        api_client.force_authenticate(user=another_user)
        response = api_client.delete(
            reverse("blog:api-v1:comment-detail", kwargs={"pk": comment.pk})
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_comment_detail_methods_are_disabled(self, api_client, comment):
        response = api_client.get(reverse("blog:api-v1:comment-detail", kwargs={"pk": comment.pk}))
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
class TestCommentVerifyApi:
    def test_unauthenticated_user_cannot_verify_comment(self, api_client, comment):
        payload = {"comment_pk": str(comment.pk)}
        response = api_client.post(reverse("blog:api-v1:comment-verify"), payload, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_post_owner_can_verify_comment(self, api_client, test_user, comment):
        api_client.force_authenticate(user=test_user)
        payload = {"comment_pk": str(comment.pk)}
        response = api_client.post(reverse("blog:api-v1:comment-verify"), payload, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_non_post_owner_cannot_verify_comment(self, api_client, another_user, comment):
        api_client.force_authenticate(user=another_user)
        payload = {"comment_pk": str(comment.pk)}
        response = api_client.post(reverse("blog:api-v1:comment-verify"), payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_verify_nonexistent_comment_returns_error(self, api_client, test_user):
        api_client.force_authenticate(user=test_user)
        payload = {"comment_pk": str(uuid4())}
        response = api_client.post(reverse("blog:api-v1:comment-verify"), payload, format="json")
        assert response.status_code in {status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND}

    def test_verify_comment_only_accepts_post(self, api_client, comment):
        api_client.force_login(user=comment.author.user)
        payload = {"comment_pk": comment.pk}
        response = api_client.get(reverse("blog:api-v1:comment-verify"), payload)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
class TestPostCommentApi:
    def test_only_approved_comments_are_returned(self, api_client, approved_comment):
        response = api_client.get(reverse("blog:api-v1:post-comments-list", kwargs={"post_pk": approved_comment.post.pk}))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) >= 1

    def test_comments_of_another_post_are_not_returned(self, api_client, approved_comment, comment_of_another_post):
        response = api_client.get(reverse("blog:api-v1:post-comments-list", kwargs={"post_pk": approved_comment.post.pk}))
        assert response.status_code == status.HTTP_200_OK
        returned_ids = [item["id"] for item in response.data["results"]]
        assert comment_of_another_post.pk not in returned_ids

    def test_post_comments_are_cached(self, api_client, approved_comment):
        url = reverse("blog:api-v1:post-comments-list", kwargs={"post_pk": approved_comment.post.pk})
        response1 = api_client.get(url)
        response2 = api_client.get(url)
        assert response1.status_code == response2.status_code == status.HTTP_200_OK
        assert response1.data == response2.data
