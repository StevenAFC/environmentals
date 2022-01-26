import Adafruit_DHT
import time
import paho.mqtt.publish as mqtt
import json

broker = '192.168.86.50'
port = 1883
topic = "lakeside/garage/atmosphere"
client_id = 'garage-temp-mqtt-01'
username = 'mqtt_admin'
password = 'f2VmlM3pX]W,Yjf'

sensor_data = {'temperature': 0, 'humidity': 0}


def readDHTDevice():
    DHT_SENSOR = Adafruit_DHT.DHT22
    DHT_PIN = 4

    return Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)


def getAtmosphere():
    attempts = 0
    while attempts < 3:
        try:
            humidity, temperature = readDHTDevice()

            if humidity is not None and temperature is not None and humidity < 150 and temperature < 150:
                return {'temperature': temperature, 'humidity': humidity}
            else:
                print(
                    "Reading from sensor invalid trying again attempt {} of 3".format(attempts + 1))
        except Exception as e:
            print(e)

        attempts += 1


starttime = time.time()
while True:
    result = getAtmosphere()

    if result:
        temperature = round(result['temperature'], 1)
        humidity = round(result['humidity'], 1)

        sensor_data['temperature'] = temperature
        sensor_data['humidity'] = humidity

        mqtt.single(
            topic,
            json.dumps(sensor_data),
            hostname=broker,
            client_id=client_id,
            auth={'username': username, 'password': password}
        )

    time.sleep(300.0 - ((time.time() - starttime) % 300.0))
