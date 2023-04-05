import RPi.GPIO as GPIO
import time
import random
from paho.mqtt import client as mqtt_client
import credentials

# Set which GPIO pins will handle each input
START_LED = 38
LOCK_LED  = 36
SPIN_LED  = 32
DONE_LED  = 26

# Setup MQTT
broker = 'homeassistant.local'
port = 1883
roottopic = "WashingMachine/"
statetopic = "PowerState/0"
availablitytopic = "Available"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'

# Configure GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(START_LED, GPIO.IN)
GPIO.setup(LOCK_LED, GPIO.IN) 
GPIO.setup(SPIN_LED, GPIO.IN) 
GPIO.setup(DONE_LED, GPIO.IN)

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.publish(roottopic + availablitytopic,"Online")
        else:
            print("Failed to connect, return code %d\n", rc)
            client.publish(roottopic + availablitytopic,"Offline")

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.will_set(roottopic + availablitytopic, payload="Offline", qos=0, retain=True)
    client.username_pw_set(credentials.username,credentials.password)
    client.connect(broker, port)
    return client


def publish(client):
    while True:
        time.sleep(1)
        if GPIO.input(DONE_LED):
          msg = "ON"
        else:
          msg = "OFF"

        result = client.publish(roottopic + statetopic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{roottopic}`")
        else:
            print(f"Failed to send message to topic {roottopic}")


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    # time.sleep(300)
    run()