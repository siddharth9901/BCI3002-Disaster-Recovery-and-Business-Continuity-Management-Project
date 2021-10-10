from fastapi import APIRouter, Body, HTTPException, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from .models import User, Login, Token, TokenData
from .hashing import Hash

router = APIRouter()

@router.post("/login")
async def login(request: Request, user_to_login: Login = Body(...)):
	user = await request.app.mongodb["users"].find_one({"username":user_to_login.username})
	if not user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'No user found with this {user_to_login.username} username')
	if not Hash.verify(user["password"],user_to_login.password):
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'Wrong Username or password')

	return {"login": "successful"}


#signup
@router.post("/signup", response_description="Signup for a new user")
async def create_user(request: Request, user: User = Body(...)):
    user = jsonable_encoder(user)
    user["following"] = []
    user["posts_id"] = []
    user["followers"] = []
    user["followers_count"] = 0
    user["following_count"] = 0
    hashed_pass = Hash.bcrypt(user["password"])
    user["password"] = hashed_pass
    new_user = await request.app.mongodb["users"].insert_one(user)
    created_user = await request.app.mongodb["users"].find_one(
        {"_id": new_user.inserted_id}
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)
