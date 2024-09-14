from fastapi import APIRouter, Depends, HTTPException, status
from repository.user_repository import UserRepository
from api.schemas.v1.users_schema import UserRequest, UserResponse
import logging
import api.ioc as ioc
from commands.add_user_command import AddUserCommand

router = APIRouter(prefix="/v1/users", tags=["Users"])
logger = logging.getLogger(__name__)


@router.post("", status_code=status.HTTP_200_OK, response_model=UserResponse)
def add_user(
    request: UserRequest,
    add_user_command: AddUserCommand = Depends(ioc.add_user_command),
) -> UserResponse:
    user = add_user_command.run(request.to_command_request())
    return UserResponse.from_user(user)


@router.get("", status_code=status.HTTP_200_OK, response_model=list[UserResponse])
def list_users(
    user_repository: UserRepository = Depends(ioc.user_repository),
) -> list[UserResponse]:
    users = user_repository.list_users()
    return [UserResponse.from_user(user) for user in users]


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user(
    id: int,
    user_repository: UserRepository = Depends(ioc.user_repository),
) -> UserResponse:
    user = user_repository.get_user(id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    return UserResponse.from_user(user)
