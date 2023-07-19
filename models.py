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
    phone_number = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    dob = Column(String(255), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='user_information')
    created_at = Column(String(255), default=datetime.datetime.utcnow())
