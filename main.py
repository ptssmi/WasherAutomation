import RPi.GPIO as GPIO
import time
import random
from paho.mqtt import client as mqtt_client
import credentials

# Configure GPIO
GpioArray = [26,36,32,38,40,37]
GPIO.setmode(GPIO.BOARD)
GPIO.setup(GpioArray, GPIO.IN)

# Setup MQTT
broker           = 'homeassistant.local'
port             = 1883
roottopic        = "WashingMachine/"
availablitytopic = "Available"
StatusTopicArray = ["Sense","Wash","Rinse","Spin","Done","Lock"]

# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'

# Fetch the state of the GPIO pin
def fetch_gpio(LED):
    if GPIO.input(LED):
        return "ON"
    else:
        return "OFF"

# Connect to MQTT on homeassistant.local broker
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

# Publish the GPIO states to MQTT
def publish(client):
    while True:
        # Loop through all GPIO and report state
        for i in range(len(StatusTopicArray)):
            msg = fetch_gpio(GpioArray[i])
            result = client.publish(roottopic + StatusTopicArray[i], msg)
            # Check if message was sent properly
            status = result[0]
        # Delay update by 1 second
        time.sleep(1)

# Run script
def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

# Main function
if __name__ == '__main__':
    # Add delay to allow Raspberry PI to boot
    time.sleep(300)
    run()