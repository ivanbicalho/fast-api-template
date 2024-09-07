from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from responses import ApiResponse
from services.todo_service import TodoService
from factory import Factory
from services.user_service import UserService
from schemas.users_schema import InitRequest, UserResponse
import logging

router = APIRouter(prefix="/users", tags=["Users"])
logger = logging.getLogger(__name__)


@router.post("/init", status_code=status.HTTP_200_OK, response_model=list[UserResponse])
def init(
    request: InitRequest,
    user_service: UserService = Depends(Factory.user_service),
    todo_service: TodoService = Depends(Factory.todo_service),
) -> JSONResponse:
    user = user_service.add(request.to_add_user_request())
    todo_service.create_todo_list(user, request.default_list_name)
    return ApiResponse.ok(UserResponse.from_user(user))
