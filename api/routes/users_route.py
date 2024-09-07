from fastapi import APIRouter, Depends, status
from services.todo_service import TodoService
from api.ioc import IoC
from services.user_service import UserService
from api.schemas.users_schema import InitRequest, UserResponse
import logging

router = APIRouter(prefix="/users", tags=["Users"])
logger = logging.getLogger(__name__)


@router.post("/init", status_code=status.HTTP_200_OK, response_model=UserResponse)
def init(
    request: InitRequest,
    user_service: UserService = Depends(IoC.user_service),
    todo_service: TodoService = Depends(IoC.todo_service),
) -> UserResponse:
    user = user_service.add(request.to_add_user_request())
    todo_service.create_todo_list(user, request.default_list_name)
    return UserResponse.from_user(user)
