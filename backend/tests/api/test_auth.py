from starlette import status

from users.models import User


def test_register(app_client):
    response = app_client.post(
        "/users/auth/register/",
        json={
            "email": "test@smallcalorie.com",
            "nickname": "test",
            "password": "Password123!",
            "first_name": "First",
            "last_name": "Last",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    created_user_id = response_data["id"]
    created_user: User = User.get_or_none(id=created_user_id)
    assert all(
        (
            created_user.id == response_data["id"],
            created_user.created_at.isoformat() == response_data["created_at"],
            created_user.first_name == response_data["first_name"] == "First",
            created_user.last_name == response_data["last_name"] == "Last",
            created_user.email == response_data["email"] == "test@smallcalorie.com",
            created_user.nickname == response_data["nickname"] == "test",
        )
    )


def test_unregistered_user_cannot_login(app_client):
    response = app_client.post(
        "/users/auth/login/",
        json={"login": "nonexistent@mail.com", "password": "Password123!"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_invalid_email(app_client):
    response = app_client.post(
        "/users/auth/register/",
        json={
            "email": "XD",
            "nickname": "test",
            "password": "Password123!",
            "first_name": "First",
            "last_name": "Last",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
