from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class UserCreate(BaseModel):
    email: EmailStr
    password: str 

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True
        
class UserLogin(UserCreate):
    pass

class PostBase(BaseModel):
    title: str
    content: str
    published : bool = True
    
class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserOut
    
    class Config:
        from_attributes = True
    

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
    
class PostOut(PostBase):
    Post:Post
    votes:int
    
    class Config:
        from_attributes = True