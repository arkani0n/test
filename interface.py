import random
import tkinter
from tkinter import messagebox

import classes
import configuration


class MainWindow:
    def __init__(self, username, password, field, red_threshold, yellow_threshold, green_threshold):

        self.username = username
        self.password = password

        self.root = tkinter.Tk()
        self.root.title(username)
        self.field = field

        self.main_frame = tkinter.Frame(self.root)
        self.main_frame.grid(row=0, column=0)

        self.bottom_frame = tkinter.Frame(self.root)
        self.bottom_frame.grid(row=1, column=0, sticky="w")  # Always will be from left

        self.sensor_label_color_settings = {
            "green": green_threshold,
            "yellow": yellow_threshold,
            "red": red_threshold,
            "white": -1,  # sector will be white if no value was found
        }
        self.sensor_water_list = []

        start_days_entry = tkinter.Entry(self.bottom_frame, width=4)
        start_days_label = tkinter.Label(self.bottom_frame, text="From days:")
        start_hours_entry = tkinter.Entry(self.bottom_frame, width=4)
        start_hours_label = tkinter.Label(self.bottom_frame, text="hours:")
        start_minutes_entry = tkinter.Entry(self.bottom_frame, width=4)
        start_minutes_label = tkinter.Label(self.bottom_frame, text="minutes:")

        end_days_entry = tkinter.Entry(self.bottom_frame, width=4)
        end_days_label = tkinter.Label(self.bottom_frame, text="Until days:")
        end_hours_entry = tkinter.Entry(self.bottom_frame, width=4)
        end_hours_label = tkinter.Label(self.bottom_frame, text="hours:")
        end_minutes_entry = tkinter.Entry(self.bottom_frame, width=4)
        end_minutes_label = tkinter.Label(self.bottom_frame, text="minutes:")

        self.time_entries = {
            "end_days": end_days_entry,
            "end_hours": end_hours_entry,
            "end_minutes": end_minutes_entry,
            "start_days": start_days_entry,
            "start_hours": start_hours_entry,
            "start_minutes": start_minutes_entry,
        }

        self.sensor_labels = self.set_sensor_labels()
        self.get_moisture_map()
        self.set_sensor_labels_binds(self.sensor_labels)
        for sensor_name in self.sensor_labels:
            self.set_sensor_color(sensor_name)

        place_holder = tkinter.Label(self.bottom_frame)
        place_holder.grid(row=0)
        # START DATE GRID
        start_days_label.grid(row=1, column=0)
        start_days_entry.grid(row=1, column=1)

        start_hours_label.grid(row=1, column=2)
        start_hours_entry.grid(row=1, column=3)

        start_minutes_label.grid(row=1, column=4)
        start_minutes_entry.grid(row=1, column=5)

        # UNTIL DATE GRID
        end_days_label.grid(row=2, column=0)
        end_days_entry.grid(row=2, column=1)

        end_hours_label.grid(row=2, column=2)
        end_hours_entry.grid(row=2, column=3)

        end_minutes_label.grid(row=2, column=4)
        end_minutes_entry.grid(row=2, column=5)

        self.refresh_button = tkinter.Button(self.bottom_frame, text="refresh", command=self.get_moisture_map)
        self.refresh_button.grid(row=2, column=6)

        self.trigger_watering_button = tkinter.Button(self.bottom_frame, text="Water selected sectors",
                                                      command=self.trigger_watering)
        self.reset_watering_button = tkinter.Button(self.bottom_frame, text="Reset selected sectors",
                                                    command=self.reset_water_list)

        self.trigger_watering_button.grid(row=1, column=7, padx=4)
        self.reset_watering_button.grid(row=2, column=7, padx=4)

    def add_remove_sensor_in_water_list(self, sensor_label):
        if sensor_label in self.sensor_water_list:
            self.sensor_water_list.remove(sensor_label)
            self.set_sensor_color(sensor_label)
        else:
            self.sensor_water_list.append(sensor_label)
            self.sensor_labels[sensor_label].config(bg="blue")

    def reset_water_list(self):
        for sensor_name in self.sensor_water_list.copy():
            self.add_remove_sensor_in_water_list(sensor_name)
        self.sensor_water_list = []

    def trigger_watering(self):
        print(f"Triggering watering for sectors: {self.sensor_water_list}")
        self.field.water_sectors(self.sensor_water_list)
        self.reset_water_list()  # Reset water list after the watering

    def set_sensor_color(self, sensor_name):
        sensor_moisture_value = float(self.sensor_labels[sensor_name].cget("text").split()[-1])  # moisture value will be in the last index
        if sensor_moisture_value >= self.sensor_label_color_settings["green"]:
            color = "green"
        elif sensor_moisture_value >= self.sensor_label_color_settings["yellow"]:
            color = "yellow"
        elif sensor_moisture_value >= self.sensor_label_color_settings["red"]:
            color = "red"
        elif sensor_moisture_value >= self.sensor_label_color_settings["white"]:
            color = "white"
        self.sensor_labels[sensor_name].config(bg=color)

    def set_sensor_labels(self):
        rows = self.field.number_of_rows
        columns = self.field.number_of_column
        sensor_labels = {}
        for row in range(rows):
            for column in range(columns):
                number = random.randint(1, 10)
                sensor_name = f"{row + 1}_{column + 1}"
                sensor_labels[sensor_name] = tkinter.Label(self.main_frame)
                sensor_labels[sensor_name].grid(row=row, column=column, padx=3, pady=3)

        return sensor_labels

    def set_sensor_labels_binds(self, sensor_labels):
        for sensor_name in sensor_labels:
            sensor_labels[sensor_name].bind("<Button-1>",
                                            lambda event, sensor_label=sensor_name: self.add_remove_sensor_in_water_list(
                                                sensor_label))

    def get_moisture_map(self):
        time_entries_values = {}
        # Getting time entries values
        for key in self.time_entries.keys():
            try:
                time_entries_values[key] = int(self.time_entries[key].get())
            except ValueError:
                time_entries_values[key] = 0

        for row_of_sensor_list in self.field.sensor_list:
            for sensor in row_of_sensor_list:
                moisture = self.field.get_moisture_map(sensor_cords=sensor,
                                                       start_time_delta_dict={
                                                           "days": time_entries_values["start_days"],
                                                           "hours": time_entries_values["start_hours"],
                                                           "minutes": time_entries_values["start_minutes"],
                                                       },
                                                       end_time_delta_dict={
                                                           "days": time_entries_values["end_days"],
                                                           "hours": time_entries_values["end_hours"],
                                                           "minutes": time_entries_values["end_minutes"],
                                                       },
                                                       username=self.username,
                                                       password=self.password
                                                       )
                self.sensor_labels[sensor].config(text=f"sensor coords: {sensor} \nmoisture: {moisture}")
                self.set_sensor_color(sensor_name=sensor)


