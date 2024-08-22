'''
    모든 엔드포인트를 갖춘 각 모듈의 핵심
'''
from typing import Any, Dict
from fastapi import APIRouter, Depends, Request
from ReviewApps import dependencies, schemas, service
from UserApps.utils import validate_token
from database import SessionLocal, engine
from . import models as review_models
from sqlalchemy.orm import Session

class ReviewRouter :
    def __init__(self) -> None:
        self.router = APIRouter(prefix='/review')
        self.router.add_api_route("/health_check", self.health_check, methods=["GET"])
        self.router.add_api_route("/", self.review, methods=["POST"])
        self.db = Depends(dependencies.get_db)

    async def health_check(self):
        return {"message" : "review_apps - ok"}
    
    async def review(self, request:Request, payload:Dict[Any, Any], db: Session=Depends(dependencies.get_db)):
        print(payload)
        
        token = await validate_token(request)
        
        print(token)
        print("-----------------")
        
        print(payload.get('title'))
        print(payload.get('content'))
        print(payload.get('food'))
        print("-----------------")
        
        _food_list = []
        for _payload_food in payload.get('food') :
            _food_list.append(schemas.FoodCreate(**_payload_food))
            
        _review = schemas.ReviewCreate(
            title=payload.get('title'),
            content=payload.get('content'),
            rating=payload.get('rating'),
        )
        
        print("-----------------")
        print(_review)
        print("-----------------")
        
        _create_review = service.create_user_review(db, _review, token.get('user'))
        
        await service.bulk_create_food(db, _food_list, _create_review.id)
        
        return {"message" : "review_apps - review"}
