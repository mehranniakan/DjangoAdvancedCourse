import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from ToDoApp.models import Task
from account.models import User, UserProfile


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user_verified():
    user_obj = User.objects.create_user(
        email="test@test.com", password="Mn00137400", is_verified=True
    )
    profile_obj = UserProfile.objects.create(
        user=user_obj, first_name="tester", last_name="tester"
    )
    return profile_obj


@pytest.fixture
def test_token(test_user_verified, api_client):
    url = reverse("account:api-v1:auth_token")
    params = {
        "email": test_user_verified.user.email,
        "password": "Mn00137400",
    }
    return api_client.post(url, params).data["token"]


@pytest.fixture
def test_jwt(test_user_verified, api_client):
    url = reverse("account:api-v1:token_obtain_pair")
    params = {
        "email": test_user_verified.user.email,
        "password": "Mn00137400",
    }

    return api_client.post(url, params).data


@pytest.fixture
def test_tasks(test_user_verified, api_client):
    for i in range(1, 11):
        Task.objects.create(
            user=test_user_verified,
            title=f"Task {i}",
            description=f"Description {i}...",
            status=True,
        )

    return Task.objects


@pytest.mark.django_db
class TestToDOApp:

    def test_todoapp_get_tasks_without_filter(
            self, api_client, test_user_verified, test_token, test_jwt
    ):
        url = reverse("ToDoApp:api-v1:Task-list")

        # With Token
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {test_token}")
        params = {
            "page": 1,
            "page_size": 1,
        }
        get_token = api_client.get(url, params)

        # With JWT
        jwt_token = test_jwt["access"]
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
        get_jwt = api_client.get(url, params)

        assert get_jwt.status_code == 200 and get_token.status_code == 200

    def test_todoapp_get_tasks_with_filter(
            self, api_client, test_user_verified, test_token, test_jwt, test_tasks
    ):
        url = reverse("ToDoApp:api-v1:Task-list")
        params = {
            "page": 1,
            "page_size": 1,
            "search": str(test_tasks.order_by("?").first().title),
            "status": "True",
        }
        jwt_token = test_jwt["access"]
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
        get_jwt = api_client.get(url, params)

        assert get_jwt.status_code == 200

    def test_todoapp_create_task(self, api_client, test_jwt):
        url = reverse("ToDoApp:api-v1:Task-list")
        params = {
            "title": "test1",
            "description": "test1 description",
            "status": "True",
        }
        jwt_token = test_jwt["access"]
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        post = api_client.post(url, params)

        assert post.status_code == 201

    def test_todoapp_update_task(self, test_tasks, api_client, test_jwt):
        url = reverse(
            "ToDoApp:api-v1:Task-detail", kwargs={"pk": test_tasks.first().id}
        )

        params = {
            "title": "new title",
            "description": "new description",
            "status": "True",
        }
        jwt_token = test_jwt["access"]
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        put = api_client.put(url, params)

        assert put.status_code == 200

    def test_todoapp_delete_task(self, test_tasks, api_client, test_jwt):
        url = reverse(
            "ToDoApp:api-v1:Task-detail", kwargs={"pk": test_tasks.first().id}
        )

        jwt_token = test_jwt["access"]
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        put = api_client.delete(url)

        assert put.status_code == 204
