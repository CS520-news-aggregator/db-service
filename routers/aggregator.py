from fastapi import APIRouter, Body, Depends, HTTPException
from utils import get_mongo_client
from models.aggregator import Post, Comment
from models.user import UserVotes
from fastapi.encoders import jsonable_encoder
from routers.user import auth_manager, user_client


aggregator_router = APIRouter(prefix="/aggregator")
aggregator_client = get_mongo_client()["aggregator"]

def change_db_id_to_str(data):
    if data:
        data["id"] = str(data["_id"])
    return data

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


def vote_post_or_comment(
    uid: str,
    is_upvote: bool,
    is_comment: bool,
    user=Depends(auth_manager),
):
    identifier = "Comment" if is_comment else "Post"
    if (is_comment and get_comment(uid) is None) or (
        not is_comment and get_post(uid) is None
    ):
        raise HTTPException(status_code=404, detail=f"{identifier} not found")

    collection_name = "comments" if is_comment else "posts"

    to_vote = "upvotes" if is_upvote else "downvotes"
    to_vote_against = "downvotes" if is_upvote else "upvotes"

    user_votes = user_client["votes"].find_one({"user_id": user["id"]})

    # Checks if user has already upvoted
    if uid in user_votes[f"list_of_{collection_name}_{to_vote}"]:
        raise HTTPException(status_code=400, detail=f"{identifier} already {to_vote}")

    # Checks if user has downvoted the post
    if uid in user_votes[f"list_of_{collection_name}_{to_vote_against}"]:
        change_attribute_count(collection_name, uid, to_vote_against, False)
        remove_from_attribute_list(
            user_votes, f"list_of_{collection_name}_{to_vote_against}", uid
        )

    change_attribute_count(collection_name, uid, to_vote, True)
    add_to_attribute_list(user["id"], f"list_of_{collection_name}_{to_vote}", uid)

    return {"message": f"{identifier} {to_vote}"}


def remove_vote_post_or_comment(
    uid: str,
    is_upvote: bool,
    is_comment: bool,
    user=Depends(auth_manager),
):
    identifier = "Comment" if is_comment else "Post"
    if (is_comment and get_comment(uid) is None) or (
        not is_comment and get_post(uid) is None
    ):
        raise HTTPException(status_code=404, detail=f"{identifier} not found")

    collection_name = "comments" if is_comment else "posts"
    to_vote = "upvotes" if is_upvote else "downvotes"

    user_votes = user_client["votes"].find_one({"user_id": user["id"]})

    # Checks if user has not voted the post
    if uid not in user_votes[f"list_of_{collection_name}_{to_vote}"]:
        raise HTTPException(status_code=400, detail=f"{collection_name} not {to_vote}")

    change_attribute_count(collection_name, uid, to_vote, False)
    remove_from_attribute_list(user_votes, f"list_of_{collection_name}_{to_vote}", uid)

    return {"message": f"{identifier} {to_vote} removed"}


@aggregator_router.put("/upvote-post")
async def upvote_post(post_id: str, user=Depends(auth_manager)):
    return vote_post_or_comment(
        uid=post_id, is_upvote=True, is_comment=False, user=user
    )


@aggregator_router.put("/upvote-comment")
async def upvote_comment(comment_id: str, user=Depends(auth_manager)):
    return vote_post_or_comment(
        uid=comment_id, is_upvote=True, is_comment=True, user=user
    )


@aggregator_router.put("/downvote-post")
async def downvote_post(post_id: str, user=Depends(auth_manager)):
    return vote_post_or_comment(
        uid=post_id, is_upvote=False, is_comment=False, user=user
    )


@aggregator_router.put("/downvote-comment")
async def downvote_comment(comment_id: str, user=Depends(auth_manager)):
    return vote_post_or_comment(
        uid=comment_id, is_upvote=False, is_comment=True, user=user
    )


@aggregator_router.put("/remove-upvote-comment")
async def remove_upvote_comment(comment_id: str, user=Depends(auth_manager)):
    return remove_vote_post_or_comment(
        uid=comment_id, is_upvote=True, is_comment=True, user=user
    )


@aggregator_router.put("/remove-downvote-comment")
async def remove_downvote_comment(comment_id: str, user=Depends(auth_manager)):
    return remove_vote_post_or_comment(
        uid=comment_id, is_upvote=False, is_comment=True, user=user
    )


@aggregator_router.put("/remove-upvote-post")
async def remove_upvote_post(post_id: str, user=Depends(auth_manager)):
    return remove_vote_post_or_comment(
        uid=post_id, is_upvote=True, is_comment=False, user=user
    )


@aggregator_router.put("/remove-downvote-post")
async def remove_downvote_post(post_id: str, user=Depends(auth_manager)):
    return remove_vote_post_or_comment(
        uid=post_id, is_upvote=False, is_comment=False, user=user
    )


@aggregator_router.post("/comment")
async def comment_post(comment: Comment = Body(...), user=Depends(auth_manager)):
    if get_post(comment.post_id) is None:
        raise HTTPException(status_code=404, detail="Post not found")

    comment_data = jsonable_encoder(comment)
    comment_data["author_id"] = user["id"]

    aggregator_client["comments"].insert_one(comment_data)
    return {"message": "Comment added", "comment_id": str(comment_data["_id"])}


@aggregator_router.get("/get-comments")
async def get_comments(post_id: str):
    comments = list(aggregator_client["comments"].find({"post_id": post_id}))
    return {"message": "Retrieved comments", "comments": comments}


def remove_from_attribute_list(dt_vals: dict, attribute: str, post_id: str):
    dt_vals[attribute].remove(post_id)
    user_client["votes"].update_one(
        {"_id": dt_vals["_id"]}, {"$set": {attribute: dt_vals[attribute]}}, upsert=False
    )


def add_to_attribute_list(user_id: str, attribute: str, uid: str):
    user_client["votes"].update_one(
        {"user_id": user_id}, {"$push": {attribute: uid}}, upsert=False
    )


def change_attribute_count(
    collection_name: str, uid: str, attribute: str, increment: bool
):
    aggregator_client[collection_name].update_one(
        {"_id": uid}, {"$inc": {attribute: 1 if increment else -1}}, upsert=False
    )


def get_post(post_id: str):
    post = aggregator_client["posts"].find_one({"_id": post_id})
    post = change_db_id_to_str(post)
    return post


def get_comment(comment_id: str):
    comment = aggregator_client["comments"].find_one({"_id": comment_id})
    comment = change_db_id_to_str(comment)
    return comment
