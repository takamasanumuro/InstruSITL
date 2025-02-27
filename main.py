import tkinter as tk # Used for GUI
from tkinter import ttk # ttk is a module that contains themed widgets
import threading
from pymavlink import mavutil
from pymavlink.dialects.v20 import ardupilotmega


root = tk.Tk()
root.title("Mavlink voltage monitor")

voltage = 10.0

def update_voltage(value):
    voltage_label.config(text = f"Voltage: {float(value):.2f}V")
    global voltage
    voltage = float(value)

voltage_slider = ttk.Scale(root, from_ = 10, to = 14.4, orient = "horizontal", length = 300, command=update_voltage)
voltage_slider.pack(pady = 20)

voltage_label = tk.Label(root, text = "Voltage: 10.00V")
voltage_label.pack(pady=10)

location_label = tk.Label(root, text = "Location: ")
location_label.pack(pady=10)


def mavlink_thread():
    connection: mavutil.mavfile = mavutil.mavlink_connection(device = 'tcp:localhost:5762', source_system= 1, source_component= ardupilotmega.MAV_COMP_ID_BATTERY)
    connection.wait_heartbeat()
    print(f"Heartbeat from system {connection.target_system}")
    while True:
        mav: ardupilotmega.MAVLink = connection.mav

        #send battery status
        mav.battery_status_send(
            id = 0,
            battery_function = ardupilotmega.MAV_BATTERY_FUNCTION_ALL,
            type = ardupilotmega.MAV_BATTERY_TYPE_LIPO,
            temperature = -1,
            voltages = [int(voltage * 1000), 0, 0, 0, 0, 0, 0, 0, 0, 0],
            current_battery = -1,
            current_consumed = -1,
            energy_consumed = -1,
            battery_remaining = -1
        )

        location : mavutil.location = connection.location()
        location_label.config(text = f"Location: {location.lat}, {location.lng}")

        import time
        time.sleep(0.1)







threading.Thread(target=mavlink_thread, daemon=True).start()
root.mainloop()