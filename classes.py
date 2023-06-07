import datetime
import json
import random
import time
import sqlite3

class Field:
    def __init__(self, length, width, sensor_radius):

        self.length = length
        self.width = width
        self.sensor_radius = sensor_radius

        sensor_diameter = sensor_radius * 2
        if length % sensor_diameter == 0:
            self.number_of_rows = length // sensor_diameter
        else:
            self.number_of_rows = length // sensor_diameter + 1

        if width % sensor_diameter == 0:
            self.number_of_column = width // sensor_diameter
        else:
            self.number_of_column = width // sensor_diameter + 1

        self.sensor_list = self.create_list()


    def create_list(self):

        sensor_list = [[] for row in range(self.number_of_rows) ]
        for row in range(self.number_of_rows):
            for column  in range(self.number_of_column):
                sensor_list[row].append(f"{row+1}_{column+1}")
                # format sensor_list[
                #   [
                #    x_y,
                #    x_y, ..
                #   ]
                # ]
        return sensor_list

    def get_moisture_map(self, sensor_cords, start_time_delta_dict, end_time_delta_dict, username, password):
        # time_delta_dict = { STRUCTURE
        #   "days"    : int
        #   "hours"   : int
        #   "minutes" : int
        # }

        sqliteConnection = sqlite3.connect('sql.db')
        cursor = sqliteConnection.cursor()

        from_time = datetime.datetime.now() - datetime.timedelta(days=start_time_delta_dict["days"], hours=start_time_delta_dict["hours"], minutes=start_time_delta_dict["minutes"])
        until_time = datetime.datetime.now() - datetime.timedelta(days=end_time_delta_dict["days"], hours=end_time_delta_dict["hours"], minutes=end_time_delta_dict["minutes"])

        sensor_cord_x, sensor_cord_y = sensor_cords.split("_") # sensor_cords expected to be in format x_y

        query = f"SELECT x_cord, y_cord, AVG(moisture_value), timestamp FROM sensor_data" \
                f" WHERE x_cord = {sensor_cord_x}" \
                f" AND y_cord = {sensor_cord_y}" \
                f" AND username = '{username}'" \
                f" AND password = '{password}'" \
                f" AND timestamp BETWEEN '{from_time}' AND '{until_time}'"
        row = cursor.execute(query).fetchall()
        sensor_avg_moisture = round(row[0][2],2) if row[0][2] != None else (-1) # rounds average moisture of given sensor over specified time

        return sensor_avg_moisture

    def water_sectors(self, coord_list):
        pass
