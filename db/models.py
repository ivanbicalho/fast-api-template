from __future__ import annotations
import datetime
from typing import Any
from db.database import Base
from uuid import UUID, uuid4
from sqlalchemy import ForeignKey, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.enum import TodoStatus


def default_updated(context) -> Any:
    # updated and created should be exactly the same when inserting a new record
    # so it returns the created date to be used as a default value for updated date
    return context.get_current_parameters()["created"]


class BaseModel(Base):
    __abstract__ = True
    created: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    updated: Mapped[datetime.datetime] = mapped_column(default=default_updated, onupdate=datetime.datetime.now)


class UserModel(BaseModel):
    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}

    def __str__(self) -> str:
        return f"User: ID={self.id}, Name={self.name}"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    first_name: Mapped[str] = mapped_column(String(200))
    last_name: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(200))


class TodoListModel(BaseModel):
    __tablename__ = "todo_list"
    __table_args__ = {"extend_existing": True}

    def __str__(self) -> str:
        return f"List: ID={self.id}"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    status: Mapped[TodoStatus] = mapped_column(Enum(TodoStatus), default=TodoStatus.PENDING)
    # status: Mapped[TodoStatus] = mapped_column(
    #     Enum(TodoStatus, native_enum=False, values_callable=lambda e: [x.value for x in e]),
    # )
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[UserModel] = relationship()
    items: Mapped[list[TodoItemModel]] = relationship(back_populates="list")


class TodoItemModel(BaseModel):
    __tablename__ = "todo_item"
    __table_args__ = {"extend_existing": True}

    def __str__(self) -> str:
        return f"Item: ID={self.id}"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    description: Mapped[str] = mapped_column(String(200))
    status: Mapped[int] = mapped_column(Enum(TodoStatus), default=TodoStatus.PENDING)

    list_id: Mapped[int] = mapped_column(ForeignKey("todo_list.id"))
    list: Mapped[TodoListModel] = relationship()


class AuditModel(Base):
    __tablename__ = "auditing"
    __table_args__ = {"extend_existing": True}

    def __str__(self) -> str:
        return f"Auditing: ID={self.id}"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4)
    created: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now, index=True)
    operation: Mapped[str] = mapped_column(String(200))
    message: Mapped[str] = mapped_column(String(500))
