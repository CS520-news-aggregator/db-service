from fastapi import APIRouter, Body, Depends, HTTPException, Request
from models.user import RegisterUser, LoginUser, Token, Preferences
from fastapi_login import LoginManager
from passlib.context import CryptContext
from fastapi.encoders import jsonable_encoder
from datetime import timedelta
from utils import get_mongo_client

user_router = APIRouter(prefix="/user")

auth_manager = LoginManager("SECRET_KEY", "/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

user_client = get_mongo_client()["user"]


@auth_manager.user_loader()
def query_user(email_address: str):
    user = user_client["users"].find_one({"email_address": email_address})
    user["id"] = str(user.pop("_id"))
    return user


@user_router.post("/register")
async def register_user(_: Request, reg_user: RegisterUser = Body(...)):
    if user_client["users"].find_one({"email_address": reg_user.email_address}):
        raise HTTPException(status_code=401, detail="User already exists")

    user_data = jsonable_encoder(reg_user)
    user_data["hashed_password"] = pwd_context.hash(user_data.pop("password"))
    res_user = user_client["users"].insert_one(user_data)

    return {
        "message": "User created",
        "token": create_token(user_data, str(res_user.inserted_id)),
    }


@user_router.post("/login")
def login(_: Request, data: LoginUser = Body(...)):
    if not (
        user := user_client["users"].find_one({"email_address": data.email_address})
    ):
        raise HTTPException(status_code=401, detail="User not found")

    if not pwd_context.verify(data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return {"message": "Logged in", "token": create_token(user, str(user["_id"]))}


@user_router.get("/view")
async def view_user(user=Depends(auth_manager)):
    return {"message": "User is logged in", "user": user}


@user_router.get("/get-all-users")
async def get_all_users():
    return [str(user["_id"]) for user in user_client["users"].find()]


def create_token(user, user_id: str):
    for token in user_client["tokens"].find({"user_id": user_id}):
        user_client["tokens"].delete_one({"_id": token["_id"]})

    access_token = auth_manager.create_access_token(
        data={"sub": user["email_address"]}, expires=timedelta(days=14)
    )

    token = Token(user_id=user_id, token=access_token)
    user_client["tokens"].insert_one(jsonable_encoder(token))
    return access_token


@user_router.post("/add-preferences")
def add_preferences(user=Depends(auth_manager), prefs: Preferences = Body(...)):
    if user_client["preferences"].find_one({"user_id": user["id"]}):
        raise HTTPException(status_code=401, detail="User-preferences already exists")

    user_prefs = jsonable_encoder(prefs)
    user_prefs["user_id"] = user["id"]
    res_prefs = user_client["preferences"].insert_one(user_prefs)
    return {
        "message": "Preferences have been added",
        "prefs_id": str(res_prefs.inserted_id),
    }


@user_router.get("/get-preferences")
def get_preferences(user=Depends(auth_manager)):
    prefs = user_client["preferences"].find_one({"user_id": user["id"]})
    return {
        "message": "This the list of user preferences",
        "preferences": jsonable_encoder(prefs["preferences"]),
    }
