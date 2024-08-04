'''
    라우터 종속성을 정의하는 파일
'''

from database import SessionLocal

def get_db() :
    db = SessionLocal()
    
    try :
        yield db
    finally :
        db.close()
