import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from account.models import User, UserProfile
from functions import generate_token


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
def test_user_unverified():
    user_obj = User.objects.create_user(
        email="test@test.com", password="Mn00137400", is_verified=False
    )
    profile_obj = UserProfile.objects.create(
        user=user_obj, first_name="tester", last_name="tester"
    )
    return profile_obj


@pytest.fixture
def test_token(test_user_verified,
               api_client):
    url = reverse("account:api-v1:auth_token")
    params = {
        "email": test_user_verified.user.email,
        "password": "Mn00137400",
    }
    return api_client.post(url, params).data["token"]


@pytest.fixture
def test_jwt(test_user_verified,
             api_client):
    url = reverse("account:api-v1:token_obtain_pair")
    params = {
        "email": test_user_verified.user.email,
        "password": "Mn00137400",
    }

    return api_client.post(url, params).data


@pytest.fixture
def test_verify_token(test_user_unverified):
    token = generate_token(test_user_unverified.user)
    return token


# Create your tests here.
@pytest.mark.django_db
class TestAccount:
    # Register Tests
    def test_account_signup_valid_data(self,
                                       api_client,
                                       test_user_verified):
        url = reverse("account:api-v1:register_api")
        params = {
            "email": "tester@tester.com",
            "password": "Mn00137400",
            "confirm_password": "Mn00137400",
            "first_name": "tester",
            "last_name": "tester",
            "birth_date": "1995-10-24",
        }

        post = api_client.post(url, params)
        assert post.status_code == 201

    def test_account_signup_invalid_data(self,
                                         api_client,
                                         test_user_verified):
        url = reverse("account:api-v1:register_api")
        params = {
            "email": "tester@tester.com",
            "password": "123",
            "confirm_password": "123",
            "first_name": "tester",
            "last_name": "tester",
            "birth_date": "24-10-1995",
        }

        post = api_client.post(url, params)
        assert post.status_code == 400

    def test_account_signup_invalid_method(self,
                                           api_client,
                                           test_user_verified):
        url = reverse("account:api-v1:register_api")
        params = {
            "email": "tester@tester.com",
            "password": "Mn00137400",
            "confirm_password": "Mn00137400",
            "first_name": "tester",
            "last_name": "tester",
            "birth_date": "1995-10-24",
        }

        post = api_client.get(url, params)
        assert post.status_code == 405

    # Login Token Tests
    def test_account_login_valid_data(self,
                                      api_client,
                                      test_user_verified):
        url = reverse("account:api-v1:auth_token")
        params = {
            "email": test_user_verified.user.email,
            "password": "Mn00137400",
        }
        post = api_client.post(url, params)
        assert (post.status_code == 200) and (post.data["token"])

    def test_account_login_invalid_data(self,
                                        api_client,
                                        test_user_verified):
        url = reverse("account:api-v1:auth_token")
        params = {
            "email": test_user_verified.user.email,
            "password": "123",
        }
        post = api_client.post(url, params)
        assert post.status_code == 400

    def test_account_login_invalid_method(self,
                                          api_client,
                                          test_user_verified):
        url = reverse("account:api-v1:auth_token")
        params = {
            "email": test_user_verified.user.email,
            "password": "Mn00137400",
        }
        post = api_client.get(url, params)
        assert post.status_code == 405

    # Login JWT Tests
    def test_account_login_jwt_valid_data(self,
                                          api_client,
                                          test_user_verified):
        url = reverse("account:api-v1:token_obtain_pair")

        params = {
            "email": test_user_verified.user.email,
            "password": "Mn00137400",
        }

        post = api_client.post(url, params)

        assert (post.status_code == 201 and post.data["access"] and post.data["refresh"])

    def test_account_login_jwt_invalid_data(self,
                                            api_client,
                                            test_user_verified):
        url = reverse("account:api-v1:token_obtain_pair")
        params = {
            "email": test_user_verified.user.email,
            "password": "1234",
        }
        post = api_client.post(url, params)
        assert post.status_code == 401

    # Logout Token Tests
    def test_account_logout_valid_data(self,
                                       api_client,
                                       test_token):
        url = reverse("account:api-v1:discard_token")

        api_client.credentials(HTTP_AUTHORIZATION=f"Token {test_token}")
        post = api_client.post(url)

        assert post.status_code == 204

    def test_account_logout_invalid_data(self,
                                         api_client,
                                         test_token):
        url = reverse("account:api-v1:discard_token")

        api_client.credentials(HTTP_AUTHORIZATION="Token 74516")
        post = api_client.post(url)

        assert post.status_code == 401

    # Account Verify Tests
    def test_account_verify_valid_data(self,
                                       api_client,
                                       test_verify_token):
        host_name = 'https://127.0.0.1:8000'
        verify_url = reverse('account:api-v1:account_verify_jwt')

        verify_url = f"{host_name}{verify_url}?token={test_verify_token}"
        print(verify_url)
        get = api_client.get(verify_url)
        assert get.status_code == 200
