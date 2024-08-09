from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserBase(BaseModel):
    """
    Base model for User schema.
    """
    username: str = Field(..., min_length=3, max_length=50, description="Username of the user")
    email: EmailStr = Field(..., description="Email address of the user")

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    password: str = Field(..., min_length=8, max_length=100, description="Password for the user")

class UserUpdate(UserBase):
    """
    Schema for updating user information.
    """
    password: Optional[str] = Field(None, min_length=8, max_length=100, description="Password for the user")

class UserOut(UserBase):
    """
    Schema for outputting user information.
    """
    id: int

    class Config:
        from_attributes = True

class PhotoBase(BaseModel):
    """
    Base model for Photo schema.
    """
    title: str = Field(..., min_length=3, max_length=100, description="Title of the photo")
    description: Optional[str] = Field(None, max_length=500, description="Description of the photo")

class PhotoCreate(PhotoBase):
    """
    Schema for creating a new photo.
    """
    image_url: str = Field(..., description="URL of the photo")

class PhotoOut(PhotoBase):
    """
    Schema for outputting photo information.
    """
    id: int
    owner_id: int

    class Config:
        from_attributes = True

class CommentBase(BaseModel):
    """
    Base model for Comment schema.
    """
    content: str = Field(..., min_length=1, max_length=500, description="Content of the comment")

class CommentCreate(CommentBase):
    """
    Schema for creating a new comment.
    """
    pass

class CommentOut(CommentBase):
    """
    Schema for outputting comment information.
    """
    id: int
    user_id: int
    photo_id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Schema for token data.
    """
    username: Optional[str] = None
