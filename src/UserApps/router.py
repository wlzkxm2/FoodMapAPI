'''
    모든 엔드포인트를 갖춘 각 모듈의 핵심
'''
from fastapi import APIRouter, FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from UserApps.utils import RequestData
from database import SessionLocal, engine
from . import models as user_models
from . import service, dependencies, schemas

user_models.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix='/users')

@router.get("/health_check/", tags=["health_check"])
async def health_check():
    return {"message" : "user_apps - ok"}

@router.post("/parameter_test/")
async def parameter_test(test: int):
    """
        Parameters
    """
    if test is not None :
        return {"test" : test}
    else :
        return {"test" : "None"}
    
@router.post("/body_test/")
async def body_test(body: RequestData):
    """
        body
    """
    if body is not None :
        return {"body" : body}
    else :
        return {"body" : "None"}

@router.get("/users/", tags=["users"])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    users = service.get_users(db, skip=skip, limit=limit)
    return users

@router.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    db_user = service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return service.create_user(db=db, user=user)