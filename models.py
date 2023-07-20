from enum import Enum
import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, BLOB
from sqlalchemy.orm import relationship

from database.database import Base


class UserRole(str, Enum):
    SUPPER_ADMIN = 'supper_admin'
    ADMIN = 'admin'
    USER = 'user'


class OrderStatus(str, Enum):
    PENDING = 'pending'
    DELIVERING = 'delivering'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    user_role = Column(String(255), default=UserRole.USER, nullable=False)
    is_active = Column(String(255), default=True, nullable=True)
    refresh_token = Column(String(255), nullable=True)

    user_information = relationship("UserInformation", back_populates="user", uselist=False)
    carts = relationship("Cart", back_populates="user", uselist=False)
    orders = relationship("Order", back_populates="user", uselist=True)


class UserInformation(Base):
    __tablename__ = 'user_information'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=True)
    phone_number = Column(String(255), default="", nullable=True)
    address = Column(String(255), default="", nullable=True)
    dob = Column(String(255), default="", nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='user_information')
    created_at = Column(String(255), default=datetime.datetime.utcnow())


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), default="", nullable=True)

    products = relationship('Product', back_populates='category', uselist=True)
    created_at = Column(String(255), default=datetime.datetime.utcnow())
    updated_at = Column(String(255), default=datetime.datetime.utcnow())


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))

    images = relationship('Image', back_populates='product', uselist=True)
    category = relationship('Category', back_populates='products')
    cart_items = relationship('CartItem', back_populates='product', uselist=True)
    order_items = relationship('OrderItem', back_populates='product', uselist=True)
    created_at = Column(String(255), default=datetime.datetime.utcnow())
    updated_at = Column(String(255), default=datetime.datetime.utcnow())


class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String(255), nullable=False)
    file_name = Column(String(255), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'))

    product = relationship('Product', back_populates='images')
    created_at = Column(String(255), default=datetime.datetime.utcnow())
    updated_at = Column(String(255), default=datetime.datetime.utcnow())


class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='carts')
    cart_items = relationship('CartItem', back_populates='cart', uselist=True)
    created_at = Column(String(255), default=datetime.datetime.utcnow())
    updated_at = Column(String(255), default=datetime.datetime.utcnow())


class CartItem(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey('carts.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, default=1, nullable=False)

    cart = relationship('Cart', back_populates='cart_items')
    product = relationship('Product', back_populates='cart_items', uselist=False)
    created_at = Column(String(255), default=datetime.datetime.utcnow())
    updated_at = Column(String(255), default=datetime.datetime.utcnow())


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    total = Column(Integer, default=0, nullable=False)
    status = Column(String(255), default=OrderStatus.PENDING, nullable=False)

    user = relationship('User', back_populates='orders')
    order_items = relationship('OrderItem', back_populates='order', uselist=True)
    created_at = Column(String(255), default=datetime.datetime.utcnow())
    updated_at = Column(String(255), default=datetime.datetime.utcnow())


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, default=1, nullable=False)

    order = relationship('Order', back_populates='order_items')
    product = relationship('Product', back_populates='order_items', uselist=False)
    created_at = Column(String(255), default=datetime.datetime.utcnow())
    updated_at = Column(String(255), default=datetime.datetime.utcnow())
