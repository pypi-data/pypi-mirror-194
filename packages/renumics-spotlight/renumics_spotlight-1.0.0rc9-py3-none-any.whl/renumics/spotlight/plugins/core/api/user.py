"""
user api endpoints
"""

from datetime import date
from typing import Optional
from fastapi import APIRouter, Request
from pydantic import BaseModel  # pylint: disable=no-name-in-module

router = APIRouter()

# pylint: disable=too-few-public-methods
class User(BaseModel):
    """
    a User
    """

    user_name: str
    expiration_date: date
    row_limit: Optional[int]
    column_limit: Optional[int]
    has_test_license: bool


@router.get(
    "/", response_model=User, tags=["user"], summary="User Api", operation_id="get_user"
)
async def _(request: Request) -> User:
    """
    user api endpoint
    """

    spotlight_license = request.app.spotlight_license
    return User(
        user_name=spotlight_license.users[0],
        expiration_date=spotlight_license.expiration_date,
        row_limit=spotlight_license.row_limit,
        column_limit=spotlight_license.column_limit,
        has_test_license=spotlight_license.is_test,
    )
