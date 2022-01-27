import os
from dotenv import load_dotenv
import adafruit_dht
import board
import time
import paho.mqtt.publish as mqtt
import json

load_dotenv()

dht_device = adafruit_dht.DHT22(board.D4)

def readDHTDevice():
  try:
    temperature = dht_device.temperature
    humidity = dht_device.humidity

  except RuntimeError as error:
    print("readDHTDevice - RuntimeError - {}".format(error.args[0]))
    time.sleep(2.0)
    return False

  except Exception as error:
    print("readDHTDevice - Exception - {}".format(error.args[0]))
    time.sleep(2.0)
    return False

  return temperature, humidity 


def getReading():
  for i in range(3):
    reading = readDHTDevice()

    if reading:
      temperature, humidity = readDHTDevice()

      if humidity is not None and temperature is not None and humidity < 150 and temperature < 100:
        return temperature, humidity
      else:
        print("Reading from sensor invalid trying again attempt {} of 3".format(attempts + 1))
        time.sleep(1.0)

  return False

def generateAverage():
  temperatureCumulative = 0
  humidityCumulative = 0
  readingCount = 0

  for i in range(3):
    reading = getReading()
    if reading:
      temperature, humidity = reading
      temperatureCumulative += temperature
      humidityCumulative += humidity
      readingCount += 1

    time.sleep(1.0)

  if readingCount == 0: return False
  return round(temperatureCumulative / readingCount, 1), round(humidityCumulative / readingCount, 1)

while True:
  reading = generateAverage()

  if reading:
    temperature, humidity = reading

    mqtt.single(
      os.environ['MQTT_TOPIC'],
      json.dumps({'temperature': temperature, 'humidity': humidity}),
      hostname=os.environ['MQTT_BROKER_HOST'],
      port=int(os.environ['MQTT_BROKER_PORT']),
      client_id=os.environ['MQTT_CLIENT_ID'],
      auth={'username': os.environ['MQTT_USERNAME'], 'password': os.environ['MQTT_PASSWORD']}
    )

    time.sleep(float(os.environ['REFRESH_TIME']))
  else:
    time.sleep(100.0)
