from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

from database import engine

import UserApps.router as user_router
import ReviewApps.router as review_router
# from ReviewApps.router import ReviewRouter
# from UserApps.router import TokenRouter, UserRouter

import uvicorn

# uvicorn main:app --reload

app = FastAPI()

app.mount("/media", StaticFiles(directory="../media"), name="media")

app.include_router(review_router.ReviewRouter().router)
app.include_router(user_router.UserRouter().router)
app.include_router(user_router.TokenRouter().router)

@app.get("/health_check/")
async def health_check():
    return {"message" : "main - ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port="8112", reload=True)