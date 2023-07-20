from enum import Enum
import datetime

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base


class UserRole(str, Enum):
    SUPPER_ADMIN = 'supper_admin'
    ADMIN = 'admin'
    USER = 'user'


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

    products = relationship('Product', back_populates='category')
    created_at = Column(String(255), default=datetime.datetime.utcnow())
    updated_at = Column(String(255), default=datetime.datetime.utcnow())


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))

    images = relationship('Image', back_populates='product')
    category = relationship('Category', back_populates='products')
    created_at = Column(String(255), default=datetime.datetime.utcnow())
    updated_at = Column(String(255), default=datetime.datetime.utcnow())


class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'))

    product = relationship('Product', back_populates='images')
    created_at = Column(String(255), default=datetime.datetime.utcnow())
    updated_at = Column(String(255), default=datetime.datetime.utcnow())
