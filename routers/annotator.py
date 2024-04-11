from fastapi import APIRouter, Body, Depends
from fastapi import Depends, APIRouter
from utils import get_mongo_client
from routers.user import auth_manager

annotator_router = APIRouter(prefix="/annotator")
annotator_client = get_mongo_client()["annotator"]


@annotator_router.post("/add-annotation")
def annotate_text(user=Depends(auth_manager)):
    return {"message": "Added text annotation"}


@annotator_router.get("/get-annotation")
def get_annotations(user=Depends(auth_manager)):
    return {"message": "Retrieved annotations"}
