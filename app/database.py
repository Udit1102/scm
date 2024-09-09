from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import asyncio
import urllib.parse

load_dotenv()
#loading variables

db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_encoded_password = urllib.parse.quote(db_password)

#connection string

mongo_uri = f"mongodb+srv://{db_user}:{db_encoded_password}@scm.oduo3.mongodb.net/?retryWrites=true&w=majority&appName=SCM"
print(mongo_uri)

# Create an AsyncIOMotorClient instance
client = AsyncIOMotorClient(mongo_uri)

# Access a specific database
db = client['my_scm']

'''
user_collection = db['user']
shipment_collection = db['shipment']

async def user_creation():
    data = {"name": "temp", "email": "temp"}
    result = await user_collection.insert_one(data)
    print(f"success insertion {result.inserted_id}")

loop = asyncio.get_event_loop()
loop.run_until_complete(user_creation())

# Example async function to test the connection
async def test_connection():
    # List all the collections in the database
    collections = await db.list_collection_names()
    print("Collections in the database:", collections)

# Run the async test function
loop = asyncio.get_event_loop()
loop.run_until_complete(test_connection())
'''