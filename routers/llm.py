from fastapi import APIRouter, Body, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from models.llm import Summary, Title
from routers.annotator import annotator_client
from utils import get_mongo_client, change_db_id_to_str

llm_router = APIRouter(prefix="/llm")
llm_client = get_mongo_client()["llm"]


@llm_router.post("/add-summary")
async def add_summary(_: Request, summary: Summary = Body(...)):
    if llm_client["summaries"].find_one({"id": summary.id}):
        raise HTTPException(
            status_code=400, detail="Summary with same id already exists"
        )
    elif llm_client["summaries"].find_one({"post_id": summary.post_id}):
        raise HTTPException(
            status_code=400, detail="Summary with same post_id already exists"
        )
    elif annotator_client["posts"].find_one({"_id": summary.post_id}) is None:
        raise HTTPException(status_code=400, detail="Post with post_id does not exist")

    summary_data = jsonable_encoder(summary)
    res_summary = llm_client["summaries"].insert_one(summary_data)

    return {
        "message": "Added summary",
        "summary_id": str(res_summary.inserted_id),
    }


@llm_router.post("/add-title")
async def add_title(_: Request, title: Title = Body(...)):
    if llm_client["titles"].find_one({"id": title.id}):
        raise HTTPException(status_code=400, detail="Title with same id already exists")
    elif llm_client["titles"].find_one({"post_id": title.post_id}):
        raise HTTPException(
            status_code=400, detail="Title with same post_id already exists"
        )
    elif annotator_client["posts"].find_one({"_id": title.post_id}) is None:
        raise HTTPException(status_code=400, detail="Post with post_id does not exist")

    title_data = jsonable_encoder(title)
    res_title = llm_client["titles"].insert_one(title_data)

    return {
        "message": "Added title",
        "title_id": str(res_title.inserted_id),
    }


@llm_router.get("/get-summary")
async def get_summary(summary_id: str):
    if summary := llm_client["summaries"].find_one(
        {"_id": change_db_id_to_str(summary_id)}
    ):
        return {"message": "Summary found", "summary": change_db_id_to_str(summary)}
    else:
        raise HTTPException(status_code=404, detail="Summary not found")


def get_summary_by_post_id(post_id: str):
    return llm_client["summaries"].find_one({"post_id": post_id})
