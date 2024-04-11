from fastapi import APIRouter, Body
from utils import get_mongo_client
from models.aggregator import Post
from fastapi.encoders import jsonable_encoder


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


def get_post(post_id: str):
    post = aggregator_client["posts"].find_one({"_id": post_id})
    return post
