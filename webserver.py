import datetime
import json
import random
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import sqlite3


hostName = "localhost"
serverPort = 8060

class FieldServer(HTTPServer):
    def __init__(self, *args, **kwargs):
        super(FieldServer, self).__init__(*args, **kwargs)
        self.init_database()

    def init_database(self):
        sqliteConnection = sqlite3.connect('sql.db')
        self.cursor = sqliteConnection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS sensor_data("
                            "x_cord int,"
                            "y_cord int,"
                            "moisture_value float,"
                            "timestamp timestamp )"
                            )
        result = self.cursor.fetchall()
        print(f"Table init result: {result}")
        sqliteConnection.close()


class MyServer(BaseHTTPRequestHandler):

    def do_POST(self):

        try:
            content_len = int(self.headers.get('Content-Length'))
            post_body = json.loads(self.rfile.read(content_len))
            print(f"Request: {self.requestline}, \nData:{post_body}")
            self.connect_to_database()
            self.add_data_to_list(post_body)
            self.successful_response()
        except Exception as e:
            print(f"During request handling error occurred{e}")
            self.unsuccessful_response()
        # self.add_data_to_list(post_body)

    def successful_response(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("Successful Response", "utf-8"))

    def unsuccessful_response(self):
        self.send_response(500)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("Unsuccessful Response", "utf-8"))

    def connect_to_database(self):
        self.sqliteConnection = sqlite3.connect('sql.db')
        self.cursor = self.sqliteConnection.cursor()

    def add_data_to_list(self,data):
        insert_data = f"{data['x_cord']}, {data['y_cord']}, {data['moisture_value']}, \'{datetime.datetime.now()}\'"
        try:
            self.cursor.execute(f"INSERT INTO sensor_data (x_cord, y_cord, moisture_value, timestamp) VALUES ({insert_data})")
            self.sqliteConnection.commit()
            result = self.cursor.fetchone() #TODO Not retirning the result of insert
            print(f"Insert of values {insert_data} \n resulted with: {result}")
        except sqlite3.Error as error:
            print(f"Durring insert of values: {insert_data} \nError occurred - {error}")
        finally:
            self.sqliteConnection.close()


webServer = FieldServer((hostName, serverPort), MyServer)
print("Server started http://%s:%s" % (hostName, serverPort))

try:
    webServer.serve_forever()
except KeyboardInterrupt:
    pass

webServer.server_close()
print("Server stopped.")
