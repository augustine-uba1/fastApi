from datetime import datetime
from pydantic import BaseModel, EmailStr, conint, Field, validator
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

class PostCreate(PostBase):
    pass

class UpdatePost(PostBase):
    published: bool

class UserOut (BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True
    
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    
    owner: UserOut
    
    class Config:
        orm_mode = True
        
class PostOut(BaseModel):
    Post: Post
    votes: int
    
    class Config:
        orm_mode = True
    
class UserCreate(BaseModel):
    email: EmailStr
    password: str
     
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str]

# ALTERNATIVE METHOD OF VALIDATING VOTE DIRECTION (0 OR 1)
# BUT THIS METHOD ALLOWS FOR NEGATIVE INTEGERS  
# class Vote(BaseModel):
#     post_id: int
#     dir: conint(le=1)

class Vote(BaseModel):
    post_id: int
    dir: int = Field(..., ge=0, le=1)
    
    
    @validator('dir')
    def validate_dir(cls, dir_value):
        if dir_value not in (0, 1):
            raise ValueError('dir field must be 0 or 1')
        return dir_value