def login_window(users):
    def login():
        username = username_entry.get()
        password = password_entry.get()

        if username in users and users[username] == password:
            messagebox.showinfo("Login", "Successful login!")
            save_credentials(username, password)  # Зберегти дані в файл
            open_main_window(username, password)
        else:
            messagebox.showerror("Login", "Invalid username or password.")

    def save_credentials(username, password):
        with open('my_credentials.py', 'w') as file:
            file.write(f'username= "{username}"\n')
            file.write(f'password= "{password}"\n')

    root = tkinter.Tk()
    root.title("Login")
    root.geometry("300x150")

    username_label = tkinter.Label(root, text="Username:")
    username_label.pack()
    username_entry = tkinter.Entry(root)
    username_entry.pack()

    password_label = tkinter.Label(root, text="Password:")
    password_label.pack()
    password_entry = tkinter.Entry(root, show="*")
    password_entry.pack()

    login_button = tkinter.Button(root, text="Login", command=login)
    login_button.pack()

    root.mainloop()


def open_main_window(username, password):
    Field = classes.Field(configuration.FIELD_LENGTH, configuration.FIELD_WIDTH, configuration.FIELD_SENSOR_RADIUS)
    interface = MainWindow(field=Field, red_threshold=configuration.INTERFACE_SECTOR_COLOR_RED, yellow_threshold=configuration.INTERFACE_SECTOR_COLOR_YELLOW,
                           green_threshold=configuration.INTERFACE_SECTOR_COLOR_GREEN, username=username, password=password)
    interface.root.mainloop()


users = {
    "potato": "potato1",
    "grain": "grain1",
    # Add other users as needed
}

login_window(users)
