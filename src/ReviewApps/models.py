'''
    db 모델용
'''

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base 

from UserApps.models import User

class Review(Base) :
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, index=True)
    content = Column(String)
    rating = Column(Integer)
    
    address = Column(String)
    
    latitude = Column(Float)
    longitude = Column(Float)
    
    owner = relationship("User", back_populates="reviews")
    eat_food = relationship("Food", back_populates="reviews")
    food_img = relationship("FoodImg", back_populates="reviews")

class Food(Base) :
    __tablename__ = "foods"
    
    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("reviews.id"))
    name = Column(String, index=True)
    price = Column(Integer)
    rating = Column(Integer)
    
    reviews = relationship("Review", back_populates="eat_food")
    
class FoodImg(Base) :
    __tablename__ = "food_imgs"
    
    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("reviews.id"))
    img = Column(String)
    
    reviews = relationship("Review", back_populates="food_img")
