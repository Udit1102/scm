from app.models import UserInDB
from passlib.context import CryptContext
from app.database import db
from dotenv import load_dotenv
import os
import requests


load_dotenv
RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")


#initializing the password context
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

#defining functions

#google recaptcha function

def verify_recaptcha(recaptcha_response: str):
	payload = {
		'secret': RECAPTCHA_SECRET_KEY,
		'response': recaptcha_response
	}
	
	# Send the request to Google's reCAPTCHA API
	response = requests.post("https://www.google.com/recaptcha/api/siteverify", data=payload)
	result = response.json()
	
	# Return whether the reCAPTCHA was successful
	return result.get("success", False)

##function for password hashing and verification

def hash_password(password):
	hashed = pwd.hash(password)
	return hashed

def password_verification(password, hashed):
	verified = pwd.verify(password, hashed)
	return verified

##creating the user

async def create_user(user_details: dict):
	user_collection = db['user']
	await user_collection.insert_one(user_details)

##checking if user exists

async def get_user(db, username: str):
	user_collection = db['user']
	user_dict = await user_collection.find_one({"username": username})
	if not user_dict:
		return False
	return UserInDB(**user_dict)


async def authenticate_user(db, username: str, password: str):
	user = await get_user(db, username)
	if not user:
		return False
	if not password_verification(password, user.hashed_password):
		return False
	return user

async def create_shipment(shipment: dict):
	shipment_collection = db['shipment']
	status = await shipment_collection.find_one({"shipment_no": shipment['shipment_no']})
	if status:
		return {"message": "shipment already exists"}
	await shipment_collection.insert_one(shipment)
	return {"message": "shipment created successfully"}

async def get_shipment(username: str):
	shipment_collection = db['shipment']
	shipment_details = await shipment_collection.find({"username": username})
	return shipment_details