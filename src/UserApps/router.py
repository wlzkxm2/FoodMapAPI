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

class UserRouter :
    def __init__(self) -> None:
        self.router = APIRouter(prefix='/users')
        self.router.add_api_route("/master", self.health_check, methods=["GET"])
        self.router.add_api_route("/register", self.create_user, methods=["POST"])
        self.router.add_api_route("/login", self.login, methods=["POST"])
        
    def health_check(self):
        return {"message" : "UserService - ok"}
    
    async def create_user(self, user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
        db_user = service.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        return service.create_user(db=db, user=user)

    async def login(self, request:Request, payload: Dict[Any, Any], db: Session = Depends(dependencies.get_db)):
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

class TokenRouter :
    def __init__(self):
        self.router = APIRouter(prefix='/token')
        self.router.add_api_route("/master", self.health_check, methods=["GET"])
        self.router.add_api_route("/refresh_token", self.refresh, methods=["POST"])
    
    def health_check(self):
        return {"message" : "TokenService - ok"}
            
    async def refresh(self, payload: Dict[Any, Any], db: Session = Depends(dependencies.get_db)):
        try :
            refresh_token = payload['refresh_token']
            token = jwt_service.refresh_token(refresh_token)
            
            return HTTPResponse(
                content={
                    "type" : "Bearer",
                    "access_token": token,
                    "refresh_token": refresh_token
                })
        except Exception as e:
            print(e)
            raise HTTPErrorException(
                error_code="FORBIDDEN_REQUEST",
                detail="Invalid request"
            )
    


