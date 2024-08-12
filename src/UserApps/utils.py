'''
    응답 정규화 데이터 보강 등 로직이 아닌 기능
'''
import jwt

from datetime import datetime, timedelta
from jwt.exceptions import InvalidTokenError
from typing import Optional
from pydantic import BaseModel
from fastapi import HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from env.config import jwt_settings

class RequestData(BaseModel) :
    id: int
    email: Optional[str] = None

def HTTPErrorException(
    status_code: int=status.HTTP_403_FORBIDDEN, 
    error_code:str="FORBIDDEN_REQUEST", 
    detail: str="올바르지 않은 요청입니다."
) :
    return HTTPException(
        status_code=status_code,
        detail={
            "code": error_code,
            "message": detail
        }
    )
    
def HTTPResponse(status_code: int=status.HTTP_200_OK, content: dict=None) :
    return JSONResponse(
        status_code=status_code,
        content=content
    )

class JWTService :
    def __init__(self):
        self.SECRET_KEY = jwt_settings.secret_key
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 60
        self.REFRESH_TOKEN_EXPIRE_DAYS = 7
        
    def create_access_token(self, data: dict) :
        # 토큰 생성
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt
    
    def create_refresh_token(self, data: dict) :
        # 토큰 생성
        to_encode = data.copy()
        expire = datetime.now() + timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def check_access_token(self, token: str) :
        # 토큰 체크
        try :
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['exp'] is None or payload['exp'] < datetime.now().timestamp() :
                return False
            return True
        except InvalidTokenError :
            return False
        except :
            return False
        
    def refresh_token(self, token: str) :
        # 토큰 갱신
        payload = jwt.decode(token, self.SECRET_KEY, algorithms=self.ALGORITHM)
        if payload['exp'] < datetime.now().timestamp() :
            return False
        
        return self.create_access_token(payload)
    
async def validate_token(request: Request) -> dict | None:
    authorization = request.headers.get("Authorization")
    scheme = authorization.split(" ")[0]
    param = authorization.split(" ")[1]
    
    if not authorization or scheme.lower() != "bearer" or not jwt_service.check_access_token(param):
        raise HTTPErrorException(status_code=status.HTTP_401_UNAUTHORIZED, error_code="INVALID_TOKEN", detail="Invalid token")
    payload = jwt.decode(param, jwt_service.SECRET_KEY, algorithms=jwt_service.ALGORITHM)
    return payload

jwt_service = JWTService()