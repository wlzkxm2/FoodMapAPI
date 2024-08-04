'''
    pydantic 모델용
'''

from pydantic import BaseModel

class FoodImgBase(BaseModel):
    id: int
    img: str
        
class FoodImgCreate(BaseModel):
    pass

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
    pass

class Food(FoodBase):
    id: int
    review_id: int

    class Config:
        from_attributes = True


class ReviewBase(BaseModel):
    id: int
    title: str
    content: str
        
class ReviewCreate(BaseModel):
    pass

class Review(ReviewBase):
    id: int
    user_id: int
    eat_food: list[Food] = []
    food_img: list[FoodImg] = []
    
    class Config:
        from_attributes = True
