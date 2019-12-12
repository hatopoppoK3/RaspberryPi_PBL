from collections import OrderedDict

from flask import Flask, render_template, jsonify
from flask import request

from actuator import get_actuator_dict
from led import turn_on_led, turn_off_led


app = Flask(__name__)
COOLER_NUMBER = 7
HEATER_NUMBER = 25
DRYER_NUMBER = 8


@app.route('/')
def index():
    output_dict = OrderedDict()
    output_dict = get_actuator_dict()
    temperature = output_dict['temperature']
    humidity = output_dict['humidity']
    location = output_dict['location']
    datetime = output_dict['datetime']
    return render_template('index.html', temperature=temperature,
                           humidity=humidity,
                           location=location,
                           datetime=datetime)


@app.route('/action/', methods=['GET', 'POST'])
def conditioner_action():
    """
    get data from post methods.
    """
    request_temperature = float(request.form['temperature'])
    request_humidity = float(request.form['humidity'])
    request_action = str(request.form['request_action'])
    actuator_dict = get_actuator_dict()
    temperature = actuator_dict['temperature']
    humidity = actuator_dict['humidity']
    action_flag = 'do'
    if request_action == 'cooler':
        if request_temperature < temperature:
            turn_on_led(COOLER_NUMBER)
        else:
            action_flag = 'undo'
            turn_off_led()
    elif request_action == 'heater':
        if temperature < request_temperature:
            turn_on_led(HEATER_NUMBER)
        else:
            action_flag = 'undo'
            turn_off_led()
    else:
        if request_humidity < humidity:
            turn_on_led(DRYER_NUMBER)
        else:
            action_flag = 'undo'
            turn_off_led()
    return render_template('led.html', temperature=temperature,
                           humidity=humidity,
                           request_action=request_action,
                           request_temperature=request_temperature,
                           request_humidity=request_humidity,
                           action_flag=action_flag)


@app.route('/output/json/')
def output_json():
    return jsonify(get_actuator_dict())


if __name__ == '__main__':
    try:
        app.run()
    except KeyboardInterrupt:
        turn_off_led()
