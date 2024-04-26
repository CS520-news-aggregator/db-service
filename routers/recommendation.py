from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from models.recommendation import Recommendation
from utils import get_mongo_client

recommendation_router = APIRouter(prefix="/recommendation")
recommendation_client = get_mongo_client()["recommendation"]


@recommendation_router.post("/add-recommendation")
async def add_recommendation(recommendation: Recommendation = Body(...)):
    recommendation_dict = jsonable_encoder(recommendation)

    added_recommendation = recommendation_client["recommendations"].insert_one(
        recommendation_dict
    )

    return {
        "message": "Recommendation added",
        "recommendation_id": str(added_recommendation.inserted_id),
    }


@recommendation_router.get("/get-recommendations")
async def get_recommendations(user_id: str):
    if (
        recommendations := recommendation_client["recommendations"].find(
            {"user_id": user_id}
        )
    ) is not None:
        return {
            "recommendations": list(recommendations),
            "message": "Recommendations retrieved",
        }

    raise HTTPException(status_code=404, detail="Recommendations not found")
