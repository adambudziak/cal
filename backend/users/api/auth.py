from datetime import datetime

from email_validator import validate_email
from fastapi import APIRouter, HTTPException
from fastapi import Response
from pydantic import validator
from starlette import status
from passlib.hash import bcrypt

from core.schemas import BaseSchema
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

    @validator('email')
    def validate_email_format(cls, value: str):
        validate_email(value, check_deliverability=False)  # TODO(adambudziak) check should be disabled only for tests.
        return value

    @validator('nickname')
    def validate_nickname_format(cls, value: str):
        if '@' in value:
            raise ValueError('at_sign')
        return value

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
def register(user_form: UserRegistrationData, response: Response):
    if User.filter(email=user_form.email).exists():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='email_conflict')

    if User.filter(nickname=user_form.nickname):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='nickname_conflict')

    response.status_code = status.HTTP_201_CREATED
    return user_form.to_orm().save()


def get_user_by_login(login: str):
    return User.get_or_none((User.email == login) | (User.nickname == login))


@router.post("/login/", response_model=UserResponse)
def login(data: UserLoginData):
    user = get_user_by_login(data.login)
    auth_exc = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not_found")
    if not user:
        raise auth_exc

    if not bcrypt.verify(data.password, user.password):
        raise auth_exc

    return user
