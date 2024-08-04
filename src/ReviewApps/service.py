'''
    모듈별 비즈니스 로직
'''
from sqlalchemy.orm import Session
from . import models, schemas

def get_review(db: Session, review_id: int):
    return db.query(models.Review).filter(models.Review.id == review_id).first()

def create_user_review(db: Session, review: schemas.ReviewCreate, user_id: int):
    db_review = models.Review(**review.model_dump(), user_id=user_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_food(db: Session, food_id: int):
    return db.query(models.Food).filter(models.Food.id == food_id).first()

def create_food(db: Session, food: schemas.FoodCreate, review_id: int):
    db_food = models.Food(**food.model_dump(), review_id=review_id)
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food

def get_food_img(db: Session, food_img_id: int):
    return db.query(models.FoodImg).filter(models.FoodImg.id == food_img_id).first()

def create_food_img(db: Session, food_img: schemas.FoodImgCreate, review_id: int):
    db_food_img = models.FoodImg(**food_img.model_dump(), review_id=review_id)
    db.add(db_food_img)
    db.commit()
    db.refresh(db_food_img)
    return db_food_img
