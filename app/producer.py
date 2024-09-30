from kafka import KafkaProducer
import json
import socket

producer = KafkaProducer(
	bootstrap_servers = '127.0.0.1:9092',
	key_serializer = lambda k: k.encode('utf-8'),
	value_serializer = lambda v: json.dumps(v).encode('utf-8')
	)

#socket initialization and connection

s = socket.socket()
s.connect(('127.0.0.1', 12345))

while True:
	try:
		data = s.recv(1024)
		if not data:
			break
		decoded_data = data.decode('utf-8')
		result = json.loads(decoded_data)
		print("the received data from the server:", result)
		producer.send("sensor_data", key= "sensor_reading", value= result)
		print("Data produced to brokers successfully")
	except Exception as e:
		print(e)

s.close()