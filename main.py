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
import pygetwindow as gw
import re

# Check if the file exists
if not os.path.isfile("config.properties"):
    raise FileNotFoundError("Config file 'config.properties' not found.")

# Load configurations from the property file
config = configparser.ConfigParser()
config.read("config.properties")

# a developer hatch/hook for now, if set to False things will surely break.
disable_if_no_eve_windows = bool(
    config["SETTINGS"].get("disable_if_no_eve_windows", "True")
)

# When cargo hold is full, the ship will dock up and unload cargo, undock and warp to another belt
cargo_loading_time_adjustment = int(
    config["SETTINGS"].get("cargo_loading_time_adjustment", "180")
)

# Mining functions
#########################################################


def start_function():
    global stop_flag
    stop_flag = False
    # make sure we save and update config before we start
    save_properties()
    mining_runs = int(entry.get())
    undock_coo_value = [
        int(x.strip()) for x in config["POSITIONS"]["undock_coo"].split(",")
    ]
    mining_coo_values = [
        (int(x.strip()), int(y.strip()))
        for x, y in (
            value.split(",") for value in config["POSITIONS"]["mining_coo"].split("\n")
        )
    ]
    warp_to_coo_values = [
        int(x.strip()) for x in config["POSITIONS"]["warp_to_coo"].split(",")
    ]
    clear_cargo_coo_values = [
        int(x.strip()) for x in config["POSITIONS"]["clear_cargo_coo"].split(",")
    ]
    target_one_coo_values = [
        int(x.strip()) for x in config["POSITIONS"]["target_one_coo"].split(",")
    ]
    target_two_coo_values = [
        int(x.strip()) for x in config["POSITIONS"]["target_two_coo"].split(",")
    ]
    mouse_reset_coo_values = [
        int(x.strip()) for x in config["POSITIONS"]["mouse_reset_coo"].split(",")
    ]
    mining_hold_value = int(config["SETTINGS"]["mining_hold"])
    mining_yield_value = float(config["SETTINGS"]["mining_yield"].replace(",", "."))
    # add 2 seconds to mining_reset_timer to ensure sure we wait long enough for the lasers to complete its mining cycle
    mining_reset_timer = 2 + int(config["SETTINGS"].get("mining_reset_timer", "120"))
    fe.log(f"Using miner reset timer of {mining_reset_timer} seconds.")
    cargo_loading_time = mining_hold_value / mining_yield_value
    if cargo_loading_time < fe.long_sleep_base:
        fe.log(
            "MINING HOLD OR YIELD IS LIKELY MISCONFIGURED, BECAUSE THE TOTAL TIME TO COMPLETE CARGO LOADING IS LESS THAN THE TIME TO WARP OUT TO BELT."
        )
    hardener_key = config["SETTINGS"].get("hardener_key", "F3")
    unlock_all_targets_key = config["SETTINGS"].get("unlock_all_targets_key", "")
    fe.log(f"The mining script will run {mining_runs} mining runs!")
    thread = threading.Thread(
        target=lambda: repeat_function(
            mining_runs=mining_runs,
            undock_coo_value=undock_coo_value,
            mining_coo_values=mining_coo_values,
            warp_to_coo_values=warp_to_coo_values,
            clear_cargo_coo_values=clear_cargo_coo_values,
            target_one_coo_values=target_one_coo_values,
            target_two_coo_values=target_two_coo_values,
            mouse_reset_coo_values=mouse_reset_coo_values,
            mining_reset_timer=mining_reset_timer,
            cargo_loading_time=cargo_loading_time,
            hardener_key=hardener_key,
            unlock_all_targets_key=unlock_all_targets_key,
        )
    )
    thread.start()


