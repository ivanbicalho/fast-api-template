from fastapi import APIRouter, Depends, HTTPException, status
from commands.add_todo_item_command import AddTodoItemCommand
from commands.add_todo_list_command import AddTodoListCommand
from commands.complete_todo_item_command import CompleteTodoItemCommand, CompleteTodoItemCommandRequest
from commands.exceptions import TodoItemNotFound, TodoListNotFound, UserNotFound
from repository.todo_repository import TodoRepository
from api.schemas.v1.todo_schema import TodoListRequest, TodoListResponse, TodoItemRequest, TodoItemResponse
import logging
import api.ioc as ioc

router = APIRouter(prefix="/v1/todo", tags=["ToDo"])
logger = logging.getLogger(__name__)


@router.post("/list", status_code=status.HTTP_200_OK, response_model=TodoListResponse)
def add_todo_list(
    request: TodoListRequest,
    add_todo_list_command: AddTodoListCommand = Depends(ioc.add_todo_list_command),
) -> TodoListResponse:
    try:
        todo_list = add_todo_list_command.run(request.to_command_request())
        return TodoListResponse.from_todo_list(todo_list)
    except UserNotFound:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "User not found")


@router.post("/list/{id}", status_code=status.HTTP_200_OK, response_model=TodoItemResponse)
def add_todo_item(
    id: int,
    request: TodoItemRequest,
    add_todo_item_command: AddTodoItemCommand = Depends(ioc.add_todo_item_command),
) -> TodoItemResponse:
    try:
        todo_item = add_todo_item_command.run(request.to_command_request(list_id=id))
        return TodoItemResponse.from_todo_item(todo_item)
    except TodoListNotFound:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "List not Found")


@router.get("/list/{id}", status_code=status.HTTP_200_OK, response_model=TodoListResponse)
def get_todo_list(
    id: int,
    todo_repository: TodoRepository = Depends(ioc.todo_repository),
) -> TodoListResponse:
    todo_list = todo_repository.get_list(id)
    if not todo_list:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "List not found")

    return TodoListResponse.from_todo_list(todo_list)


@router.patch("/list/{id}/items/{item_id}", status_code=status.HTTP_200_OK, response_model=TodoItemResponse)
def complete_todo_item(
    id: int,
    item_id: int,
    complete_todo_item_command: CompleteTodoItemCommand = Depends(ioc.complete_todo_item_command),
) -> TodoItemResponse:
    try:
        todo_item = complete_todo_item_command.run(CompleteTodoItemCommandRequest(list_id=id, item_id=item_id))
    except (TodoListNotFound, TodoItemNotFound):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "List or Item not Found")

    return TodoItemResponse.from_todo_item(todo_item)
