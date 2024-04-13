from fastapi import APIRouter, Body, Depends, HTTPException
from utils import get_mongo_client
from models.aggregator import Post
from fastapi.encoders import jsonable_encoder
from routers.user import auth_manager


aggregator_router = APIRouter(prefix="/aggregator")
aggregator_client = get_mongo_client()["aggregator"]


@aggregator_router.post("/add-aggregation")
def put_aggregations(post: Post = Body(...)):
    post_data = jsonable_encoder(post)
    res_post = aggregator_client["posts"].insert_one(post_data)
    return {"message": "Added text aggregation", "post_id": str(res_post.inserted_id)}


@aggregator_router.get("/get-aggregation")
def get_aggregations(post_id: str):
    post = get_post(post_id)
    return {"message": "Retrieved aggregations", "post": jsonable_encoder(post)}


@aggregator_router.get("/get-all-aggregations")
def get_all_aggregations(limit: int):
    return {
        "message": "Retrieved aggregations",
        "list_posts": list(aggregator_client["posts"].find().limit(limit)),
    }


@aggregator_client.post("/upvote")
def upvote_post(post_id: str, user=Depends(auth_manager)):
    if get_post(post_id) is None:
        raise HTTPException(status_code=404, detail="Post not found")

    aggregator_client["posts"].update_one(
        {"_id": post_id}, {"$inc": {"upvotes": 1}}, upsert=False
    )
    return {"message": "Post upvoted"}


def get_post(post_id: str):
    post = aggregator_client["posts"].find_one({"_id": post_id})
    return post
