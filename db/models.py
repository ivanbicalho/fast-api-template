from __future__ import annotations
import datetime
from db.database import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class BaseModel(Base):
    __abstract__ = True
    created: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    updated: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now, onupdate=datetime.datetime.now)


class UserModel(Base):
    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}

    def __str__(self) -> str:
        return f"User: ID={self.id}, Name={self.name}"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(200))


class TodoListModel(Base):
    __tablename__ = "todo_list"
    __table_args__ = {"extend_existing": True}

    def __str__(self) -> str:
        return f"List: ID={self.id}"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    status: Mapped[int]
    user: Mapped[UserModel] = mapped_column(ForeignKey("user.id"))
    items: Mapped[list[TodoItemModel]] = relationship(back_populates="list")


class TodoItemModel(Base):
    __tablename__ = "todo_item"
    __table_args__ = {"extend_existing": True}

    def __str__(self) -> str:
        return f"Item: ID={self.id}"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    description: Mapped[str] = mapped_column(String(200))
    status: Mapped[int] = mapped_column()

    list: Mapped[TodoListModel] = relationship(back_populates="items")
    # list_id: Mapped[int] = mapped_column(ForeignKey("todo_list.id"))
