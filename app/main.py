from datetime import datetime, timedelta, timezone
from typing import Union

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from passlib.context import CryptContext
from typing_extensions import Annotated
from dotenv import load_dotenv
import os
import secrets

from models import ShipmentCreation, User, UserInDB, Token, TokenData
from database import db
from functions import get_user, hash_password, password_verification, create_user, authenticate_user

#fetching secret key info
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()
#create access token

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.now(timezone.utc) + expires_delta
	else:
		expire = datetime.now(timezone.utc) + timedelta(minutes=15)
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Could not validate credentials",
		headers={"WWW-Authenticate": "Bearer"},
	)
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		username: str = payload.get("sub")
		if username is None:
			 #{"message": "invalid username None"}
			raise credentials_exception
		token_data = TokenData(username=username)
	except InvalidTokenError:
		raise credentials_exception
	user = await get_user(db, username=token_data.username)
	if user is None:
		#return {"message": "invalid user in get_user call"}
		raise credentials_exception
	return user

#defining the end points

@app.post("/token")
async def login_for_access_token(
	form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
	user = await authenticate_user(db, form_data.username, form_data.password)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
			headers={"WWW-Authenticate": "Bearer"},
		)
	access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	access_token = create_access_token(
		data={"sub": user.username}, expires_delta=access_token_expires
	)
	return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=User)
async def read_users_me(
	current_user: Annotated[User, Depends(get_current_user)],
):
	return current_user


@app.post("/users/create/shipment/")
async def create_shipment(
	shipment: Annotated[ShipmentCreation, Depends()],
	current_user: Annotated[User, Depends(get_current_user)],
):
	shipment_collection = db["shipment"]
	shipment_data = shipment.dict()
	shipment_data["username"] = current_user.username
	await shipment_collection.insert_one(shipment_data)
	return {"message": "Shipment created successfully"}

@app.get("/users/shipments/")
async def read_own_shipments(
	current_user: Annotated[User, Depends(get_current_user)],
):
	shipment_collection = db["shipment"]
	if current_user.role == "User":
		shipment_details = await shipment_collection.find({"username": current_user.username}, {"_id": 0, "username": 0}).to_list(length=None)
	else:
		shipment_details = await shipment_collection.find({}, {"_id": 0}).to_list(length=None)
	if not shipment_details:
		raise HTTPException(status_code=404, detail="No shipments found for the user")
	return {"shipments": shipment_details}

@app.post("/register")
async def user_registration(user: UserInDB):
	if await get_user(db, user.username):
		raise HTTPException(status_code = 400, detail= "This email already exists")
	hashed = hash_password(user.hashed_password)
	user_details = {"first_name": user.first_name, "last_name": user.last_name, "username": user.username, "hashed_password": hashed, "role": user.role}
	await create_user(user_details)
	return {"message": "Registration successful", "status_code": 200}
