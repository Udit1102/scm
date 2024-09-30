from kafka import KafkaConsumer
import json

def message_consumption():
	consumer = KafkaConsumer(
	"sensor_data",
	bootstrap_servers = '127.0.0.1:9092',
	auto_offset_reset = 'earliest',
	group_id = "my_scm",
	key_deserializer = lambda k: k.decode('utf-8'),
	value_deserializer = lambda v: json.loads(v) #.decode('utf-8')
)

#message consumption

	for message in consumer:
    		return {"key": message.key, "message": message.value}