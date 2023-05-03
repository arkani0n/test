import time
import requests


# Как я понимаю, делая запросы на localhost:5000 код делает запрос к самому датчику, данные о влажности находятся по пути localhost:5000/soil_moisture/<какое-то число>
# ^ Заметки от Арканиона

# Wi-Fi connection setup
ssid = "ваш_SSID_роутера"
password = "ваш_пароль_роутера"

# Address of remote server
server_address = "адрес_вашего_сервера"

# Pin number, on which moisture sensor FC-28 is connected
soil_moisture_pin = 0

# Sensor coords, please change for every sensor
x_cord = 1
y_cord = 1

def get_soil_moisture():
    response = requests.get(f"http://localhost:5000/soil_moisture/{soil_moisture_pin}")
    if response.status_code == 200:
        return response.json().get("soil_moisture")
    return None

print("Connecting to Wi-Fi...")
while True:
    try:
        response = requests.get(f"http://localhost:5000/wifi/{ssid}/{password}")
        if response.status_code == 200:
            print("Connected to Wi-Fi")
            break
    except:
        pass
    time.sleep(1)

# Sends to remote server value on soil moisture every 10 seconds (to change the delay, change time.sleep(DELAY_NUMBER_IN_SECONDS, in line 53)
while True:
    soil_moisture = get_soil_moisture()
    if soil_moisture is not None:
        data = {
            "moisture_value": soil_moisture,
            "x_cord": x_cord,
            "y_cord": y_cord
                }
        response = requests.post(f"http://{server_address}/api/data", data=data)
        if response.status_code == 200:
            print("Data sent to server")
        else:
            print("Connection to server failed")
    time.sleep(10)