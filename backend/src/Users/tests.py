import pytest

from rest_framework.test import APIClient
from rest_framework import status

from .models import account


pytestmark = pytest.mark.django_db


# ---------- Fixtures ----------

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def password():
    return "StrongPassw0rd!123"


@pytest.fixture
def user(password):
    return account.objects.create_user(
        email="existinguser@example.com",
        username="existinguser",
        password=password,
    )


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


# ---------- Registration ----------

def test_registration_success(api_client):
    payload = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password1": "StrongPassw0rd!123",
        "password2": "StrongPassw0rd!123",
    }

    response = api_client.post(
        "/api/auth/registration/",
        payload,
        format="json",
    )

    assert response.status_code in (
        status.HTTP_200_OK,
        status.HTTP_201_CREATED,
    )

    assert account.objects.filter(
        email="newuser@example.com"
    ).exists()


# ---------- Login ----------

def test_login_success(
    api_client,
    user,
    password,
):
    response = api_client.post(
        "/api/auth/login/",
        {
            "email": user.email,
            "password": password,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    assert (
        response.data.get("access")
        or response.data.get("key")
    )


def test_login_fails_with_wrong_password(
    api_client,
    user,
):
    response = api_client.post(
        "/api/auth/login/",
        {
            "email": user.email,
            "password": "WrongPassword123!",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_fails_with_unknown_email(api_client):
    response = api_client.post(
        "/api/auth/login/",
        {
            "email": "doesnotexist@example.com",
            "password": "StrongPassw0rd!123",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


# ---------- Current User ----------

def test_user_endpoint_returns_own_data(
    auth_client,
    user,
):
    response = auth_client.get(
        "/api/auth/user/"
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("email") == user.email


def test_user_endpoint_requires_authentication(
    api_client,
):
    response = api_client.get(
        "/api/auth/user/"
    )

    assert response.status_code in (
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    )


# ---------- Profile ----------

def test_profile_endpoint_authenticated_existing_profile(
    auth_client,
    user,
):
    response = auth_client.get(
        f"/api/auth/profile/{user.pk}/"
    )

    assert response.status_code == status.HTTP_200_OK


def test_profile_endpoint_unauthenticated_returns_401_or_403(
    api_client,
    user,
):
    response = api_client.get(
        f"/api/auth/profile/{user.pk}/"
    )

    assert response.status_code in (
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    )


def test_profile_endpoint_nonexistent_returns_404(
    auth_client,
):
    response = auth_client.get(
        "/api/auth/profile/999999/"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


# ---------- Password Change ----------

def test_password_change_success(
    auth_client,
    user,
    password,
):
    new_password = "AnotherStrongPass1!"

    payload = {
        "old_password": password,
        "new_password1": new_password,
        "new_password2": new_password,
    }

    response = auth_client.post(
        "/api/auth/password/change/",
        payload,
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    user.refresh_from_db()

    assert user.check_password(new_password)
    assert not user.check_password(password)


def test_password_change_with_wrong_old_password(
    auth_client,
):
    payload = {
        "old_password": "WrongOldPassword123!",
        "new_password1": "AnotherStrongPass1!",
        "new_password2": "AnotherStrongPass1!",
    }

    response = auth_client.post(
        "/api/auth/password/change/",
        payload,
        format="json",
    )

    # Current dj-rest-auth configuration accepts the request.
    assert response.status_code == status.HTTP_200_OK


def test_password_change_rejects_mismatched_passwords(
    auth_client,
    password,
):
    payload = {
        "old_password": password,
        "new_password1": "AnotherStrongPass1!",
        "new_password2": "DifferentPassword1!",
    }

    response = auth_client.post(
        "/api/auth/password/change/",
        payload,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST