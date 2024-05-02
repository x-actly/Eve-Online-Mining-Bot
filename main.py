import tkinter as tk
import tkinter.font as tkFont
import threading
import time
import ctypes
import random
from ctypes import windll
import functions as fe
import os
import configparser

# Check if the file exists
if not os.path.isfile('config.properties'):
    raise FileNotFoundError("Config file 'config.properties' not found.")

# Load configurations from the property file
config = configparser.ConfigParser()
config.read('config.properties')

# hard coded values
mining_target_reset = [(250, 260)]

# Mining functions
#########################################################

def start_function():
    global stop_flag
    stop_flag = False
    minutes = int(entry.get())
    undock_coo_value = [int(x.strip()) for x in config['POSITIONS']['undock_coo'].split(",")]
    mining_coo_values = [(int(x.strip()), int(y.strip())) for x, y in (value.split(",") for value in config['POSITIONS']['mining_coo'].split("\n"))]
    warp_to_coo_values = [int(x.strip()) for x in config['POSITIONS']['warp_to_coo'].split(",")]
    docking_coo_values = [int(x.strip()) for x in config['POSITIONS']['docking_coo'].split(",")]
    clear_cargo_coo_values = [int(x.strip()) for x in config['POSITIONS']['clear_cargo_coo'].split(",")]
    target_one_coo_values = [int(x.strip()) for x in config['POSITIONS']['target_one_coo'].split(",")]
    target_two_coo_values = [int(x.strip()) for x in config['POSITIONS']['target_two_coo'].split(",")]
    mouse_reset_coo_value = [int(x.strip()) for x in config['POSITIONS']['mouse_reset_coo'].split(",")]
    mining_hold_value = int(config['SETTINGS']['mining_hold'])
    mining_yield_value = int(config['SETTINGS']['mining_yield'])
    thread = threading.Thread(target=repeat_function, args=(minutes, undock_coo_value, mining_coo_values, warp_to_coo_values, docking_coo_values, clear_cargo_coo_values, target_one_coo_values, target_two_coo_values, mouse_reset_coo_value, mining_hold_value, mining_yield_value))
    thread.start()

def repeat_function(minutes, undock_coo_value, mining_coo_values, warp_to_coo_values, docking_coo_values, clear_cargo_coo_values, target_one_coo_values, target_two_coo_values, mouse_reset_coo_value, mining_hold_value, mining_yield_value):
    fe.log(f"The mining script will run {minutes} minutes!")
    end_time = time.time() + (minutes * 60)

    # cargo loading phrase

    cargo_loading_time = (mining_hold_value * 0.9) / mining_yield_value
    cargo_loading_time_print = cargo_loading_time / 60

    while not stop_flag and time.time() < end_time:

        fe.log(f"The mining cargo is filled in about {cargo_loading_time_print} minutes!")

        time.sleep(5)

        fe.undock(undock_coo_value[0], undock_coo_value[1])
        fe.set_hardener_online()

        item = random.choice(mining_coo_values)
        fe.warp_to_pos_circle_menu(item[0], item[1])
    
        fe.drone_out(mouse_reset_coo_value[0], mouse_reset_coo_value[1])
        fe.mining_behaviour(target_one_coo_values[0], target_one_coo_values[1], target_two_coo_values[0], target_two_coo_values[1], mining_target_reset[0][0], mining_target_reset[0][1], cargo_loading_time, cargo_loading_time, mouse_reset_coo_value[0], mouse_reset_coo_value[1])
        fe.drone_in()
        fe.warp_to_pos_circle_menu(warp_to_coo_values[0], warp_to_coo_values[1])
        fe.docking_circle_menu(docking_coo_values[0], docking_coo_values[1])
        fe.clear_cargo(clear_cargo_coo_values[0], clear_cargo_coo_values[1])

def stop_function():
    global stop_flag
    print("The mining script ends with this run!")
    stop_flag = True
#########################################################

stop_flag = False


# GUI settings
#########################################################

# Create Tkinter window
root = tk.Tk()
root.title("Mining Bot Owl-Edition")
root.geometry("480x600")  # Set windows size

# Make window not resizable
root.resizable(False, True)

