from contextlib import asynccontextmanager

from dotenv import dotenv_values
from fastapi import FastAPI
from pymongo import MongoClient

config = dotenv_values(".env")


def get_mongo_client():
    return MongoClient(config["ATLAS_URI"])


def change_db_id_to_str(data):
    if data:
        data["id"] = str(data["_id"])
    return data
