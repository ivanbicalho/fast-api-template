from __future__ import annotations
import datetime
from typing import Any
from db.database import Base
from uuid import UUID, uuid4
from sqlalchemy import ForeignKey, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.enum import TodoStatus, AuditOperation


def default_updated(context) -> Any:
    # updated and created should be exactly the same when inserting a new record
    # so it returns the created date to be used as a default value for the updated date
    return context.get_current_parameters()["created"]


class EditableModel(Base):
    __abstract__ = True
    created: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    updated: Mapped[datetime.datetime] = mapped_column(default=default_updated, onupdate=datetime.datetime.now)


class User(EditableModel):
    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}

    def __str__(self) -> str:
        return f"User: ID={self.id}, Name={self.name}"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    first_name: Mapped[str] = mapped_column(String(200))
    last_name: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(200))


class TodoList(EditableModel):
    __tablename__ = "todo_list"
    __table_args__ = {"extend_existing": True}

    def __str__(self) -> str:
        return f"List: ID={self.id}"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    status: Mapped[TodoStatus] = mapped_column(Enum(TodoStatus), default=TodoStatus.PENDING)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship()
    items: Mapped[list[TodoItem]] = relationship(back_populates="list")


class TodoItem(EditableModel):
    __tablename__ = "todo_item"
    __table_args__ = {"extend_existing": True}

    def __str__(self) -> str:
        return f"Item: ID={self.id}"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    description: Mapped[str] = mapped_column(String(200))
    status: Mapped[TodoStatus] = mapped_column(Enum(TodoStatus), default=TodoStatus.PENDING)

    list_id: Mapped[int] = mapped_column(ForeignKey("todo_list.id"))
    list: Mapped[TodoList] = relationship()


class Audit(Base):
    __tablename__ = "auditing"
    __table_args__ = {"extend_existing": True}

    def __str__(self) -> str:
        return f"Auditing: ID={self.id}"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4)
    created: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now, index=True)
    operation: Mapped[AuditOperation] = mapped_column(Enum(AuditOperation))
    message: Mapped[str] = mapped_column(String(500))

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship()
