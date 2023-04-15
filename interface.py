import random
import tkinter
import classes

#TODO add stat time, end time delta support,
# connect refresh button to get_moisture with setted time
class MainWindow:

    def __init__(self):

        self.root=tkinter.Tk()
        self.main_frame=tkinter.Frame(self.root)
        self.main_frame.grid(row=0,column=0)
        self.bottom_frame = tkinter.Frame(self.root)
        self.bottom_frame.grid(row=0,column=1)


        self.sensor_labels = self.set_sensor_labels()

        # self.get_moisture_map()

        start_days_entry = tkinter.Entry(self.main_frame, width=4)
        start_days_label = tkinter.Label(self.main_frame, text="From days:")
        start_hours_entry = tkinter.Entry(self.main_frame, width=4)
        start_hours_label = tkinter.Label(self.main_frame, text="hours:")
        start_minutes_entry = tkinter.Entry(self.main_frame, width=4)
        start_minutes_label = tkinter.Label(self.main_frame, text="minutes:")

        end_days_entry = tkinter.Entry(self.main_frame, width=4)
        end_days_label = tkinter.Label(self.main_frame, text="Until days:")
        end_hours_entry = tkinter.Entry(self.main_frame, width=4)
        end_hours_label = tkinter.Label(self.main_frame, text="hours:")
        end_minutes_entry = tkinter.Entry(self.main_frame, width=4)
        end_minutes_label = tkinter.Label(self.main_frame, text="minutes:")


        self.refresh_button = tkinter.Button(self.main_frame, text="refrsh", command=self.get_moisture_map)

        self.time_entries = {
            "end_days": end_days_entry,
            "end_hours" : end_hours_entry,
            "end_minutes" : end_minutes_entry,

            "start_days": start_days_entry,
            "start_hours" : start_hours_entry,
            "start_minutes" : start_minutes_entry
        }
        rows = classes.test.number_of_rows + 1
        place_holder = tkinter.Label(self.main_frame)
        place_holder.grid(row=rows)
        # START DATE GRID
        start_days_label.grid(row=rows+1, column=0)
        start_days_entry.grid(row=rows+1, column=1)

        start_hours_label.grid(row=rows+1, column=2)
        start_hours_entry.grid(row=rows+1, column=3)

        start_minutes_label.grid(row=rows+1, column=4)
        start_minutes_entry.grid(row=rows+1, column=5)

        # UNTIL DATE GRID
        end_days_label.grid(row=rows+2, column=0)
        end_days_entry.grid(row=rows+2, column=1)

        end_hours_label.grid(row=rows+2, column=2)
        end_hours_entry.grid(row=rows+2, column=3)

        end_minutes_label.grid(row=rows + 2, column=4)
        end_minutes_entry.grid(row=rows+2, column=5)
        self.refresh_button.grid(row=rows+2, column=6)
    # def set_time_entries(self):



    def set_sensor_labels(self):
        rows= classes.test.number_of_rows
        columns= classes.test.number_of_column
        sensor_labels = {}
        for row in range(rows):
            for coulumn in range(columns):
                number = random.randint(1,10)
                sensor_name = f"{row+1}_{coulumn+1}"
                sensor_labels[sensor_name] = tkinter.Label(self.main_frame, text=f"{sensor_name}\n {number}", borderwidth=2, bg="green" if number >5 else "red")
                sensor_labels[sensor_name].grid(row=row, column=coulumn )

        return sensor_labels

    def get_moisture_map(self):
        for row_of_sensor_list in classes.test.sensor_list:
            for sensor in row_of_sensor_list:
                print(f"geting moisture for {sensor}")
                moisure = classes.test.get_moisture_map(sensor,{"days":10, "minutes": 0, "hours":0}, {"days":0, "minutes": 0, "hours":0})
                self.sensor_labels[sensor].config(text=moisure)


test=MainWindow()
test.root.mainloop()
