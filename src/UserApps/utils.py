'''
    응답 정규화 데이터 보강 등 로직이 아닌 기능
'''
from typing import Optional
from pydantic import BaseModel

class RequestData(BaseModel) :
    id: int
    email: Optional[str] = None
    