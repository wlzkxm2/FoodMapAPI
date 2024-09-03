'''
    pydantic 모델용
'''

from pydantic import BaseModel

class FoodImgBase(BaseModel):
    id: int
    img: str
        
class FoodImgCreate(BaseModel):
    img:str

class FoodImg(FoodImgBase):
    id: int
    review_id: int

    class Config:
        from_attributes = True
        

class FoodBase(BaseModel):
    id: int
    name: str
    price: int
    rating: int

class FoodCreate(BaseModel):
    name: str
    price: int
    rating: int

class Food(FoodBase):
    id: int
    review_id: int

    class Config:
        from_attributes = True


class ReviewBase(BaseModel):
    id: int
    title: str
    content: str
    latitude: float
    longitude: float
    rating: int
        
class ReviewCreate(BaseModel):
    title: str
    content: str

class Review(ReviewBase):
    id: int
    user_id: int
    eat_food: list[Food] = []
    food_img: list[FoodImg] = []
    
    class Config:
        from_attributes = True
