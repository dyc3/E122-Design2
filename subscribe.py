#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import datetime
from pathlib import Path

data_path = Path("data")
topics = [x.replace("XXXX", "6754") for x in ["E122/XXXX/Temperature", "E122/XXXX/Humidity", "E122/XXXX/Light"]]
output_paths = dict(zip(topics, [f"{data_path}/{topic.replace('/', '_')}.csv" for topic in topics]))
combined_output = data_path / Path(f"{'_'.join(topics[0].split('/')[:-1])}_combined.csv")

if not data_path.exists():
	data_path.mkdir()

def on_connect(client, userdata, flags, rc):
	print(f"Connected with result code {rc}")
	for topic in topics:
		client.subscribe(topic)

def on_subscribe(client, userdata, mid, granted_qos):
	print(f"Subscribed {mid}")

last_values = dict(zip(topics, [None] * len(topics)))
def on_message(client, userdata, msg):
	global last_values
	topic, payload = msg.topic, int(msg.payload) if "Humidity" in msg.topic else float(msg.payload)
	print(f"{topic}: {payload}")
	with Path(output_paths[topic]).open("a") as f:
		f.write(f"{datetime.datetime.now()},{payload}\n")

	if last_values[topic]:
		# we missed a value, flush these values to file so we don't trash them.
		print("WARN: we are missing a value from one or more of the topics, recording what we have anyway...")
		write_combined_values(last_values)
		last_values = dict(zip(topics, [None] * len(topics)))
	last_values[topic] = payload
	# if none of the values are none, flush to disk and reset the dict
	if all(last_values.values()):
		write_combined_values(last_values)
		last_values = dict(zip(topics, [None] * len(topics)))

def write_combined_values(topic_values):
	if not combined_output.exists():
		combined_output.touch()
	with combined_output.open("a") as f:
		values = [str(topic_values[topic]) for topic in topics]
		out = f"{datetime.datetime.now()},{','.join(values)}\n"
		f.write(out)

def main():
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	client.on_subscribe = on_subscribe
	client.username_pw_set("jojo", "hereboy")
	client.connect("155.246.62.110")

	client.loop_forever()

if __name__ == "__main__":
	main()
