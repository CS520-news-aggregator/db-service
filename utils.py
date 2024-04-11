from contextlib import asynccontextmanager

from dotenv import dotenv_values
from fastapi import FastAPI
from pymongo import MongoClient

config = dotenv_values(".env")


def get_mongo_client():
   return MongoClient(config["ATLAS_URI"])
