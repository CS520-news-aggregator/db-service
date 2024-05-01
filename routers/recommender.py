from fastapi import APIRouter, Depends, HTTPException
from models.utils.constants import RECOMMENDER_HOST
from routers.user import auth_manager
from models.utils.funcs import Response, get_data_from_api


recommender_router = APIRouter(prefix="/recommender")


@recommender_router.get("/get-recommendations")
def get_recommendations(user=Depends(auth_manager), limit: int = 5):
    if (
        recommendations := get_data_from_api(
            RECOMMENDER_HOST,
            "recommender/get-recommendations",
            {"user_id": user["id"], "limit": limit},
        )
    ) == Response.FAILURE:
        raise HTTPException(status_code=400, detail="Could not get recommendations")

    return recommendations