def repeat_function(
    mining_runs: int,
    undock_coo_value: list[int],
    mining_coo_values: list[int],
    warp_to_coo_values: list[int],
    clear_cargo_coo_values: list[int],
    target_one_coo_values: list[int],
    target_two_coo_values: list[int],
    mouse_reset_coo_values: list[int],
    mining_reset_timer: int,
    cargo_loading_time: float,
    hardener_key: str,
    unlock_all_targets_key: str,
):
    disable_fields()
    actual_mining_runs = 0
    update_mining_runs(actual_mining_runs, mining_runs)
    estimated_run_time = mining_runs * (
        cargo_loading_time + (cargo_loading_time_adjustment if mining_runs > 1 else 0)
    )
    fe.set_next_reset(estimated_run_time, fe.TIME_LEFT)
    fe.log(f"Estimate for completion is {estimated_run_time / 60} minutes!")
    while not stop_flag and actual_mining_runs < mining_runs:
        selected_eve_window.activate()
        fe.set_next_reset(cargo_loading_time, fe.CARGO_LOAD_TIME)
        fe.log(
            f"The mining cargo is filled in about {cargo_loading_time / 60} minutes!"
        )
        time.sleep(1)
        fe.undock(undock_coo_value[0], undock_coo_value[1])
        selected_eve_window.activate()
        fe.set_hardener_online(hardener_key)
        item = random.choice(mining_coo_values)
        fe.click_warp_circle_menu(item[0], item[1])
        selected_eve_window.activate()
        fe.drone_out(mouse_reset_coo_values[0], mouse_reset_coo_values[1])
        fe.mining_behaviour(
            tx1=target_one_coo_values[0],
            ty1=target_one_coo_values[1],
            tx2=target_two_coo_values[0],
            ty2=target_two_coo_values[1],
            mr_start=mining_reset_timer,
            mr_end=mining_reset_timer,
            ml_start=cargo_loading_time,
            ml_end=cargo_loading_time,
            rm_x=mouse_reset_coo_values[0],
            rm_y=mouse_reset_coo_values[1],
            unlock_all_targets_keys=unlock_all_targets_key,
            focus_eve_window=lambda: selected_eve_window.activate(),
        )
        selected_eve_window.activate()
        fe.drone_in()
        selected_eve_window.activate()
        fe.click_dock_circle_menu(warp_to_coo_values[0], warp_to_coo_values[1])
        selected_eve_window.activate()
        fe.clear_cargo(clear_cargo_coo_values[0], clear_cargo_coo_values[1])
        actual_mining_runs += 1
        update_mining_runs(actual_mining_runs, mining_runs)
    fe.set_next_reset(0, fe.TIME_LEFT)
    fe.log(f"Completed {actual_mining_runs}/{mining_runs} mining sessions")
    enable_fields()


def stop_function():
    global stop_flag
    fe.set_next_reset(0, fe.TIME_LEFT)
    fe.log("The mining script ends with this run!")
    stop_flag = True


#########################################################


def disable_fields():
    # Disable input fields
    entry.config(state=tk.DISABLED)
    undock_coo_entry.config(state=tk.DISABLED)
    clear_cargo_coo_entry.config(state=tk.DISABLED)
    mining_hold_entry.config(state=tk.DISABLED)
    mining_yield_entry.config(state=tk.DISABLED)
    target_one_coo_entry.config(state=tk.DISABLED)
    target_two_coo_entry.config(state=tk.DISABLED)
    mouse_reset_coo_entry.config(state=tk.DISABLED)
    warp_to_coo_entry.config(state=tk.DISABLED)
    mining_coo_entry.config(state=tk.NORMAL)
    mining_coo_entry.tag_configure("disabled", foreground="gray")
    mining_coo_entry.config(state=tk.DISABLED)
    mining_coo_entry.insert(tk.END, config["POSITIONS"]["mining_coo"].lstrip("\n"))
    mining_coo_entry.tag_add("disabled", "1.0", "end")

    # Disable buttons
    start_button.config(state=tk.DISABLED)
    save_button.config(state=tk.DISABLED)
    check_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)


