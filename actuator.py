from collections import OrderedDict
from datetime import datetime
import json

import pandas
import RPi.GPIO as GPIO
from DHT11_Python import dht11

DHT_NUMBER = 14


def get_actuator_dict():
    """
    get temperature and humidity from actuator.
    return OrderedDict
    {
        "temperature":
        "humidity":
        "location":
        "datetime":
    }
    """
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    instance = dht11.DHT11(pin=DHT_NUMBER)
    result = instance.read()
    read_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if result.is_valid():
        output_json(read_datetime, result.temperature, result.humidity)
        output_csv(read_datetime, result.temperature, result.humidity)
    GPIO.cleanup()
    with open('./json/actuator.json', 'r', encoding='utf-8') as f:
        return json.load(f, object_pairs_hook=OrderedDict)


def output_json(read_datetime, temperature, humidity):
    output_dict = OrderedDict()
    output_dict['temperature'] = temperature
    output_dict['humidity'] = humidity
    output_dict['location'] = 'Tokyo'
    output_dict['datetime'] = read_datetime
    with open('./json/actuator.json', 'w', encoding='utf-8') as f:
        json.dump(output_dict, f, indent=4, ensure_ascii=False)


def output_csv(read_datetime, temperature, humidity):
    add_data = pandas.DataFrame([[read_datetime, temperature, humidity]])
    add_data.to_csv('./csv/actuator.csv',
                    index=False, mode='a', header=False)
