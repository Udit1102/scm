from datetime import datetime, timedelta, timezone
from typing import Union

import jwt
from fastapi import Depends, FastAPI, HTTPException, status, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from typing_extensions import Annotated
from dotenv import load_dotenv
import os

from app.models import ShipmentCreation, User, UserInDB, Token, TokenData, LoginRequest, ResetPassword, NewPassword
from app.database import db
from app.functions import get_user, hash_password, password_verification, create_user, authenticate_user, verify_recaptcha
from app.security import send_mail_for_reset_password, create_access_token, get_current_user, verify_reset_password_token

#access token time
load_dotenv()
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()

# Set up the Jinja2 template directory
templates = Jinja2Templates(directory="app/templates")

# Mount the 'static' folder for serving static files 
app.mount("/static", StaticFiles(directory="app/static"), name="static")

#cors
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],  # Allows all origins, adjust for your needs
	allow_credentials=True,
	allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
	allow_headers=["*"],  # Allows all headers
)

#defining the end points
#serving the signup
@app.get("/", response_class=HTMLResponse)
async def get_signup_page(request: Request):
	return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/register")
async def user_registration(user: UserInDB):
	if await get_user(db, user.username.lower()):
		raise HTTPException(status_code = 400, detail= "This email already exists")
	hashed = hash_password(user.hashed_password)
	user_details = {"first_name": user.first_name, "last_name": user.last_name, "username": user.username.lower(), "hashed_password": hashed, "role": user.role.capitalize()}
	await create_user(user_details)
	return {"message": "Registration successful", "status_code": 200}

# Serve the login.html page
@app.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
	return templates.TemplateResponse("login.html", {"request": request})

@app.post("/token")
async def login_for_access_token(
	form_data: LoginRequest, response: Response
):
	recaptcha_valid = verify_recaptcha(form_data.g_recaptcha_response)
	if not recaptcha_valid:
		raise HTTPException(status_code=400, detail="reCAPTCHA verification failed")

	user = await authenticate_user(db, form_data.username, form_data.password)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
		)
	access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	access_token = create_access_token(
		data={"sub": user.username}, expires_delta=access_token_expires
	)
	# Set the cookie on the response
	response.set_cookie(
		key="access_token", 
		value=access_token, 
		max_age=1800,  # Cookie expires after 30 min
		httponly=True,  # The cookie is HTTP-only
		secure=False,
		samesite="lax"
	)
	return {"message": "Login successful"}

#serving the password reset

@app.get("/forgot_password")
def forgot_password_page(request: Request):
	return templates.TemplateResponse("forgot_password.html", {"request": request})

@app.post("/reset_password")
async def reset_password(email: ResetPassword, request: Request):
	base_url = str(request.base_url)
	if not (await get_user(db, email.email)):
		raise HTTPException(status_code = 404, detail= "This email does not exists")
	reset_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	reset_token = create_access_token(data={"sub": email.email}, expires_delta=reset_token_expires)
	return send_mail_for_reset_password(base_url, email.email, reset_token)

#serving the new password creation

@app.get("/newpassword/page/", response_class= HTMLResponse)
def new_password_page(request: Request, token: str):
	return templates.TemplateResponse("new_password.html", {"request": request, "token":token})

@app.post("/create/newpassword/")
async def create_new_password(data: NewPassword, request: Request):
	user = await verify_reset_password_token(data.token)
	user_collection = db['user']
	hashed = hash_password(data.new_password)
	update_password = await user_collection.update_one({"username": user.username}, {"$set": {"hashed_password": hashed}})
	return {"message": "Your password is updated, please proceed to login"}

#serving the dashboard
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, current_user: Annotated[User, Depends(get_current_user)]):
	return templates.TemplateResponse("dashboard.html", {"request": request, "username": current_user.username})

@app.get("/users/me/", response_model=User)
async def read_users_me(
	current_user: Annotated[User, Depends(get_current_user)],
):
	return current_user

#serving the shipment
@app.get("/create/shipment", response_class=HTMLResponse)
async def create_shipment(request: Request,current_user: Annotated[User, Depends(get_current_user)]):
	return templates.TemplateResponse("shipment_creation.html", {"request": request})

@app.post("/users/create/shipment/")
async def create_shipment(
	shipment: ShipmentCreation,
	current_user: Annotated[User, Depends(get_current_user)],
):
	shipment_collection = db["shipment"]
	shipment_data = shipment.dict()
	shipment_data["username"] = current_user.username
	await shipment_collection.insert_one(shipment_data)
	return {"message": "Shipment created successfully"}

@app.get("/view/shipments", response_class=HTMLResponse)
async def view_shipment(request: Request,current_user: Annotated[User,Depends(get_current_user)]):
	return templates.TemplateResponse("my_shipments_2.html", {"request": request})

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
	return shipment_details

#logout end point
@app.post("/logout")
def logout(response: Response):
	response.delete_cookie(key = 'access_token')
	return {"message": "Logout successful"}

#data stream end point
@app.get("/datastream_page", response_class=HTMLResponse)
def datastream_page(request: Request, current_user: Annotated[User, Depends(get_current_user)]):
	if current_user.role.capitalize() == "User":
		#raise HTTPException(status_code=401, detail="Not Authorized")
		#result = "Not Authorized 401"
		return templates.TemplateResponse("error.html", {"request": request, "status_code": 401, "message": "You are not authorized"})
	return templates.TemplateResponse("datastream.html", {"request": request})

@app.get("/datastream")
async def data_stream(current_user: Annotated[User, Depends(get_current_user)], request: Request):
	if current_user.role.capitalize() == "User":
		#raise HTTPException(status_code=401, detail="Not Authorized")
		#result = "Not Authorized 401"
		return templates.TemplateResponse("error.html", {"request": request, "status_code": 401, "message": "You are not authorized"})
	else:
		data_stream_collection = db['data_stream']
		result = data_stream_collection.find({}, {"_id": 0}).sort([("$natural", -1)]).limit(50)
		result = await result.to_list(length=None)
	return result

#creating user end point
@app.get("/user_creation_page", response_class=HTMLResponse)
def user_creation_page(request: Request, current_user: Annotated[User, Depends(get_current_user)]):
	if current_user.role.capitalize() == "User":
		#raise HTTPException(status_code=401, detail="Not Authorized")
		#result = "Not Authorized 401"
		return templates.TemplateResponse("error.html", {"request": request, "status_code": 401, "message": "You are not authorized"})
	return templates.TemplateResponse("user_creation.html", {"request": request})

@app.post("/createuser")
async def user_creation(user: UserInDB, current_user: Annotated[User, Depends(get_current_user)], request:Request):
	if current_user.role.capitalize() == "User":
		#raise HTTPException(status_code=401, detail="Not Authorized")
		return templates.TemplateResponse("error.html", {"request": request, "status_code": 401, "message": "You are not authorized"})
	if await get_user(db, user.username.lower()):
		raise HTTPException(status_code = 400, detail= "This email already exists")
	hashed = hash_password(user.hashed_password)
	user_details = {"first_name": user.first_name, "last_name": user.last_name, "username": user.username.lower(), "hashed_password": hashed, "role": user.role.capitalize()}
	await create_user(user_details)
	return {"message": "User created successfully", "status_code": 200}
