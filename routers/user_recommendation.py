from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from models.user_recommendation import UserRecommendation
from utils import get_mongo_client

user_recommendation_router = APIRouter(prefix="/user_recommendation")
user_recommendation_client = get_mongo_client()["user_recommendation"]


@user_recommendation_router.post("/add-recommendation")
async def add_user_recommendation(recommendation: UserRecommendation = Body(...)):
    recommendation_dict = jsonable_encoder(recommendation)

    added_recommendation = user_recommendation_client["recommendations"].insert_one(
        recommendation_dict
    )

    return {
        "message": "Recommendation added",
        "recommendation_id": str(added_recommendation.inserted_id),
    }


@user_recommendation_router.get("/get-recommendations")
async def get_user_recommendations(user_id: str, limit: int, page: int):
    if (
        recommendations := user_recommendation_client["recommendations"]
        .find({"user_id": user_id})
        .sort({"_id": -1})
        .skip((page - 1) * limit)
        .limit(limit)
    ) is not None:
        return {
            "recommendations": list(recommendations),
            "message": "Recommendations retrieved",
        }

    raise HTTPException(status_code=404, detail="Recommendations not found")
