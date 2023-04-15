import time
import requests
# УДАЛИТЬ
# Как я понимаю, делая запросы на localhost:5000 код делает запрос к самому датчику, данные о влажности находятся по пути localhost:5000/soil_moisture/<какое-то число>
#
# УДАЛИТЬ

# Настройки Wi-Fi соединения
ssid = "ваш_SSID_роутера"
password = "ваш_пароль_роутера"

# Адрес сервера, на который будут отправляться данные
server_address = "адрес_вашего_сервера"

# Номер пина, на котором подключен датчик влажности почвы FC-28
soil_moisture_pin = 0

# Номер датчика в секте по горизонтали
x_cord = 1

# Номер датчика в секте по вертикале
y_cord = 1

# Функция для получения показаний датчика влажности почвы
def get_soil_moisture():
    response = requests.get(f"http://localhost:5000/soil_moisture/{soil_moisture_pin}")
    if response.status_code == 200:
        return response.json().get("soil_moisture")
    return None

# Настройка соединения с Wi-Fi
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

# Бесконечный цикл считывания показаний и отправки на сервер
# Sends to remote server value on soil moisture and
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