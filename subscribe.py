#!/usr/bin/env python3
import paho.mqtt.client as mqtt

topics = [x.replace("XXXX", "6754") for x in ["E122/XXXX/Temperature", "E122/XXXX/Humidity", "E122/XXXX/Light"]]

def on_connect(client, userdata, flags, rc):
	print(f"Connected with result code {rc}")
	for topic in topics:
		client.subscribe(topic)

def on_subscribe(client, userdata, mid, granted_qos):
	print(f"Subscribed {mid}")

def on_message(client, userdata, msg):
	topic, payload = msg.topic, int(msg.payload) if "Humidity" in msg.topic else float(msg.payload)
	print(f"{topic}: {payload}")

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
