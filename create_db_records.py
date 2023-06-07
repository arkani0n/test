import json
import requests
import random
from my_credentials import username,password


number_of_sensors_in_row = 10
number_of_sensors_in_column = 10

moisture_value_range = [0, 100]

number_of_loops = 1

web_server_address = "http://localhost:8060"

def get_color(moisture_value):
    if moisture_value >= 0 and moisture_value < 40:
        return "red"
    elif moisture_value >= 40 and moisture_value <= 69:
        return "yellow"
    else:
        return "green"

for loop in range(number_of_loops):
    for row in range(number_of_sensors_in_row):
        for col in range(number_of_sensors_in_column):
            moisture_value = random.randint(moisture_value_range[0], moisture_value_range[1])
            color = get_color(moisture_value)

            payload = {
                "moisture_value": moisture_value,
                "x_cord": col + 1,
                "y_cord": row + 1,
                "color": color,
                "username": username,
                "password": password


            }

            r = requests.post(
                web_server_address,
                data=json.dumps(payload)
            )

            print(f"Response: {r.text}\nAdded moisture value {payload['moisture_value']} on coord {payload['x_cord']}, {payload['y_cord']}, color: {payload['color']}, username: {payload['username']}, password: {payload['password']}")