def enable_fields():
    # Enable input fields
    entry.config(state=tk.NORMAL)
    undock_coo_entry.config(state=tk.NORMAL)
    clear_cargo_coo_entry.config(state=tk.NORMAL)
    mining_hold_entry.config(state=tk.NORMAL)
    mining_yield_entry.config(state=tk.NORMAL)
    target_one_coo_entry.config(state=tk.NORMAL)
    target_two_coo_entry.config(state=tk.NORMAL)
    mouse_reset_coo_entry.config(state=tk.NORMAL)
    warp_to_coo_entry.config(state=tk.NORMAL)
    mining_coo_entry.config(state=tk.NORMAL)
    mining_coo_entry.tag_remove("disabled", "1.0", "end")

    # Enable buttons
    start_button.config(state=tk.NORMAL)
    save_button.config(state=tk.NORMAL)
    check_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)


stop_flag = False


# GUI settings
#########################################################

# Create Tkinter window
root = tk.Tk()
root.wm_attributes("-topmost", 1)
root.title("Mining Bot Owl-Edition")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 480
window_height = 680
x_pos = screen_width - window_width
y_pos = 0
root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

# Make window not resizable
root.resizable(False, True)

# Create frame for input and buttons
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# Create frame for start- and stop buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# EVE window selection
#########################################################


def on_window_select(selection):
    global selected_eve_window
    windows = gw.getWindowsWithTitle(selection)
    if windows:
        selected_eve_window = windows[0]


# Label for the EVE window selector
window_label = tk.Label(input_frame, text="Select EVE window:")
window_label.grid(row=0, column=0, sticky="w")

# Get list of EVE windows
eve_windows = gw.getWindowsWithTitle("EVE -")
if eve_windows:
    window_titles = [window.title for window in eve_windows]
else:
    window_titles = ["No EVE windows"]

# Dropdown menu
# Default selection
eve_window = tk.StringVar()
if window_titles:
    eve_window.set(window_titles[0])
    if eve_windows:
        selected_eve_window = eve_windows[0]
        fe.log(f"Selected the first EVE window")
else:
    eve_window.set("No EVE windows")


# Function to update the OptionMenu text
def update_option_menu(selection):
    if selection:
        eve_window.set(re.sub(r"EVE - .*", "EVE - REDACTED", selection))
    else:
        eve_window.set("No EVE windows")


window_select = tk.OptionMenu(
    input_frame, eve_window, *window_titles, command=on_window_select
)
update_option_menu(eve_window.get())  # Update initial text
eve_window.trace_add(
    "write", lambda *args: update_option_menu(eve_window.get())
)  # Update text on selection change
window_select.grid(row=0, column=1, padx=5, pady=4, sticky="w")

# Mining time
#########################################################

# Label for the number of mining runs
entry_label = tk.Label(input_frame, text="Set number of mining runs:")
entry_label.grid(row=1, column=0, sticky="w")

# Entry field for the number of mining runs
entry = tk.Entry(input_frame)
entry.grid(row=1, column=1, padx=5, pady=4, sticky="w")
entry.insert(tk.END, config["SETTINGS"]["mining_runs"])

# Undock
#########################################################

# create input field for undock coordinates
undock_coo_label = tk.Label(input_frame, text="Undock-Button Position:")
undock_coo_label.grid(row=2, column=0, sticky="w")
undock_coo_entry = tk.Entry(input_frame)
undock_coo_entry.grid(row=2, column=1, padx=5, pady=4, sticky="w")
undock_coo_entry.insert(tk.END, config["POSITIONS"]["undock_coo"])

# Clear Cargo Position
#########################################################

# Create input field for clear-cargo position
clear_cargo_coo_label = tk.Label(input_frame, text="Clear-Cargo Position:")
clear_cargo_coo_label.grid(row=3, column=0, sticky="w")
clear_cargo_coo_entry = tk.Entry(input_frame)
clear_cargo_coo_entry.grid(row=3, column=1, padx=5, pady=4, sticky="w")
clear_cargo_coo_entry.insert(tk.END, config["POSITIONS"]["clear_cargo_coo"])

# check if the coordinate is set correctly


