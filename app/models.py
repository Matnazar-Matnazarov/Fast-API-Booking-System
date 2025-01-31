from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.database import Base
from datetime import datetime
import pytz

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=255), index=True, nullable=False)
    first_name = Column(String(length=255), index=True, nullable=True)
    last_name = Column(String(length=255), index=True, nullable=True)
    email = Column(String(length=255), unique=True, index=True, nullable=False)
    password = Column(String(length=255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Tashkent')))
    updated_at = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Tashkent')), onupdate=lambda: datetime.now(pytz.timezone('Asia/Tashkent')))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
