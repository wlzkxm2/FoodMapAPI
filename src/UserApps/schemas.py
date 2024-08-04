'''
    pydantic 모델용
'''

from pydantic import BaseModel

from ReviewApps.schemas import Review

class UserBase(BaseModel):
    email: str
    
class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    reviews: list[Review] = []
    
    class Config:
        from_attributes = True