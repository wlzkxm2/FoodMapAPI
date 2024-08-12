from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

from database import engine

from ReviewApps.router import router as review_apps

from UserApps.router import TokenService, UserService

import uvicorn

# uvicorn main:app --reload

app = FastAPI()
token_service = TokenService()
user_service = UserService()

app.include_router(review_apps)
app.include_router(token_service.router)
app.include_router(user_service.router)

@app.get("/health_check/")
async def health_check():
    return {"message" : "main - ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port="8112", reload=True)