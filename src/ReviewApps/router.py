'''
    모든 엔드포인트를 갖춘 각 모듈의 핵심
'''
from base64 import b64decode
from datetime import datetime
from typing import Any, Dict
from fastapi import APIRouter, Depends, Request, Response
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
        self.router.add_api_route("/byte", self.byte_image, methods=["POST"])
        self.db = Depends(dependencies.get_db)

    async def health_check(self):
        return {"message" : "review_apps - ok"}
    
    async def byte_image(self, request:Request, payload:Dict[Any, Any], db: Session=Depends(dependencies.get_db)):
        byte_image = payload.get('byte_image')
        if byte_image is None:
            return {"error": "No byte image provided"}

        decode_img = b64decode(byte_image)
        
        with open('../media/test/test.jpg', 'wb') as f:
            f.write(decode_img)
        print(f.name)
        print('/'.join(f.name.split('/')[1:]
        ))

        # 이미지 응답 생성
        return Response(content=decode_img, media_type="image/jpeg")
    
    async def review(self, request:Request, payload:Dict[Any, Any], db: Session=Depends(dependencies.get_db)):
        
        token = await validate_token(request)
        
        _food_list = []
        for _payload_food in payload.get('food') :
            _food_list.append(schemas.FoodCreate(**_payload_food))
        
        img_list = []
        for imgs in payload.get('FoodImg') : 
            b64decode_img = b64decode(imgs)
            with open(f'../media/review_imgs/{datetime.now().timestamp()}.jpg', 'wb') as f:
                f.write(b64decode_img)
                
            img_list.append(
                schemas.FoodImgCreate(
                    img='/'.join(f.name.split('/')[1:])
                )
            )
            
        _review = schemas.ReviewCreate(
            title=payload.get('title'),
            content=payload.get('content'),
            rating=payload.get('rating'),
        )
        
        _create_review = service.create_user_review(db, _review, token.get('user'))
        
        await service.bulk_create_food(db, _food_list, _create_review.id)
        await service.bulk_create_food_img(db, img_list, _create_review.id)
        
        return {"message" : "review_apps - review"}
