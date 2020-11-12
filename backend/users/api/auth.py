from datetime import datetime

from fastapi import APIRouter, HTTPException
from fastapi import Response
from starlette import status
from passlib.hash import bcrypt

from core.schemas import BaseSchema
from core.utils import get_or_404
from users.models import User

router = APIRouter()


def hash_password(raw_password: str) -> str:
    return bcrypt.hash(raw_password)


class UserRegistrationData(BaseSchema):
    email: str
    nickname: str
    password: str
    first_name: str
    last_name: str

    def to_orm(self):
        data = self.dict()
        data["password"] = hash_password(data["password"])
        return User(**data)


class UserLoginData(BaseSchema):
    login: str
    password: str


class UserResponse(BaseSchema):
    id: int
    created_at: datetime
    first_name: str
    last_name: str
    email: str
    nickname: str


@router.post("/register/", response_model=UserResponse)
def register(data: UserRegistrationData, response: Response):
    response.status_code = status.HTTP_201_CREATED
    return data.to_orm().save()


def get_user_by_login(login: str):
    return User.get_or_none((User.email == login) | (User.nickname == login))


@router.post("/login/", response_model=UserResponse)
def login(data: UserLoginData):
    user = get_user_by_login(data.login)
    auth_exc = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid")
    if not user:
        # Note: we return 400 instead of 404 to prevent an adversary from obtaining info
        #       about which logins are in use.
        raise auth_exc

    if not bcrypt.verify(data.password, user.password):
        raise auth_exc

    return user
