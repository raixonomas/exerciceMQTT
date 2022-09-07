import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("536/fond/#")

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if(msg.topic == "536/fond/humidity"):
        if(float(str(msg.payload).replace("'", "").replace("b", "")) > 55):
            GPIO.output(23, GPIO.HIGH)
            GPIO.output(18, GPIO.LOW)
        else:
            GPIO.output(18, GPIO.HIGH)
            GPIO.output(23, GPIO.LOW)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("10.4.1.181", 1883, 60)
client.loop_forever()
