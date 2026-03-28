from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Enum as SQLEnum, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.schema import Index, ForeignKey


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="用户ID"
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        comment="用户名",
    )

    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="密码(加密存储)",
    )

    nickname: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="昵称",
    )

    avatar: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        default="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg",
        comment="头像",
    )

    gender: Mapped[Optional[str]] = mapped_column(
        SQLEnum("male", "female", "unknown", name="gender_enum"),
        nullable=True,
        default="unknown",
        comment="性别",
    )

    bio: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        default="这个人很懒，什么也没写",
        comment="个人简介",
    )

    phone: Mapped[Optional[str]] = mapped_column(
        String(20),
        unique=True,
        nullable=True,
        comment="手机号",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        comment="创建时间"
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间"
    )

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, nickname={self.nickname})>"




class UserToken(Base):
    __tablename__ = "user_token"
    __table_args__ = (
        Index('token_UNIQUE', 'token'),
        Index('fk_user_token_user_idx', 'user_id'),
    )
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="令牌ID"
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(User.id),
        nullable=False,
        comment="用户ID",
    )
    token: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="令牌值",
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        comment="过期时间",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(),
        comment="创建时间"
    )
    def __repr__(self):
        return f"<UserToken(id={self.id}, user_id={self.user_id}, token={self.token})>"










