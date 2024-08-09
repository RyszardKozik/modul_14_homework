from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
import datetime

from .db import Base

class User(Base):
    """
    Represents a user in the system.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)  # Correct usage of utcnow
    is_active = Column(Boolean, default=True)

    # Relationships with other tables
    photos = relationship("Photo", back_populates="owner")
    comments = relationship("Comment", back_populates="user")


class Photo(Base):
    """
    Represents a photo uploaded by a user.
    """
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    image_url = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)  # Correct usage of utcnow

    owner = relationship("User", back_populates="photos")
    comments = relationship("Comment", back_populates="photo")


class Comment(Base):
    """
    Represents a comment made on a photo.
    """
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))
    photo_id = Column(Integer, ForeignKey('photos.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)  # Correct usage of utcnow
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="comments")
    photo = relationship("Photo", back_populates="comments")
