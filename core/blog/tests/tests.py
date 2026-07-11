import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from account.models import User, UserProfile
from blog.models import Category, Posts


# Fixtures
@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user():
    user_obj = User.objects.create_user(
        email="test@test.com", password="Mn00137400", is_verified=True
    )
    profile_obj = UserProfile.objects.create(
        user=user_obj, first_name="tester", last_name="tester"
    )
    return profile_obj


@pytest.fixture
def test_category():
    cat_name = ["Funny", "Action", "Science", "Auto", "Industry", "Fashion"]

    for i in range(len(cat_name)):
        Category.objects.create(name=cat_name[i], status=True)
    return Category.objects.all()


@pytest.fixture
def test_post(test_category,
              test_user):
    for i in range(1, 5):
        cat = test_category.order_by("?").first()
        Posts.objects.create(
            title=f"post-{i}",
            author=test_user,
            content=f"test text{i}...",
            category=cat,
            slug=f"post-{i}-{cat}",
            status=True,
        )

    return Posts.objects.all()


# Tests
@pytest.mark.django_db
class TestBlog:
    #  Get Post List
    def test_blog_get_post_valid_data(self,
                                      api_client,
                                      test_user):
        url = reverse("blog:api-v1:post-list")
        params = {"page": 1, "page_size": 1}
        posts = api_client.get(url, params)
        assert posts.status_code == 200

    def test_blog_get_post_invalid_page(self,
                                        api_client,
                                        test_user):
        url = reverse("blog:api-v1:post-list")
        params = {"page": 10, "page_size": 10}
        posts = api_client.get(url, params)
        assert posts.status_code == 404

    # Get Post Filter
    def test_blog_get_post_valid_filter(self,
                                        api_client,
                                        test_user,
                                        test_category):
        url = reverse("blog:api-v1:post-list")
        params = {
            "page": 1,
            "page_size": 1,
            "author": str(test_user.id),
            "status": "True",
            "category": str(test_category.first().id),
            "ordering": "-created_date",
        }
        posts = api_client.get(url, params)
        assert posts.status_code == 200

    def test_blog_get_post_invalid_filter(self,
                                          api_client,
                                          test_user,
                                          test_category):
        url = reverse("blog:api-v1:post-list")
        params = {
            "page": 1,
            "page_size": 1,
            "author": str(1234),
            "status": "True",
            "category": str(test_category.first().id),
            "ordering": "-created_date",
        }
        posts = api_client.get(url, params)
        assert posts.status_code == 400

    # Create Posts
    def test_blog_create_post_without_login(self,
                                            api_client,
                                            test_user,
                                            test_category):
        url = reverse("blog:api-v1:post-list")
        params = {
            "title": "test1",
            "content": "test text",
            "author": str(test_user.id),
            "category": str(test_category.first().id),
            "slug": f"test1_{str(test_category.first().id)}",
        }
        posts = api_client.post(url, params)
        assert posts.status_code == 401

    def test_blog_create_post_with_login(self,
                                         api_client,
                                         test_user,
                                         test_category):
        url = reverse("blog:api-v1:post-list")
        api_client.login(email=test_user.user.email, password="Mn00137400")

        params = {
            "title": "test1",
            "content": "test text",
            "author": str(test_user.id),
            "category": str(test_category.first().id),
            "slug": f"test1_{str(test_category.first().name)}",
        }

        posts = api_client.post(url, params)
        assert posts.status_code == 201

    # Update Posts
    def test_blog_put_post_without_login(
            self,
            api_client,
            test_user,
            test_category,
            test_post
    ):
        url = reverse(
            "blog:api-v1:post-detail", kwargs={"pk": str(test_post.first().id)}
        )

        params = {
            "title": "test (updated)",
            "content": "test text (updated)",
            "author": str(test_user.id),
            "category": str(test_category.first().id),
            "slug": f"test1_{str(test_category.first().name)}",
        }

        put = api_client.put(url, params)
        assert put.status_code == 401

    def test_blog_put_post_with_login(
            self,
            api_client,
            test_user,
            test_category,
            test_post
    ):
        url = reverse(
            "blog:api-v1:post-detail", kwargs={"pk": str(test_post.first().id)}
        )
        api_client.login(email=test_user.user.email, password="Mn00137400")

        params = {
            "title": "test (updated)",
            "content": "test text (updated)",
            "author": str(test_user.id),
            "category": str(test_category.first().id),
            "slug": f"test1_{str(test_category.first().name)}",
        }

        put = api_client.put(url, params)
        assert put.status_code == 200

    def test_blog_patch_post_without_login(
            self,
            api_client,
            test_user,
            test_category,
            test_post
    ):
        url = reverse(
            "blog:api-v1:post-detail", kwargs={"pk": str(test_post.first().id)}
        )

        params = {
            "title": "test (updated)",
            "content": "test text (updated)",
        }

        patch = api_client.patch(url, params)
        assert patch.status_code == 401

    def test_blog_patch_post_with_login(
            self,
            api_client,
            test_user,
            test_category,
            test_post
    ):
        url = reverse(
            "blog:api-v1:post-detail", kwargs={"pk": str(test_post.first().id)}
        )
        api_client.login(email=test_user.user.email, password="Mn00137400")

        params = {
            "title": "test (updated)",
            "content": "test text (updated)",
        }

        patch = api_client.patch(url, params)
        assert patch.status_code == 200

    # Delete Posts
    def test_blog_delete_post_without_login(
            self,
            api_client,
            test_user,
            test_category,
            test_post
    ):
        url = reverse(
            "blog:api-v1:post-detail", kwargs={"pk": str(test_post.first().id)}
        )
        delete = api_client.delete(url)
        assert delete.status_code == 401

    def test_blog_delete_post_with_login(
            self,
            api_client,
            test_user,
            test_category,
            test_post
    ):
        url = reverse(
            "blog:api-v1:post-detail", kwargs={"pk": str(test_post.first().id)}
        )
        api_client.login(email=test_user.user.email, password="Mn00137400")
        delete = api_client.delete(url)
        assert delete.status_code == 204
