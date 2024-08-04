from pydantic_settings import BaseSettings

class Settings(BaseSettings) :
    db_user:str = ""
    db_password:str = ""
    db_host:str = ""
    db_name:str = ""
    
settings = Settings()