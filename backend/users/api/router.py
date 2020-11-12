from fastapi import APIRouter, Depends

from core.database import get_db
from users.api import auth

router = APIRouter()

router.include_router(auth.router, prefix="/auth", dependencies=[Depends(get_db)])
