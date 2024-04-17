from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from utils import get_mongo_client
from models.annotator import Annotation

annotator_router = APIRouter(prefix="/annotator")
annotator_client = get_mongo_client()["annotator"]


@annotator_router.post("/add-annotation")
def add_annotations(annotation: Annotation = Body(...)):
    if get_topics(annotation.post_id) is not None:
        raise HTTPException(
            status_code=400, detail="Annotation with same post_id already exists"
        )

    annotation_data = jsonable_encoder(annotation)
    res_annotation = annotator_client["topics"].insert_one(annotation_data)
    return {
        "message": "Added text annotation",
        "annotation_id": str(res_annotation.inserted_id),
    }


@annotator_router.get("/get-annotation")
def get_annotations(post_id: str):
    annotations = get_topics(post_id)
    return {
        "message": "Retrieved annotations",
        "annotations": jsonable_encoder(annotations),
    }


def get_topics(post_id: str):
    annotations = annotator_client["topics"].find_one({"post_id": post_id})
    return annotations
