from fastapi import APIRouter, Depends, HTTPException
from routers.user import auth_manager
import requests
import os


recommender_router = APIRouter(prefix="/recommender")


@recommender_router.get("/get-recommendations")
def get_recommendations(user=Depends(auth_manager), limit: int = 10):
    RECOMMENDER_HOST = os.getenv("RECOMMENDER_HOST", "localhost")
    recommender_url = f"http://{RECOMMENDER_HOST}:8030/recommender/get-recommendations"

    try:
        response = requests.get(
            recommender_url,
            params={"user_id": user["id"], "limit": limit},
            timeout=30,
        )
    except requests.exceptions.RequestException:
        return {"message": "Could not send data to recommender service due to timeout"}

    if response.status_code != 200:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {response.text}"
        )

    return response.json()
