import tkinter as tk
import threading
import time
import ctypes
import random
from ctypes import windll
import functions_evebot as fe
from PIL import ImageTk, Image



# hard coded values
mining_target_reset = [(250, 260)]


# Mining functions
#########################################################

def start_function():
    global stop_flag
    stop_flag = False
    minutes = int(entry.get())
    undock_coo_value = [int(x.strip()) for x in undock_coo_entry.get().split(",")]
    drone_mouse_reset_coo_value = [int(x.strip()) for x in drone_mouse_reset_coo_entry.get().split(",")]
    mining_coo_values = mining_coo_entry.get("1.0", tk.END).strip().split("\n")
    mining_coo_values = [(int(x.strip()), int(y.strip())) for x, y in (value.split(",") for value in mining_coo_values)]
    mining_loop_reset_value = int(mining_loop_reset_entry.get())
    warp_to_coo_values = [int(x.strip()) for x in warp_to_coo_entry.get().split(",")]
    docking_coo_values = [int(x.strip()) for x in docking_coo_entry.get().split(",")]
    clear_cargo_coo_values = [int(x.strip()) for x in clear_cargo_coo_entry.get().split(",")]
    target_one_coo_values = [int(x.strip()) for x in target_one_coo_entry.get().split(",")]
    target_two_coo_values = [int(x.strip()) for x in target_two_coo_entry.get().split(",")]
    mining_mouse_reset_coo_values = [int(x.strip()) for x in mining_mouse_reset_coo_entry.get().split(",")]
    thread = threading.Thread(target=repeat_function, args=(minutes, undock_coo_value, drone_mouse_reset_coo_value, mining_coo_values, mining_loop_reset_value, warp_to_coo_values, docking_coo_values, clear_cargo_coo_values, target_one_coo_values, target_two_coo_values, mining_mouse_reset_coo_values))
    thread.start()

def repeat_function(minutes, undock_coo_value, drone_mouse_reset_coo_value, mining_coo_values, mining_loop_reset_value, warp_to_coo_values, docking_coo_values, clear_cargo_coo_values, target_one_coo_values, target_two_coo_values, mining_mouse_reset_coo_values):
    print(f"The mining script will run {minutes} minutes!")
    end_time = time.time() + (minutes * 60)

    while not stop_flag and time.time() < end_time:
        time.sleep(5)

        fe.undock(undock_coo_value[0], undock_coo_value[1])
        fe.set_hardener_online()

        item = random.choice(mining_coo_values)
        fe.warp_to_pos_circle_menu(item[0], item[1])
    
        fe.drone_out(drone_mouse_reset_coo_value[0], drone_mouse_reset_coo_value[1])
        fe.mining_behaviour(target_one_coo_values[0], target_one_coo_values[1], target_two_coo_values[0], target_two_coo_values[1], mining_target_reset[0][0], mining_target_reset[0][1], mining_loop_reset_value, mining_loop_reset_value, mining_mouse_reset_coo_values[0], mining_mouse_reset_coo_values[1])
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
root.title("Mining Bot 0.1.2c Owl-Edition")
root.geometry("480x560")  # Set windows size

# Make window not resizable
root.resizable(False, False)

# Load save icon
save_icon = Image.open("config/icons/save_icon.png")  # Pfade und Dateinamen anpassen
save_icon = save_icon.resize((16, 16))  # Größe anpassen
save_icon = ImageTk.PhotoImage(save_icon)

# Create frame for input and buttons
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# Create frame for start- and stop buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Mining time
#########################################################

# Create input field for bot duration in minutes
entry_label = tk.Label(input_frame, text="Set mining time in minutes:")
entry_label.grid(row=0, column=0, sticky="w")
entry = tk.Entry(input_frame)
entry.grid(row=0, column=1, padx=5, pady=4, sticky="w")

# Belt time
##########################################################

# saving and return mining loop reset
MINING_LOOP_VALUE_FILE = "config/mining_loop_value.txt"

