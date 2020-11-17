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
    assert response.status_code == status.HTTP_201_CREATED, response.content
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
    assert response.status_code == status.HTTP_404_NOT_FOUND


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
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_email_must_be_unique(app_client, user: User):
    response = app_client.post(
        "/users/auth/register/",
        json={
            "email": user.email,
            "nickname": "test",
            "password": "Password123!",
            "first_name": "First",
            "last_name": "Last",
        }
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {'detail': 'email_conflict'}


def test_nickname_must_be_unique(app_client, user: User):
    response = app_client.post(
        "/users/auth/register/",
        json={
            "email": "abc@def.com",
            "nickname": user.nickname,
            "password": "Password123!",
            "first_name": "First",
            "last_name": "Last",
        }
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {'detail': 'nickname_conflict'}


def test_nickname_must_contain_only_legal_characters(app_client):
    response = app_client.post(
        "/users/auth/register/",
        json={
            "email": "abc@def.com",
            "nickname": 'nickname@',
            "password": "Password123!",
            "first_name": "First",
            "last_name": "Last",
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert not User.filter(nickname='nickname@')
