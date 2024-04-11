from fastapi import FastAPI
from dotenv import dotenv_values
import uvicorn
from routers.user import user_router
from routers.annotator import annotator_router
from routers.aggregator import aggregator_router
from utils import get_mongo_client

config = dotenv_values(".env")


app = FastAPI(title="News Annotator DB-Service", version="1.0")

app.include_router(user_router)
app.include_router(annotator_router)
app.include_router(aggregator_router)


@app.get("/")
async def root():
    return {"Hello": "World"}

@app.get("/clean_db")
async def clean_db():
    client = get_mongo_client()
    client.drop_database("user")
    client.drop_database("annotator")
    client.drop_database("aggregator")
    return {"message": "Databases cleaned"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=1)
