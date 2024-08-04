from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

from database import engine
from ReviewApps.router import router as review_apps
from UserApps.router import router as user_apps

import uvicorn

# uvicorn main:app --reload

app = FastAPI()

app.include_router(review_apps)
app.include_router(user_apps)

@app.get("/health_check/")
async def health_check():
    return {"message" : "main - ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port="8111", reload=True)