def check_function():
    # Disable the button to prevent further clicks.
    check_button.config(state=tk.DISABLED)

    def execute_function():
        clear_cargo_coo_values = [
            int(x.strip()) for x in clear_cargo_coo_entry.get().split(",")
        ]
        fe.clear_cargo(clear_cargo_coo_values[0], clear_cargo_coo_values[1])

        # Enable the button after the function completes.
        root.after(1, lambda: check_button.config(state=tk.NORMAL))

    # run function in a separate thread
    thread = threading.Thread(target=execute_function)
    thread.start()


check_button = tk.Button(
    input_frame, text="Test", compound="left", command=check_function
)
check_button.grid(row=3, column=2, padx=5, pady=4, sticky="w")

# Mining Hold
#########################################################

# Create input field for mining hold in m3
mining_hold_label = tk.Label(input_frame, text="Mining Hold (m3):")
mining_hold_label.grid(row=4, column=0, sticky="w")
mining_hold_entry = tk.Entry(input_frame)
mining_hold_entry.grid(row=4, column=1, padx=5, pady=4, sticky="w")
mining_hold_entry.insert(tk.END, config["SETTINGS"]["mining_hold"])

# Mining Yield
#########################################################

# Create input field for mining yield in m3/s
mining_yield_label = tk.Label(input_frame, text="Mining Yield (m3/s):")
mining_yield_label.grid(row=5, column=0, sticky="w")
mining_yield_entry = tk.Entry(input_frame)
mining_yield_entry.grid(row=5, column=1, padx=5, pady=4, sticky="w")
mining_yield_entry.insert(tk.END, config["SETTINGS"]["mining_yield"])

# Target-One-Position
########################################################

# Create input field for target-one position
target_one_coo_label = tk.Label(input_frame, text="Target-One Overview Position:")
target_one_coo_label.grid(row=6, column=0, sticky="w")
target_one_coo_entry = tk.Entry(input_frame)
target_one_coo_entry.grid(row=6, column=1, padx=5, pady=4, sticky="w")
target_one_coo_entry.insert(tk.END, config["POSITIONS"]["target_one_coo"])

# Target-Two-Position
#######################################################

# Create input field for target-two position
target_two_coo_label = tk.Label(input_frame, text="Target-Two Overview Position:")
target_two_coo_label.grid(row=7, column=0, sticky="w")
target_two_coo_entry = tk.Entry(input_frame)
target_two_coo_entry.grid(row=7, column=1, padx=5, pady=4, sticky="w")
target_two_coo_entry.insert(tk.END, config["POSITIONS"]["target_two_coo"])

# Target-Reset-Position
#######################################################

# Create input field for mouse reset
mouse_reset_coo_label = tk.Label(input_frame, text="Mouse Reset Position:")
mouse_reset_coo_label.grid(row=8, column=0, sticky="w")
mouse_reset_coo_entry = tk.Entry(input_frame)
mouse_reset_coo_entry.grid(row=8, column=1, padx=5, pady=4, sticky="w")
mouse_reset_coo_entry.insert(tk.END, config["POSITIONS"]["mouse_reset_coo"])

# Home Position
##########################################################

# Create input field for warp-to position
warp_to_coo_label = tk.Label(input_frame, text="Home Bookmark:")
warp_to_coo_label.grid(row=9, column=0, sticky="w")
warp_to_coo_entry = tk.Entry(input_frame)
warp_to_coo_entry.grid(row=9, column=1, padx=5, pady=4, sticky="w")
warp_to_coo_entry.insert(tk.END, config["POSITIONS"]["warp_to_coo"])

# Belt Bookmarks
#########################################################

# Create input field for mining position
mining_coo_label = tk.Label(input_frame, text="Belt Bookmarks:")
mining_coo_label.grid(row=10, column=0, sticky="w")
mining_coo_entry = tk.Text(input_frame, width=15, height=5)
mining_coo_entry.grid(row=10, column=1, padx=5, pady=4, sticky="w")
mining_coo_entry.insert(tk.END, config["POSITIONS"]["mining_coo"].lstrip("\n"))

