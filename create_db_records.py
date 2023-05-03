import json

import requests
import random
# localhost:8060 -d '{
#             "moisture_value": 8,
#             "x_cord": 2,
#             "y_cord": 2
#                 }'
number_of_sensors_in_row = 10
number_of_sensors_in_column = 10

moisture_value_range = [0, 100]

number_of_loops = 5

web_server_address = "http://localhost:8060"

for loop in range(number_of_loops):

    for row in range(number_of_sensors_in_row):
        for col in range(number_of_sensors_in_column):
            payload = {
                "moisture_value": random.randint(
                    moisture_value_range[0],
                    moisture_value_range[1]
                ),
                "x_cord": col+1,
                "y_cord": row+1
            }
            r = requests.post(
                          web_server_address,
                          data=json.dumps(payload),

                          )
            print(f"Response:{r.text}\nAdded moist value {payload['moisture_value']} on coord {payload['x_cord']}, {payload['y_cord']}")
