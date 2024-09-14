from fastapi import APIRouter, Depends, status
from api.schemas.v1.users_schema import UserResponse
from api.schemas.v2.users_schema import UserRequest
import logging
import api.ioc as ioc
from commands.add_user_command import AddUserCommand

router = APIRouter(prefix="/v2/users", tags=["Users V2"])
logger = logging.getLogger(__name__)


@router.post("", status_code=status.HTTP_200_OK, response_model=UserResponse)
def add_user(
    request: UserRequest,
    add_user_use_case: AddUserCommand = Depends(ioc.add_user_use_case),
) -> UserResponse:
    user = add_user_use_case.run(request.to_service_request())
    return UserResponse.from_user(user)