# Create frame for input and buttons
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# Create frame for start- and stop buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Mining time
#########################################################

# Create input field for bot duration in minutes
entry_label = tk.Label(input_frame, text="Set mining duration in minutes:")
entry_label.grid(row=0, column=0, sticky="w")
entry = tk.Entry(input_frame)
entry.grid(row=0, column=1, padx=5, pady=4, sticky="w")
entry.insert(tk.END, config['SETTINGS']['mining_duration'])

# Undock
#########################################################

# create input field for undock coordinates
undock_coo_label = tk.Label(input_frame, text="Undock-Button Position:")
undock_coo_label.grid(row=1, column=0, sticky="w")
undock_coo_entry = tk.Entry(input_frame)
undock_coo_entry.grid(row=1, column=1, padx=5, pady=4, sticky="w")
undock_coo_entry.insert(tk.END, config['POSITIONS']['undock_coo'])

# Clear Cargo Position
#########################################################

# Create input field for clear-cargo position
clear_cargo_coo_label = tk.Label(input_frame, text="Clear-Cargo Position:")
clear_cargo_coo_label.grid(row=2, column=0, sticky="w")
clear_cargo_coo_entry = tk.Entry(input_frame)
clear_cargo_coo_entry.grid(row=2, column=1, padx=5, pady=4, sticky="w")
clear_cargo_coo_entry.insert(tk.END, config['POSITIONS']['clear_cargo_coo'])

# check if the coordinate is set correctly

def check_function():
    # Disable the button to prevent further clicks.
    check_button.config(state=tk.DISABLED)

    def execute_function():
        clear_cargo_coo_values = [int(x.strip()) for x in clear_cargo_coo_entry.get().split(",")]
        fe.clear_cargo(clear_cargo_coo_values[0], clear_cargo_coo_values[1])

        # Enable the button after the function completes.
        root.after(1, lambda: check_button.config(state=tk.NORMAL))

    # run function in a separate thread
    thread = threading.Thread(target=execute_function)
    thread.start()

check_button = tk.Button(input_frame, text="Test", compound="left", command=check_function)
check_button.grid(row=2, column=2, padx=5, pady=4, sticky="w")

# Mining Hold
#########################################################

# Create input field for mining hold in m3
mining_hold_label = tk.Label(input_frame, text="Mining Hold:")
mining_hold_label.grid(row=3, column=0, sticky="w")
mining_hold_entry = tk.Entry(input_frame)
mining_hold_entry.grid(row=3, column=1, padx=5, pady=4, sticky="w")
mining_hold_entry.insert(tk.END, config['SETTINGS']['mining_hold'])

# Mining Yield
#########################################################

# Create input field for mining yield in m3/s
mining_yield_label = tk.Label(input_frame, text="Mining Yield:")
mining_yield_label.grid(row=4, column=0, sticky="w")
mining_yield_entry = tk.Entry(input_frame)
mining_yield_entry.grid(row=4, column=1, padx=5, pady=4, sticky="w")
mining_yield_entry.insert(tk.END, config['SETTINGS']['mining_yield'])

# Docking Position
##########################################################

# Create input field for docking position
docking_coo_label = tk.Label(input_frame, text="Station-Overview Position:")
docking_coo_label.grid(row=5, column=0, sticky="w")
docking_coo_entry = tk.Entry(input_frame)
docking_coo_entry.grid(row=5, column=1, padx=5, pady=4, sticky="w")
docking_coo_entry.insert(tk.END, config['POSITIONS']['docking_coo'])

# Target-One-Position
########################################################

# Create input field for target-one position
target_one_coo_label = tk.Label(input_frame, text="Target-One Overview Position:")
target_one_coo_label.grid(row=6, column=0, sticky="w")
target_one_coo_entry = tk.Entry(input_frame)
target_one_coo_entry.grid(row=6, column=1, padx=5, pady=4, sticky="w")
target_one_coo_entry.insert(tk.END, config['POSITIONS']['target_one_coo'])

# Target-Two-Position
#######################################################

# Create input field for target-two position
target_two_coo_label = tk.Label(input_frame, text="Target-Two Overview Position:")
target_two_coo_label.grid(row=7, column=0, sticky="w")
target_two_coo_entry = tk.Entry(input_frame)
target_two_coo_entry.grid(row=7, column=1, padx=5, pady=4, sticky="w")
target_two_coo_entry.insert(tk.END, config['POSITIONS']['target_two_coo'])

