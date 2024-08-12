'''
    모든 엔드포인트를 갖춘 각 모듈의 핵심
'''
import base64
from datetime import datetime
from json import JSONDecodeError
from typing import Any, Dict
from fastapi import APIRouter, FastAPI, Depends, HTTPException, Request
from fastapi import status as response_status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from UserApps.utils import HTTPErrorException, HTTPResponse, RequestData, jwt_service, validate_token
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

@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    db_user = service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return service.create_user(db=db, user=user)

@router.post("/login", response_model=schemas.User)
async def login(request:Request, payload: Dict[Any, Any], db: Session = Depends(dependencies.get_db)):
    try :
        db_user = service.authenticate_user(db, email=payload['email'], password=payload['password'])
        
        if not db_user:
            raise HTTPErrorException(
                error_code="INVALID_USER",
                detail="Invalid email or password"
            )
        
        refresh_token = jwt_service.create_refresh_token(
            {
                "user": db_user.email,
                "create_at" : datetime.now().timestamp(),
                "type" : "refresh"
            }
        )
        
        access_token = jwt_service.create_access_token(
            {
                "user": db_user.email,
                "create_at" : datetime.now().timestamp(),
                "type" : "access",
            }
        )
        
        return HTTPResponse(
            content={
                "type" : "Bearer",
                "access_token": access_token,
                "refresh_token": refresh_token
            })
    except Exception as e:
        print(e)
        raise HTTPErrorException(
            error_code="FORBIDDEN_REQUEST",
            detail="Invalid request"
        )
        
@router.post("/token", response_model=schemas.User)
async def token(request:Request, payload: Dict[Any, Any], db: Session = Depends(dependencies.get_db)):
    try :
        await validate_token(request)
        
        return HTTPResponse(
            content={
                "message": "token is valid"
            })
    except Exception as e:
        print(e)
        raise HTTPErrorException(
            error_code="FORBIDDEN_REQUEST",
            detail="Invalid request"
        )