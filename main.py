from collections import OrderedDict

from flask import Flask, render_template, jsonify
from flask import request

from actuator import get_actuator_dict
from led import turn_on_led, turn_off_led


app = Flask(__name__)
cooler_number = None
heater_number = None
dryer_number = None


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
    action_type = str(request.form['action_type'])
    actuator_dict = get_actuator_dict()
    temperature = actuator_dict['temperature']
    humidity = actuator_dict['humidity']
    action_flag = 'do'
    if action_type == 'cooler':
        if request_temperature < temperature:
            turn_on_led(cooler_number)
        else:
            action_flag = 'undo'
            turn_off_led()
    elif action_type == 'heater':
        if temperature < request_temperature:
            turn_on_led(heater_number)
        else:
            action_flag = 'undo'
            turn_off_led()
    else:
        if request_humidity < humidity:
            turn_on_led(dryer_number)
        else:
            action_flag = 'undo'
            turn_off_led()
    return render_template('led.html', action_type=action_type,
                           action_flag=action_flag,
                           request_temperature=request_temperature,
                           temperature=temperature,
                           request_humidity=request_humidity,
                           humidity=humidity)


@app.route('/output/json/')
def output_json():
    return jsonify(get_actuator_dict())


if __name__ == '__main__':
    try:
        app.run()
    except KeyboardInterrupt:
        turn_off_led()