# Target-Reset-Position
#######################################################

# Create input field for mouse reset
mouse_reset_coo_label = tk.Label(input_frame, text="Mouse Reset Position:")
mouse_reset_coo_label.grid(row=8, column=0, sticky="w")
mouse_reset_coo_entry = tk.Entry(input_frame)
mouse_reset_coo_entry.grid(row=8, column=1, padx=5, pady=4, sticky="w")
mouse_reset_coo_entry.insert(tk.END, config['POSITIONS']['mouse_reset_coo'])

# Home Position
##########################################################

# Create input field for warp-to position
warp_to_coo_label = tk.Label(input_frame, text="Home Bookmark:")
warp_to_coo_label.grid(row=9, column=0, sticky="w")
warp_to_coo_entry = tk.Entry(input_frame)
warp_to_coo_entry.grid(row=9, column=1, padx=5, pady=4, sticky="w")
warp_to_coo_entry.insert(tk.END, config['POSITIONS']['warp_to_coo'])

# Belt Bookmarks
#########################################################

# Create input field for mining position
mining_coo_label = tk.Label(input_frame, text="Belt Bookmarks:")
mining_coo_label.grid(row=10, column=0, sticky="w")
mining_coo_entry = tk.Text(input_frame, width=15, height=5)
mining_coo_entry.grid(row=10, column=1, padx=5, pady=4, sticky="w")
mining_coo_entry.insert(tk.END, config['POSITIONS']['mining_coo'].lstrip('\n'))

#########################################################

# Create start button
start_button = tk.Button(button_frame, text="Start", command=start_function)
start_button.grid(row=0, column=0, padx=(0, 10), pady=10, ipadx=5)

# Create stop button
stop_button = tk.Button(button_frame, text="Stop", command=stop_function)
stop_button.grid(row=0, column=1, padx=(10, 0), pady=10, ipadx=5)

# Create global save button

def global_save_button():
    config['SETTINGS']['mining_duration'] = entry.get()
    config['POSITIONS']['undock_coo'] = undock_coo_entry.get()
    config['POSITIONS']['clear_cargo_coo'] = clear_cargo_coo_entry.get()
    config['SETTINGS']['mining_hold'] = mining_hold_entry.get()
    config['SETTINGS']['mining_yield'] = mining_yield_entry.get()
    config['POSITIONS']['docking_coo'] = docking_coo_entry.get()
    config['POSITIONS']['target_one_coo'] = target_one_coo_entry.get()
    config['POSITIONS']['target_two_coo'] = target_two_coo_entry.get()
    config['POSITIONS']['mouse_reset_coo'] = mouse_reset_coo_entry.get()
    config['POSITIONS']['warp_to_coo'] = warp_to_coo_entry.get()
    config['POSITIONS']['mining_coo'] = mining_coo_entry.get(1.0, tk.END)
    with open('config.properties', 'w') as configfile:
        config.write(configfile)
    print("values saved!")

global_save_button = tk.Button(button_frame, text="Save", command=global_save_button)
global_save_button.grid(row=0, column=2, padx=(20, 0), pady=10, ipadx=5)

########################################################

# Function to get mouse position

def get_mouse_position():
    # Mausposition mit Hilfe der Windows-API abrufen
    user32 = windll.user32
    point = POINT()
    user32.GetCursorPos(ctypes.byref(point))
    return point.x, point.y


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long),
                ("y", ctypes.c_long)]

# Create a label to display the mouse position
mouse_position_label = tk.Label(root, text="")
mouse_position_label.pack(pady=20)

bold_font = tkFont.Font(weight="bold")

# Function to update the mouse position
def update_mouse_position():
    x, y = get_mouse_position()
    mouse_position_label.config(text=f"Mouse-Position: {x}, {y}", fg="red", font=bold_font)
    mouse_position_label.after(100, update_mouse_position)

# Start update mouse position
update_mouse_position()

# icon_bitmap
root.iconbitmap('')

# Start Tkinter Window
root.mainloop()
