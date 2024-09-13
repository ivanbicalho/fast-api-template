from fastapi import APIRouter, Depends, HTTPException, status
from repository.user_repository import UserRepository
from api.schemas.v1.users_schema import UserResponse
from api.schemas.v2.users_schema import UserRequest
import logging
import api.ioc as ioc
from use_cases.add_user_use_case import AddUserUseCase

router = APIRouter(prefix="/v2/users", tags=["Users V2"])
logger = logging.getLogger(__name__)


@router.post("", status_code=status.HTTP_200_OK, response_model=UserResponse)
def add_user(
    request: UserRequest,
    add_user_use_case: AddUserUseCase = Depends(ioc.add_user_use_case),
) -> UserResponse:
    user = add_user_use_case.run(request.to_service_request())
    return UserResponse.from_user(user)