#########################################################

# Create start button
start_button = tk.Button(button_frame, text="Start", command=start_function)
start_button.grid(row=0, column=0, padx=(0, 10), pady=10, ipadx=5)
if disable_if_no_eve_windows and not eve_windows:
    start_button.config(state=tk.DISABLED)

# Create stop button
stop_button = tk.Button(button_frame, text="Stop", command=stop_function)
stop_button.grid(row=0, column=1, padx=(10, 0), pady=10, ipadx=5)
stop_button.config(state=tk.DISABLED)

# Create global save button


def save_properties():
    config["SETTINGS"]["mining_runs"] = entry.get()
    config["POSITIONS"]["undock_coo"] = undock_coo_entry.get()
    config["POSITIONS"]["clear_cargo_coo"] = clear_cargo_coo_entry.get()
    config["SETTINGS"]["mining_hold"] = mining_hold_entry.get()
    config["SETTINGS"]["mining_yield"] = mining_yield_entry.get()
    config["POSITIONS"]["target_one_coo"] = target_one_coo_entry.get()
    config["POSITIONS"]["target_two_coo"] = target_two_coo_entry.get()
    config["POSITIONS"]["mouse_reset_coo"] = mouse_reset_coo_entry.get()
    config["POSITIONS"]["warp_to_coo"] = warp_to_coo_entry.get()
    config["POSITIONS"]["mining_coo"] = mining_coo_entry.get(1.0, tk.END).strip()
    with open("config.properties", "w") as configfile:
        config.write(configfile)
    fe.log("values saved!")


save_button = tk.Button(button_frame, text="Save", command=save_properties)
save_button.grid(row=0, column=2, padx=(20, 0), pady=10, ipadx=5)

########################################################


def insert_mouse_position(event):
    x, y = get_mouse_position()
    if isinstance(event.widget, tk.Text):
        event.widget.insert(tk.END, f"\n{x}, {y}")
    elif isinstance(event.widget, tk.Entry):
        event.widget.delete(0, tk.END)
        event.widget.insert(tk.END, f"{x}, {y}")


# Function to get mouse position


def get_mouse_position():
    # Mausposition mit Hilfe der Windows-API abrufen
    user32 = windll.user32
    point = POINT()
    user32.GetCursorPos(ctypes.byref(point))
    return point.x, point.y


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


# Create a label to display the mouse position
mouse_position_label = tk.Label(root, text="")
mouse_position_label.pack(pady=10)

bold_font = tkFont.Font(weight="bold")


# Function to update the mouse position
def update_mouse_position():
    x, y = get_mouse_position()
    mouse_position_label.config(text=f"Mouse-Position: {x}, {y}", font=("Arial", 12))
    mouse_position_label.after(100, update_mouse_position)


# Start update mouse position
update_mouse_position()

# icon_bitmap
root.iconbitmap("")

root.bind("<Control-i>", insert_mouse_position)

total_time_label = tk.Label(root, text="", font=("Arial", 12))
total_time_label.pack(pady=10)

fe.update_timer(total_time_label, fe.TIME_LEFT)


# label for completed/remaining mining runs
def update_mining_runs(actual: int, wanted: int):
    mining_runs_result.config(text=f"Completed runs: {actual}/{wanted}")


mining_runs_result = tk.Label(root, text="", font=("Arial", 12))
mining_runs_result.pack(pady=10)
update_mining_runs(0, 0)

# Create a label to display the countdown timer
cargo_hold_time_label = tk.Label(root, text="", font=("Arial", 12))
cargo_hold_time_label.pack(pady=10)

# Start updating the countdown timer
fe.update_timer(cargo_hold_time_label, fe.CARGO_LOAD_TIME)

# Create a label to display the countdown timer
next_reset_label = tk.Label(root, text="", font=("Arial", 12))
next_reset_label.pack(pady=10)

# Start updating the countdown timer
fe.update_timer(next_reset_label, fe.NEXT_RESET_IN)

# Start Tkinter Window
root.mainloop()
