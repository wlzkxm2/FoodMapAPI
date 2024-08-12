'''
    모든 엔드포인트를 갖춘 각 모듈의 핵심
'''
from fastapi import APIRouter
from database import SessionLocal, engine
from . import models as review_models

review_models.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix='/review')

@router.get("/health_check/", tags=["health_check"])
async def health_check():
    return {"message" : "review_apps - ok"}