def load_mining_loop_value():
    try:
        with open(MINING_LOOP_VALUE_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

def save_mining_loop_value():
    with open(MINING_LOOP_VALUE_FILE, "w") as file:
        file.write(mining_loop_reset_entry.get())

# function to save coordinates
def save_button_clicked_mining_loop_reset():
    save_mining_loop_value()
    print("Value saved!")

# Create a text field for the mining loop reset values
mining_loop_reset_label = tk.Label(input_frame, text="Set belt time in seconds:")
mining_loop_reset_label.grid(row=1, column=0, sticky="w")
mining_loop_reset_entry = tk.Entry(input_frame)
mining_loop_reset_entry.grid(row=1, column=1, padx=5, pady=4, sticky="w")

# Loading the saved coordinates at program startup
mining_loop_reset_entry.insert(tk.END, load_mining_loop_value())

# Create save button
save_button = tk.Button(input_frame, image=save_icon, compound="left", command=save_button_clicked_mining_loop_reset)
save_button.grid(row=1, column=2, padx=5, pady=4, sticky="w")

# Undock
#########################################################

# saving and return undock coordinates
UNDOCK_COO_FILE = "config/undock_coo.txt"

def load_undock_coo():
    try:
        with open(UNDOCK_COO_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

def save_undock_coo():
    with open(UNDOCK_COO_FILE, "w") as file:
        file.write(undock_coo_entry.get())

# function to save coordinates
def save_button_clicked_undock():
    save_undock_coo()
    print("Value saved!")

# create input field for undock coordinates    
undock_coo_label = tk.Label(input_frame, text="Undock-Position:")
undock_coo_label.grid(row=2, column=0, sticky="w")
undock_coo_entry = tk.Entry(input_frame)
undock_coo_entry.grid(row=2, column=1, padx=5, pady=4, sticky="w")

# Loading the saved coordinates at startup
undock_coo_entry.insert(tk.END, load_undock_coo())

# Create save button
save_button = tk.Button(input_frame, image=save_icon, compound="left", command=save_button_clicked_undock)
save_button.grid(row=2, column=2, padx=5, pady=4, sticky="w")

# Docking Position
##########################################################

# saving and return docking coordinates
DOCKING_FILE = "config/docking_coo.txt"

def load_docking_coo():
    try:
        with open(DOCKING_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

def save_docking_coo():
    with open(DOCKING_FILE, "w") as file:
        file.write(docking_coo_entry.get())

# Function to save coordinates
def save_button_clicked_docking():
    save_docking_coo()
    print("Value saved!")

# Create input field for docking position
docking_coo_label = tk.Label(input_frame, text="Docking-Position:")
docking_coo_label.grid(row=3, column=0, sticky="w")
docking_coo_entry = tk.Entry(input_frame)
docking_coo_entry.grid(row=3, column=1, padx=5, pady=4, sticky="w")

# Loading the saved coordinates at program startup 
docking_coo_entry.insert(tk.END, load_docking_coo())

# Create save button
save_button = tk.Button(input_frame, image=save_icon, compound="left", command=save_button_clicked_docking)
save_button.grid(row=3, column=2, padx=5, pady=4, sticky="w")

# Clear Cargo Position
#########################################################

# saving and return clear cargo coordinates
CLEAR_CARGO_FILE = "config/clear_cargo_coo.txt"

def load_clear_cargo_coo():
    try:
        with open(CLEAR_CARGO_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

def save_clear_cargo_coo():
    with open(CLEAR_CARGO_FILE, "w") as file:
        file.write(clear_cargo_coo_entry.get())

# Function to save coordinates
def save_button_clicked_clear_cargo():
    save_clear_cargo_coo()
    print("Value saved!")

# Create input field for clear-cargo position
clear_cargo_coo_label = tk.Label(input_frame, text="Clear-Cargo-Position:")
clear_cargo_coo_label.grid(row=4, column=0, sticky="w")
clear_cargo_coo_entry = tk.Entry(input_frame)
clear_cargo_coo_entry.grid(row=4, column=1, padx=5, pady=4, sticky="w")

# Loading the saved coordinates at program startup
clear_cargo_coo_entry.insert(tk.END, load_clear_cargo_coo())

# Create save button
save_button = tk.Button(input_frame, image=save_icon, compound="left", command=save_button_clicked_clear_cargo)
save_button.grid(row=4, column=2, padx=5, pady=4, sticky="w")

# Target-One-Position
########################################################

# saving and return target-one-coordinates
TARGET_ONE_COO_FILE = "config/target_one_coo.txt"

def load_target_one_coo():
    try:
        with open(TARGET_ONE_COO_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

def save_target_one_coo():
    with open(TARGET_ONE_COO_FILE, "w") as file:
        file.write(target_one_coo_entry.get())

# Function to save coordinates
def save_button_clicked_target_one():
    save_target_one_coo()
    print("Value saved!")

# Create input field for target-one position
target_one_coo_label = tk.Label(input_frame, text="Target-One-Position:")
target_one_coo_label.grid(row=5, column=0, sticky="w")
target_one_coo_entry = tk.Entry(input_frame)
target_one_coo_entry.grid(row=5, column=1, padx=5, pady=4, sticky="w")

# Loading the saved coordinates at program startup
target_one_coo_entry.insert(tk.END, load_target_one_coo())

# Create a save button
save_button = tk.Button(input_frame, image=save_icon, compound="left", command=save_button_clicked_target_one)
save_button.grid(row=5, column=2, padx=5, pady=4, sticky="w")

# Target-Two-Position
#######################################################

# saving and return target-two coordinates
TARGET_TWO_COO_FILE = "config/target_two_coo.txt"

def load_target_two_coo():
    try:
        with open(TARGET_TWO_COO_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

def save_target_two_coo():
    with open(TARGET_TWO_COO_FILE, "w") as file:
        file.write(target_two_coo_entry.get())

# Function to save coordinates
def save_button_clicked_target_two():
    save_target_two_coo()
    print("Value saved!")

# Create input field for target-two position
target_two_coo_label = tk.Label(input_frame, text="Target-Two-Position:")
target_two_coo_label.grid(row=6, column=0, sticky="w")
target_two_coo_entry = tk.Entry(input_frame)
target_two_coo_entry.grid(row=6, column=1, padx=5, pady=4, sticky="w")

# Loading the saved coordinates at program startup
target_two_coo_entry.insert(tk.END, load_target_two_coo())

# Create save button
save_button = tk.Button(input_frame, image=save_icon, compound="left", command=save_button_clicked_target_two)
save_button.grid(row=6, column=2, padx=5, pady=4, sticky="w")

# Target-Reset-Position
#######################################################

# saving and return mining mouse reset
MINING_MOUSE_RESET_FILE = "config/mining_mouse_reset.txt"

def load_mining_mouse_reset_coo():
    try:
        with open(MINING_MOUSE_RESET_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

def save_mining_mouse_reset_coo():
    with open(MINING_MOUSE_RESET_FILE, "w") as file:
        file.write(mining_mouse_reset_coo_entry.get())

# Function to save coordinates
def save_button_clicked_mining_mouse_reset():
    save_mining_mouse_reset_coo()
    print("Value saved!")

# Create input field for mining mouse reset
mining_mouse_reset_coo_label = tk.Label(input_frame, text="Target Reset-Position:")
mining_mouse_reset_coo_label.grid(row=7, column=0, sticky="w")
mining_mouse_reset_coo_entry = tk.Entry(input_frame)
mining_mouse_reset_coo_entry.grid(row=7, column=1, padx=5, pady=4, sticky="w")

# Loading the saved coordinates at program startup
mining_mouse_reset_coo_entry.insert(tk.END, load_mining_mouse_reset_coo())

# Create save button
save_button = tk.Button(input_frame, image=save_icon, compound="left", command=save_button_clicked_mining_mouse_reset)
save_button.grid(row=7, column=2, padx=5, pady=4, sticky="w")

# Drone-Reset-Position
##########################################################

# saving and return drone mouse reset coordinates
DRONE_MOUSE_RESET_COO_FILE = "config/drone_mouse_reset_coo.txt"

def load_drone_mouse_reset_coo():
    try:
        with open(DRONE_MOUSE_RESET_COO_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

def save_drone_mouse_reset_coo():
    with open(DRONE_MOUSE_RESET_COO_FILE, "w") as file:
        file.write(drone_mouse_reset_coo_entry.get())

# Function to save coordinates
def save_button_clicked_drone_reset():
    save_drone_mouse_reset_coo()
    print("Value saved!")

# Create input field for drone mouse reset position
drone_mouse_reset_coo_label = tk.Label(input_frame, text="Drone Reset-Position:")
drone_mouse_reset_coo_label.grid(row=8, column=0, sticky="w")
drone_mouse_reset_coo_entry = tk.Entry(input_frame)
drone_mouse_reset_coo_entry.grid(row=8, column=1, padx=5, pady=4, sticky="w")

# Loading the saved coordinates at startup
drone_mouse_reset_coo_entry.insert(tk.END, load_drone_mouse_reset_coo())

# Create save button
save_button = tk.Button(input_frame, image=save_icon, compound="left", command=save_button_clicked_drone_reset)
save_button.grid(row=8, column=2, padx=5, pady=4, sticky="w")

# Home Position
##########################################################

# saving and return warp-to coordinates
WARP_TO_COO_FILE = "config/warp_too_coo.txt"

def load_warp_to_coo():
    try:
        with open(WARP_TO_COO_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

def save_warp_to_coo():
    with open(WARP_TO_COO_FILE, "w") as file:
        file.write(warp_to_coo_entry.get())

# Function to save coordinates
def save_button_clicked_warp_to_coo():
    save_warp_to_coo()
    print("Value saved!")

# Create input field for warp-to position
warp_to_coo_label = tk.Label(input_frame, text="Home Bookmark:")
warp_to_coo_label.grid(row=9, column=0, sticky="w")
warp_to_coo_entry = tk.Entry(input_frame)
warp_to_coo_entry.grid(row=9, column=1, padx=5, pady=4, sticky="w")

# Loading the saved coordinates at startup
warp_to_coo_entry.insert(tk.END, load_warp_to_coo())

# Create save button
save_button = tk.Button(input_frame, image=save_icon, compound="left", command=save_button_clicked_warp_to_coo)
save_button.grid(row=9, column=2, padx=5, pady=4, sticky="w")

# Belt Bookmarks
#########################################################

# saving and return mining coordinates
MINING_COO_FILE = "config/mining_coo.txt"

def load_mining_coo():
    try:
        with open(MINING_COO_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

def save_mining_coo():
    with open(MINING_COO_FILE, "w") as file:
        file.write(mining_coo_entry.get('1.0', 'end'))

# Function to save coordinates
def save_button_clicked_mining():
    save_mining_coo()
    print("Value saved!")

# Create input field for mining position
mining_coo_label = tk.Label(input_frame, text="Belt Bookmarks:")
mining_coo_label.grid(row=10, column=0, sticky="w")
mining_coo_entry = tk.Text(input_frame, width=15, height=5)
mining_coo_entry.grid(row=10, column=1, padx=5, pady=4, sticky="w")

# Loading the saved coordinates at program startup
mining_coo_entry.insert(tk.END, load_mining_coo())

# Create save button
save_button = tk.Button(input_frame, image=save_icon, compound="left", command=save_button_clicked_mining)
save_button.grid(row=10, column=2, padx=5, pady=4, sticky="w")

#########################################################

# Create start button
start_button = tk.Button(button_frame, text="Start", command=start_function)
start_button.grid(row=0, column=0, padx=(0, 10), ipadx=5)

# Create stop button
stop_button = tk.Button(button_frame, text="Stop", command=stop_function)
stop_button.grid(row=0, column=1, padx=(10, 0), ipadx=5)

########################################################

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
mouse_position_label.pack(pady=10)

# Function to update the mouse position
def update_mouse_position():
    x, y = get_mouse_position()
    mouse_position_label.config(text=f"Mouse-Position: {x}, {y}")
    mouse_position_label.after(100, update_mouse_position)

# Start update mouse position
update_mouse_position()

# Start Tkinter Window
root.mainloop()
