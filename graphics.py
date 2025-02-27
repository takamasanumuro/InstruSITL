import tkinter as tk
from tkinter import ttk

def on_voltage_change(value):
    """Callback function when slider value changes."""
    print(f"Voltage: {value} V")

# Create the main window
root = tk.Tk()
root.title("Voltage Slider")

# Create and configure the slider
slider = ttk.Scale(
    root, from_=0, to=24,  # Voltage range (0V - 24V)
    orient="horizontal",
    length=300,
    command=on_voltage_change  # Calls function on slider move
)
slider.pack(pady=20)

# Label to display the current voltage
label = tk.Label(root, text="Move the slider to set voltage")
label.pack()

# Run the Tkinter event loop
root.mainloop()
