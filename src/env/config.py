from pydantic_settings import BaseSettings

class Settings(BaseSettings) :
    db_user:str = "foodmanager"
    db_password:str = "fmpq1w2e3r4"
    db_host:str = "localhost"
    db_name:str = "foodmapdb"

class JWTSettings(BaseSettings) :
    secret_key:str = "8f590482fa9d9a1e8d44324ef1004691a880a7daaa6d6e30590aecb52f7ef050"
    
settings = Settings()
jwt_settings = JWTSettings()