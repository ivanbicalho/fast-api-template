from fastapi import APIRouter, Depends, HTTPException, status
from repository.todo_repository import TodoRepository
from repository.user_repository import UserRepository
from api.schemas.v1.todo_schema import TodoListRequest, TodoListResponse, TodoItemRequest, TodoItemResponse
import logging
import api.ioc as ioc
from use_cases.add_user_use_case import AddUserUseCase

router = APIRouter(prefix="/v1/todo", tags=["ToDo"])
logger = logging.getLogger(__name__)


@router.post("/list", status_code=status.HTTP_200_OK, response_model=TodoListResponse)
def add_todo_list(
    request: TodoListRequest,
    todo_repository: TodoRepository = Depends(ioc.todo_repository),
) -> TodoListResponse:
    todo_list = todo_repository.upsert_list(request.to_todo_list())
    return TodoListResponse.from_todo_list(todo_list)


@router.post("/list/{id}", status_code=status.HTTP_200_OK, response_model=TodoItemResponse)
def add_todo_item(
    id: int,
    request: TodoItemRequest,
    todo_repository: TodoRepository = Depends(ioc.todo_repository),
) -> TodoItemResponse:
    todo_item = todo_repository.upsert_item(request.to_todo_item(list_id=id))
    return TodoItemResponse.from_todo_item(todo_item)


@router.get("/list/{id}", status_code=status.HTTP_200_OK, response_model=TodoListResponse)
def get_todo_list(
    id: int,
    todo_repository: TodoRepository = Depends(ioc.todo_repository),
) -> TodoListResponse:
    todo_list = todo_repository.get_list(id)
    if not todo_list:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "List not found")

    return [TodoListResponse.from_todo_list(todo_list)]
