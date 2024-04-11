from fastapi import FastAPI
from dotenv import dotenv_values
import uvicorn
from routers.user import user_router

config = dotenv_values(".env")


app = FastAPI(title="News Annotator DB-Service", version="1.0")

app.include_router(user_router)


@app.get("/")
async def root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=1)
