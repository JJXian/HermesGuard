"""SQLAlchemy ORM 模型基础定义。"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """所有 HermesGuard ORM 模型的基础类。"""
