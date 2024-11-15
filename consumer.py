from confluent_kafka import Consumer
import pymongo
import urllib.parse
import json
from dotenv import load_dotenv
import os

# Getting broker info
load_dotenv()
BROKER_ADDRESS = os.getenv("BROKER_ADDRESS")
#BROKER_PORT = os.getenv("BROKER_PORT")

# Setting up database and collection
try:
	db_user = os.getenv("db_user")
	db_password = os.getenv("db_password")
	db_encoded_password = urllib.parse.quote(db_password)

# Connection string
	mongo_uri = f"mongodb+srv://{db_user}:{db_encoded_password}@scm.oduo3.mongodb.net/?retryWrites=true&w=majority&appName=SCM"

# Create an pymongo Client instance
	client = pymongo.MongoClient(mongo_uri)

# Access a specific database
	db = client['my_scm']
	data_stream_collection = db['data_stream']
except Exception as e:
	print(f"error initializing the database: {e}")

# Initializing the consumer
try:
	consumer = Consumer({
		'bootstrap.servers': f'{BROKER_ADDRESS}',
		'group.id': 'my_scm',
		'auto.offset.reset': 'earliest'
	})
	consumer.subscribe(['sensor_data'])  # Subscribe to the topic
except Exception as e:
	print(f"Error initializing the consumer: {e}")

# Message consumption
def consume_messages():
	try:
		while True:
			message = consumer.poll(1.0)  # Poll for new messages
			if message is None:
				continue
			if message.error():
				print(f"Error while consuming: {message.error()}")
				continue
			
			# Deserialize 
			key = message.key().decode('utf-8') if message.key() else None
			value = json.loads(message.value().decode('utf-8')) if message.value() else None
			# Insert data into MongoDB
			data_stream_collection.insert_many(value)
			print(f"Data received and inserted into DB: {value}")
	except Exception as e:
		print(f"error fetching the messages {e}")
	finally:
		consumer.close()  # Clean up the consumer

# Run the consumer
if __name__ == "__main__":
	consume_messages()
