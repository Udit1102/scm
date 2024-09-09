from models import UserInDB
from passlib.context import CryptContext
from database import db
#initializing the password context
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

#defining functions
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