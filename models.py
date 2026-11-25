from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from datetime import datetime 

class User(Base):
    __tablename__ = "users"
    id: Mapped[int]= mapped_column(primary_key=True)
    name: Mapped[str]= mapped_column(String(100))
    username: Mapped[str]= mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str]= mapped_column(String(255))
    role: Mapped[str]=mapped_column(String(20), default="user", server_default="user")
    posts: Mapped[list["Post"]]= relationship(back_populates="owner")
    
class Post(Base):
    __tablename__ ="posts"
    id: Mapped[int]= mapped_column(primary_key=True)
    title: Mapped[str]= mapped_column(String(255))
    user_id: Mapped[int]= mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"]=relationship(back_populates="posts")
    
class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id: Mapped[int]= mapped_column(primary_key=True)
    jti: Mapped[str]= mapped_column(String(64), unique=True, index=True)
    user_id: Mapped[int]= mapped_column(ForeignKey("users.id"))
    expires_at: Mapped[datetime]=mapped_column(DateTime(timezone=True))
    revoked: Mapped[bool]= mapped_column(default=False)
    
    
    