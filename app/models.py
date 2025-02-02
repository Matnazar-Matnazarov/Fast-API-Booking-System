from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    BigInteger,
    ForeignKey,
    Float,
    Text,
    Table,
    MetaData,
    DECIMAL,
    UUID,
)
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import func, text
import uuid
from app.database import Base
import pytz
from enum import Enum
from datetime import datetime


class TimestampMixin:
    """Base mixin for timestamp fields"""

    @declared_attr
    def created_at(cls):
        tashkent_tz = pytz.timezone("Asia/Tashkent")
        return Column(DateTime, default=lambda: datetime.now(tashkent_tz))

    @declared_attr
    def updated_at(cls):
        tashkent_tz = pytz.timezone("Asia/Tashkent")
        return Column(
            DateTime,
            default=lambda: datetime.now(tashkent_tz),
            onupdate=lambda: datetime.now(tashkent_tz),
        )


class SoftDeleteMixin:
    """Base mixin for soft delete functionality"""

    is_deleted = Column(Boolean, default=False, nullable=True)
    is_active = Column(Boolean, default=True, nullable=True)


class User(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=255), index=True, nullable=False)
    first_name = Column(String(length=255), index=True, nullable=True)
    last_name = Column(String(length=255), index=True, nullable=True)
    email = Column(String(length=255), unique=True, index=True, nullable=False)
    password = Column(String(length=255), nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    role = Column(String(length=50), nullable=False, default="user")
    products = relationship(
        "Product",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="selectin",
    )
    orders = relationship(
        "Order",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="selectin",
    )

    @validates("email")
    def validate_email(self, key, email):
        if not email:
            raise ValueError("Email cannot be empty")
        return email.lower()

    def __repr__(self):
        return f"<User {self.username}>"


class Product(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "products"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(length=255), index=True, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    token = Column(
        UUID(as_uuid=True), default=uuid.uuid4, nullable=False, unique=True, index=True
    )
    user = relationship("User", back_populates="products")
    orders = relationship("Order", back_populates="product", lazy="selectin")
    order_items = relationship("OrderItem", back_populates="product", lazy="selectin")

    @validates("price")
    def validate_price(self, key, price):
        if price < 0:
            raise ValueError("Price cannot be negative")
        return price

    def __repr__(self):
        return f"<Product {self.name}>"


class OrderStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"
    FAILED = "failed"


class Order(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "orders"

    id = Column(BigInteger, primary_key=True, index=True)
    product_id = Column(
        BigInteger, ForeignKey("products.id", ondelete="CASCADE"), index=True
    )
    product = relationship("Product", back_populates="orders", lazy="selectin")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    user = relationship("User", back_populates="orders", lazy="selectin")
    quantity = Column(Integer, nullable=True)
    total_price = Column(Float, nullable=True)
    status = Column(String, nullable=True, default=OrderStatus.PENDING.value)
    token = Column(
        UUID(as_uuid=True), default=uuid.uuid4, nullable=True, unique=True, index=True
    )
    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self):
        return f"<Order {self.product.name}>"


class OrderItem(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "order_items"

    id = Column(BigInteger, primary_key=True, index=True)
    order_id = Column(
        BigInteger, ForeignKey("orders.id", ondelete="CASCADE"), index=True
    )
    order = relationship("Order", back_populates="items", lazy="selectin")
    product_id = Column(
        BigInteger, ForeignKey("products.id", ondelete="CASCADE"), index=True
    )
    product = relationship("Product", back_populates="order_items", lazy="selectin")
    quantity = Column(Integer, nullable=True)
    price = Column(Float, nullable=True)
    total_price = Column(Float, nullable=True)

    def __repr__(self):
        return f"<OrderItem {self.product.name}>"
