from fastapi import APIRouter, Body, Depends, HTTPException
from utils import get_mongo_client
from models.aggregator import Post, Comment
from fastapi.encoders import jsonable_encoder
from routers.user import auth_manager, user_client


aggregator_router = APIRouter(prefix="/aggregator")
aggregator_client = get_mongo_client()["aggregator"]


@aggregator_router.post("/add-aggregation")
async def put_aggregations(post: Post = Body(...)):
    post_data = jsonable_encoder(post)
    res_post = aggregator_client["posts"].insert_one(post_data)
    return {"message": "Added text aggregation", "post_id": str(res_post.inserted_id)}


@aggregator_router.get("/get-aggregation")
async def get_aggregations(post_id: str):
    post = get_post(post_id)
    return {"message": "Retrieved aggregations", "post": jsonable_encoder(post)}


@aggregator_router.get("/get-all-aggregations")
async def get_all_aggregations(limit: int):
    return {
        "message": "Retrieved aggregations",
        "list_posts": list(aggregator_client["posts"].find().limit(limit)),
    }


@aggregator_router.put("/upvote")
async def upvote_post(post_id: str, user=Depends(auth_manager)):
    if get_post(post_id) is None:
        raise HTTPException(status_code=404, detail="Post not found")

    # Checks if user has already upvoted the post
    if post_id in user["list_of_upvotes"]:
        raise HTTPException(status_code=400, detail="Post already upvoted")

    # Checks if user has already downvoted the post
    if post_id in user["list_of_downvotes"]:
        change_attribute_count(post_id, "downvotes", False)
        remove_from_attribute_list(user, "list_of_downvotes", post_id)

    change_attribute_count(post_id, "upvotes", True)
    add_to_attribute_list(user["id"], "list_of_upvotes", post_id)

    return {"message": "Post upvoted"}


@aggregator_router.put("/remove-upvote")
async def remove_upvote_post(post_id: str, user=Depends(auth_manager)):
    if get_post(post_id) is None:
        raise HTTPException(status_code=404, detail="Post not found")

    # Checks if user has not upvoted the post
    if post_id not in user["list_of_upvotes"]:
        raise HTTPException(status_code=400, detail="Post not upvoted")

    change_attribute_count(post_id, "upvotes", False)
    remove_from_attribute_list(user, "list_of_upvotes", post_id)

    return {"message": "Post upvote removed"}


@aggregator_router.put("/downvote")
async def downvote_post(post_id: str, user=Depends(auth_manager)):
    if get_post(post_id) is None:
        raise HTTPException(status_code=404, detail="Post not found")

    # Checks if user has already downvoted the post
    if post_id in user["list_of_downvotes"]:
        raise HTTPException(status_code=400, detail="Post already downvoted")

    # Checks if user has already upvoted the post
    if post_id in user["list_of_upvotes"]:
        change_attribute_count(post_id, "upvotes", False)
        remove_from_attribute_list(user, "list_of_upvotes", post_id)

    change_attribute_count(post_id, "downvotes", True)
    add_to_attribute_list(user["id"], "list_of_downvotes", post_id)

    return {"message": "Post downvoted"}


@aggregator_router.put("/remove-downvote")
async def remove_downvote_post(post_id: str, user=Depends(auth_manager)):
    if get_post(post_id) is None:
        raise HTTPException(status_code=404, detail="Post not found")

    # Checks if user has not upvoted the post
    if post_id not in user["list_of_downvotes"]:
        raise HTTPException(status_code=400, detail="Post not downvoted")

    change_attribute_count(post_id, "downvotes", False)
    remove_from_attribute_list(user, "list_of_downvotes", post_id)

    return {"message": "Post upvote removed"}


@aggregator_router.post("/comment")
async def comment_post(comment: Comment = Body(...), user=Depends(auth_manager)):
    if get_post(comment.post_id) is None:
        raise HTTPException(status_code=404, detail="Post not found")

    comment_data = jsonable_encoder(comment)
    comment_data["user_id"] = user["id"]

    aggregator_client["comments"].insert_one(comment_data)
    return {"message": "Comment added"}


@aggregator_router.get("/get-comments")
async def get_comments(post_id: str):
    comments = list(aggregator_client["comments"].find({"post_id": post_id}))
    return {"message": "Retrieved comments", "comments": comments}


def remove_from_attribute_list(user: dict, attribute: str, post_id: str):
    user[attribute].remove(post_id)
    user_client["users"].update_one(
        {"_id": user["id"]}, {"$set": {attribute: user[attribute]}}, upsert=False
    )


def add_to_attribute_list(user_id: str, attribute: str, post_id: str):
    user_client["users"].update_one(
        {"_id": user_id}, {"$push": {attribute: post_id}}, upsert=False
    )


def change_attribute_count(post_id: str, attribute: str, increment: bool):
    aggregator_client["posts"].update_one(
        {"_id": post_id}, {"$inc": {attribute: 1 if increment else -1}}, upsert=False
    )


def get_post(post_id: str):
    post = aggregator_client["posts"].find_one({"_id": post_id})
    return post
