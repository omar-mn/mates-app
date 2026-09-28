import pytest

from django.utils import timezone
from rest_framework.test import APIClient

from .models import Room, MemberShip, JoinRequest
from Users.models import account


# ---------- Fixtures ----------

@pytest.fixture
def user(db):
    return account.objects.create_user(
        email="alice@example.com",
        username="alice",
        password="pass1234",
    )


@pytest.fixture
def other_user(db):
    return account.objects.create_user(
        email="bob@example.com",
        username="bob",
        password="pass1234",
    )


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def other_auth_client(other_user):
    client = APIClient()
    client.force_authenticate(user=other_user)
    return client


@pytest.fixture
def room(user):
    room = Room.objects.create(
        name="General",
        owner=user,
        private=False,
    )

    MemberShip.objects.create(
        user=user,
        room=room,
        role="owner",
    )

    return room


@pytest.fixture
def private_room(user):
    room = Room.objects.create(
        name="Private Room",
        owner=user,
        private=True,
    )

    MemberShip.objects.create(
        user=user,
        room=room,
        role="owner",
    )

    return room


# ---------- Tests ----------

def test_authenticated_user_can_list_rooms(auth_client, room):
    response = auth_client.get(
        "/api/rooms/"
    )

    assert response.status_code == 200


def test_authenticated_user_can_create_room(auth_client):
    payload = {
        "name": "New Room",
        "private": False,
    }

    response = auth_client.post(
        "/api/rooms/create/",
        payload,
        format="json",
    )

    assert response.status_code in (200, 201)
    assert Room.objects.filter(
        name="New Room"
    ).exists()


def test_existing_room_detail_returns_200(
    auth_client,
    room,
):
    response = auth_client.get(
        f"/api/rooms/room/{room.pk}/"
    )

    assert response.status_code == 200


def test_missing_room_detail_returns_200_with_error(
    auth_client,
):
    response = auth_client.get(
        "/api/rooms/room/99999/"
    )

    # Current GetRoom view returns HTTP 200
    # with an error message instead of HTTP 404.
    assert response.status_code == 200
    assert "error" in response.data


def test_user_can_join_public_room(
    other_auth_client,
    other_user,
    room,
):
    response = other_auth_client.post(
        f"/api/rooms/join/{room.pk}/"
    )

    assert response.status_code == 200

    assert MemberShip.objects.filter(
        user=other_user,
        room=room,
    ).exists()


def test_user_can_rejoin_public_room_after_leaving(
    other_auth_client,
    other_user,
    room,
):
    membership = MemberShip.objects.create(
        user=other_user,
        room=room,
        role="member",
        leftDate=timezone.now(),
    )

    response = other_auth_client.post(
        f"/api/rooms/join/{room.pk}/"
    )

    assert response.status_code == 200

    membership.refresh_from_db()

    assert membership.leftDate is None


def test_member_can_leave_room(
    other_auth_client,
    other_user,
    room,
):
    MemberShip.objects.create(
        user=other_user,
        room=room,
        role="member",
    )

    response = other_auth_client.post(
        f"/api/rooms/leave/{room.pk}/"
    )

    assert response.status_code == 200

    membership = MemberShip.objects.get(
        user=other_user,
        room=room,
    )

    assert membership.leftDate is not None


def test_owner_cannot_leave_room(
    auth_client,
    room,
):
    response = auth_client.post(
        f"/api/rooms/leave/{room.pk}/"
    )

    assert response.status_code in (401, 403)


def test_authenticated_user_can_get_joined_rooms(
    auth_client,
    room,
    user,
):
    response = auth_client.get(
        "/api/rooms/joinedrooms/"
    )

    assert response.status_code == 200


def test_authenticated_user_can_get_own_pending_requests(
    other_auth_client,
    other_user,
    room,
):
    JoinRequest.objects.create(
        user=other_user,
        room=room,
        state="pending",
    )

    response = other_auth_client.get(
        "/api/rooms/pendingrequsts/"
    )

    assert response.status_code == 200


def test_room_owner_can_get_pending_requests(
    auth_client,
    other_user,
    room,
):
    JoinRequest.objects.create(
        user=other_user,
        room=room,
        state="pending",
    )

    response = auth_client.get(
        f"/api/rooms/pendingrequsts/{room.pk}/"
    )

    assert response.status_code == 200


def test_member_cannot_get_pending_requests(
    other_auth_client,
    other_user,
    room,
    user,
):
    MemberShip.objects.create(
        user=other_user,
        room=room,
        role="member",
    )

    JoinRequest.objects.create(
        user=user,
        room=room,
        state="pending",
    )

    response = other_auth_client.get(
        f"/api/rooms/pendingrequsts/{room.pk}/"
    )

    assert response.status_code in (401, 403)


def test_user_can_request_to_join_private_room(
    other_auth_client,
    other_user,
    private_room,
):
    response = other_auth_client.post(
        f"/api/rooms/join/{private_room.pk}/"
    )

    assert response.status_code == 200

    assert JoinRequest.objects.filter(
        user=other_user,
        room=private_room,
        state="pending",
    ).exists()


def test_duplicate_private_room_request_is_not_created(
    other_auth_client,
    other_user,
    private_room,
):
    JoinRequest.objects.create(
        user=other_user,
        room=private_room,
        state="pending",
    )

    response = other_auth_client.post(
        f"/api/rooms/join/{private_room.pk}/"
    )

    assert response.status_code == 200

    assert JoinRequest.objects.filter(
        user=other_user,
        room=private_room,
        state="pending",
    ).count() == 1