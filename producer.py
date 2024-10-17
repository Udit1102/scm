from confluent_kafka import Producer
import json
import socket
import os
from dotenv import load_dotenv

# Getting broker and server info
load_dotenv()
BROKER_ADDRESS = os.getenv("BROKER_ADDRESS")
HOST_ADDRESS = os.getenv("HOST_ADDRESS")
#BROKER_PORT = int(os.getenv("BROKER_PORT"))
SERVER_PORT = int(os.getenv("SERVER_PORT"))

# Delivery report callback to confirm message delivery
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Initialize Kafka Producer (without serializers)
try:
    producer = Producer({
        'bootstrap.servers': f"{BROKER_ADDRESS}"
    })
except Exception as e:
    print(f"Error initializing the producer: {e}")

# Socket initialization and connection
try:
    s = socket.socket()
    s.connect((HOST_ADDRESS, SERVER_PORT))
except Exception as connection_error:
    print(f"Error connecting to server: {connection_error}")

while True:
    try:
        data = s.recv(1024)
        if not data:
            print("Error: unable to fetch data from server end")
            break
        decoded_data = data.decode('utf-8')
        result = json.loads(decoded_data)
        print("The received data from the server:", result)
        
        # Manually serialize key and value when producing messages
        producer.produce(
            "sensor_data", 
            key="sensor_reading".encode('utf-8'),  # Serialize key
            value=json.dumps(result).encode('utf-8'),  # Serialize value
            callback=delivery_report  # Optional callback to confirm delivery
        )
        producer.flush()  # Ensure the message is sent
        print("Data produced to brokers successfully")
    except Exception as e:
        print(e)

s.close()
