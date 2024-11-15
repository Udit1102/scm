import os
import socket
import json
from dotenv import load_dotenv
from random import random
import time
from datetime import datetime

#server port
load_dotenv()
SERVER_PORT = os.getenv("SERVER_PORT")

#intializing the socket
s = socket.socket()
print("Socket Created")
s.bind(('',int(SERVER_PORT)))
s.listen(3)
print("waiting for connections")
c, addr = s.accept()

while True:
	try:
		data =[{
"Time": datetime.now().strftime("%d-%m-%y %H:%M:%S"),
"Battery_Level": 3.57,
 "Device_Id":1156053076,
 "First_Sensor_temperature":28,
 "Route_From":"Hyderabad, India",
 "Route_To":"Louisville, USA"
 },
{
"Time": datetime.now().strftime("%d-%m-%y %H:%M:%S"),
"Battery_Level":2.8,
 "Device_Id":1156053077,
 "First_Sensor_temperature":48,
 "Route_From":"Banglore, India",
 "Route_To":"Louisville, USA"
}]

		print("connected with", addr)
		userdata = (json.dumps(data)+"\n").encode('utf-8')
		print(userdata.decode('utf-8'))
		c.send(userdata)
		time.sleep(10)
	except Exception as e:
		print(e)
c.close()