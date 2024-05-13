import os
import platform
import re
import sys
import threading
import time
import tkinter as tk
import tkinter.font as tkFont
from datetime import datetime
from typing import Any, List

import pyautogui
from loguru import logger

from Bot import config as cfg
from Bot import functions as fe

config = cfg.ConfigHandler("config.properties")  # type: ignore

logger.remove()

log_level = config.get_log_level()
logger.add(
    "client.log",
    level=log_level,
    format="[{time}] [{level}] {name}:{function}:{line} - {message}",
    colorize=False,
    backtrace=True,
    diagnose=True,
    rotation="1 day",
    retention="31 days",
)

logger.add(sys.stdout, level=log_level)

# When cargo hold is full, the ship will dock up and unload cargo, undock and warp to another belt
cargo_loading_time_adjustment = config.get_cargo_loading_time_adjustment()

# take screenshots after clearing cargo
take_screenshots = config.get_take_screenshots()

# warping to belt time
warping_time = config.get_warping_time()

# auto reset miners before selecting and activating new targets
auto_reset_miners = config.get_auto_reset_miners()

# CONSTANTS

SMALL_SLEEP = 12
MEDIUM_SLEEP = 70
LONG_SLEEP = 100

# globals (just for reference, not actually needed)

stop_flag = False
selected_eve_window: Any = None

# Mining functions
#########################################################


def get_estimated_run_time(
    mining_runs: int, cargo_loading_time: float, cargo_loading_time_adjustment: int
) -> float:
    return mining_runs * (
        cargo_loading_time + (cargo_loading_time_adjustment if mining_runs > 1 else 0)
    )


def get_cargo_loading_time(mining_hold: int, mining_yield: float) -> float:
    if mining_hold == 0:
        return 0
    time = mining_hold / mining_yield if mining_yield > 0 else 0
    if time < LONG_SLEEP:
        logger.error("Mining yield misconfiguration: loading time < warp-out time.")
    return time


# GUI settings
#########################################################

# Create Tkinter window
root = tk.Tk()
root.wm_attributes("-topmost", 1)
root.title("Mining Bot Owl-Edition")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 480
window_height = 720
x_pos = screen_width - window_width
y_pos = 0
root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

# Make window not resizable
root.resizable(False, True)

# close everything on window close
root.protocol("WM_DELETE_WINDOW", lambda: os._exit(0))

# Create frame for input and buttons
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# Create frame for start- and stop buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# EVE window selection
#########################################################


def get_windows_with_title(title) -> List[Any]:
    if platform.system() == "Windows":
        # since there is not types for this libary, we ignore the types
        import pygetwindow as gw  # type: ignore

        return gw.getWindowsWithTitle(title)
    else:
        return []


# For some reason cant use global reference as in the function below
# propably because its passed in lambda
def activate_eve_window() -> None:
    selected_eve_window = globals().get("selected_eve_window")
    if selected_eve_window is not None:
        selected_eve_window.activate()


def on_window_select(selection: str) -> None:
    global selected_eve_window
    windows = get_windows_with_title(selection)
    if windows:
        selected_eve_window = windows[0]


# Label for the EVE window selector
window_label = tk.Label(input_frame, text="Select EVE window:")
window_label.grid(row=0, column=0, sticky="w")

# Get list of EVE windows
window_titles: List[str] = []
eve_windows = get_windows_with_title("EVE -")
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
        logger.info("Selected the first EVE window")
else:
    eve_window.set("No EVE windows")


# Function to update the OptionMenu text
def update_option_menu(selection: str) -> None:
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


def format_coo(coo: List[int]) -> str:
    return ", ".join(map(str, coo))


def format_list_coo(coo_list: List[List[int]]) -> str:
    return "\n".join(format_coo(coo) for coo in coo_list)


# Label for the number of mining runs
entry_label = tk.Label(input_frame, text="Set number of mining runs:")
entry_label.grid(row=1, column=0, sticky="w")

# Entry field for the number of mining runs
entry_var = tk.StringVar()
entry = tk.Entry(input_frame, textvariable=entry_var)
entry.grid(row=1, column=1, padx=5, pady=4, sticky="w")
entry.insert(tk.END, config.get_mining_runs())

# Mining Hold
#########################################################

# Create input field for mining hold in m3
mining_hold_var = tk.StringVar()
mining_hold_label = tk.Label(input_frame, text="Mining Hold (m3):")
mining_hold_label.grid(row=2, column=0, sticky="w")
mining_hold_entry = tk.Entry(input_frame, textvariable=mining_hold_var)
mining_hold_entry.grid(row=2, column=1, padx=5, pady=4, sticky="w")
mining_hold_entry.insert(tk.END, config.get_mining_hold())

# Mining Yield
#########################################################

# Create input field for mining yield in m3/s
mining_yield_var = tk.StringVar()
mining_yield_label = tk.Label(input_frame, text="Mining Yield (m3/s):")
mining_yield_label.grid(row=3, column=0, sticky="w")
mining_yield_entry = tk.Entry(input_frame, textvariable=mining_yield_var)
mining_yield_entry.grid(row=3, column=1, padx=5, pady=4, sticky="w")
mining_yield_entry.insert(tk.END, config.get_mining_yield())

# Undock
#########################################################

# create input field for undock coordinates
undock_coo_label = tk.Label(input_frame, text="Undock-Button Position:")
undock_coo_label.grid(row=4, column=0, sticky="w")
undock_coo_entry = tk.Entry(input_frame)
undock_coo_entry.grid(row=4, column=1, padx=5, pady=4, sticky="w")
undock_coo_entry.insert(tk.END, format_coo(config.get_undock_coo()))


def test_undock():
    save_properties()
    pyautogui.moveTo(*config.get_undock_coo())


undock_test_button = tk.Button(
    input_frame,
    text="Test",
    command=lambda: execute_and_enable(undock_test_button, test_undock),
)
undock_test_button.grid(row=4, column=2, padx=5, pady=4, sticky="w")

# Clear Cargo Position
#########################################################

# Create input field for clear-cargo position
clear_cargo_coo_label = tk.Label(input_frame, text="Clear-Cargo Position:")
clear_cargo_coo_label.grid(row=5, column=0, sticky="w")
clear_cargo_coo_entry = tk.Entry(input_frame)
clear_cargo_coo_entry.grid(row=5, column=1, padx=5, pady=4, sticky="w")
clear_cargo_coo_entry.insert(tk.END, format_coo(config.get_clear_cargo_coo()))

# check if the coordinate is set correctly


def execute_and_enable(button, func):
    # Disable the button to prevent further clicks.
    button.config(state=tk.DISABLED)

    def execute_function():
        func()

        # Enable the button after the function completes.
        root.after(1, lambda: button.config(state=tk.NORMAL))

    # Run function in a separate thread
    thread = threading.Thread(target=execute_function)
    thread.start()


def test_clear_cargo():
    save_properties()
    fe.clear_cargo(*config.get_clear_cargo_coo())


clear_cargo_check_button = tk.Button(
    input_frame,
    text="Test",
    compound="left",
    command=lambda: execute_and_enable(clear_cargo_check_button, test_clear_cargo),
)
clear_cargo_check_button.grid(row=5, column=2, padx=5, pady=4, sticky="w")

# Target-One-Position
########################################################

# Create input field for target-one position
target_one_coo_label = tk.Label(input_frame, text="Target-One Overview Position:")
target_one_coo_label.grid(row=6, column=0, sticky="w")
target_one_coo_entry = tk.Entry(input_frame)
target_one_coo_entry.grid(row=6, column=1, padx=5, pady=4, sticky="w")
target_one_coo_entry.insert(tk.END, format_coo(config.get_target_one_coo()))


def test_target_one():
    save_properties()
    pyautogui.moveTo(*config.get_target_one_coo())


target_one_coo_test_button = tk.Button(
    input_frame,
    text="Test",
    command=lambda: execute_and_enable(
        target_one_coo_test_button,
        test_target_one,
    ),
)
target_one_coo_test_button.grid(row=6, column=2, padx=5, pady=4, sticky="w")

# Target-Two-Position
#######################################################

# Create input field for target-two position
target_two_coo_label = tk.Label(input_frame, text="Target-Two Overview Position:")
target_two_coo_label.grid(row=7, column=0, sticky="w")
target_two_coo_entry = tk.Entry(input_frame)
target_two_coo_entry.grid(row=7, column=1, padx=5, pady=4, sticky="w")
target_two_coo_entry.insert(tk.END, format_coo(config.get_target_two_coo()))


def test_target_two():
    save_properties()
    pyautogui.moveTo(*config.get_target_two_coo())


target_two_coo_test_button = tk.Button(
    input_frame,
    text="Test",
    command=lambda: execute_and_enable(
        target_one_coo_test_button,
        test_target_two,
    ),
)
target_two_coo_test_button.grid(row=7, column=2, padx=5, pady=4, sticky="w")

# Target-Reset-Position
#######################################################

# Create input field for mouse reset
mouse_reset_coo_label = tk.Label(input_frame, text="Mouse Reset Position:")
mouse_reset_coo_label.grid(row=8, column=0, sticky="w")
mouse_reset_coo_entry = tk.Entry(input_frame)
mouse_reset_coo_entry.grid(row=8, column=1, padx=5, pady=4, sticky="w")
mouse_reset_coo_entry.insert(tk.END, format_coo(config.get_mouse_reset_coo()))


def test_mouse_reset():
    save_properties()
    pyautogui.moveTo(*config.get_mouse_reset_coo())


mouse_reset_coo_test_button = tk.Button(
    input_frame,
    text="Test",
    command=lambda: execute_and_enable(
        target_one_coo_test_button,
        test_mouse_reset,
    ),
)
mouse_reset_coo_test_button.grid(row=8, column=2, padx=5, pady=4, sticky="w")

# Home Position
##########################################################

# Create input field for warp-to position
home_coo_label = tk.Label(input_frame, text="Home Bookmark:")
home_coo_label.grid(row=9, column=0, sticky="w")
home_coo_entry = tk.Entry(input_frame)
home_coo_entry.grid(row=9, column=1, padx=5, pady=4, sticky="w")
home_coo_entry.insert(tk.END, format_coo(config.get_home_coo()))


def test_warp_to():
    save_properties()
    pyautogui.moveTo(*config.get_home_coo())


home_coo_test_button = tk.Button(
    input_frame,
    text="Test",
    command=lambda: execute_and_enable(
        target_one_coo_test_button,
        test_warp_to,
    ),
)
home_coo_test_button.grid(row=9, column=2, padx=5, pady=4, sticky="w")

# Belt Bookmarks
#########################################################

# Create input field for mining position
mining_coo_label = tk.Label(input_frame, text="Belt Bookmarks:")
mining_coo_label.grid(row=10, column=0, sticky="w")
mining_coo_entry = tk.Text(input_frame, width=15, height=5)
mining_coo_entry.grid(row=10, column=1, padx=5, pady=4, sticky="w")
mining_coo_entry.insert(tk.END, format_list_coo(config.get_mining_coo()))

#########################################################

# Create start button
start_button = tk.Button(button_frame, text="Start")
start_button.grid(row=0, column=0, padx=(0, 10), pady=10, ipadx=5)

# Create stop button
stop_button = tk.Button(button_frame, text="Stop")
stop_button.grid(row=0, column=1, padx=(10, 0), pady=10, ipadx=5)
stop_button.config(state=tk.DISABLED)

panic_button = tk.Button(button_frame, text="Panic", bg="red", fg="white")
panic_button.grid(row=0, column=2, padx=(10, 0), pady=10, ipadx=5)

# Create global save button
save_button = tk.Button(button_frame, text="Save")
save_button.grid(row=0, column=3, padx=(20, 0), pady=10, ipadx=5)

########################################################


def insert_mouse_position(event) -> None:
    x, y = pyautogui.position()
    if isinstance(event.widget, tk.Text):
        event.widget.insert(tk.END, f"\n{x}, {y}")
    elif isinstance(event.widget, tk.Entry):
        event.widget.delete(0, tk.END)
        event.widget.insert(tk.END, f"{x}, {y}")


# Create a label to display the mouse position
mouse_position_label = tk.Label(root, text="")
mouse_position_label.pack(pady=10)

bold_font = tkFont.Font(weight="bold")


# Function to update the mouse position
def update_mouse_position() -> None:
    x, y = pyautogui.position()
    mouse_position_label.config(text=f"Mouse-Position: {x}, {y}", font=("Arial", 12))
    mouse_position_label.after(100, update_mouse_position)


# Start update mouse position
update_mouse_position()

# icon_bitmap
root.iconbitmap("")

root.bind("<Control-i>", insert_mouse_position)


def update_estimated_run_time(*args) -> None:
    config.set_mining_runs(entry_var.get())
    config.set_mining_hold(mining_hold_var.get())
    config.set_mining_yield(mining_yield_var.get())
    if mining_hold_var.get() and mining_yield_var.get() and entry_var.get():
        estimated_run_time = get_estimated_run_time(
            mining_runs=config.get_mining_runs(),
            cargo_loading_time=get_cargo_loading_time(
                config.get_mining_hold(), config.get_mining_yield()
            ),
            cargo_loading_time_adjustment=cargo_loading_time_adjustment,
        )
        total_time_label.config(
            text=f"Estimated time to complete: {fe.get_remaining_time(estimated_run_time)}"
        )
        start_button.config(state=tk.ACTIVE)
    else:
        total_time_label.config(text="Estimated time to complete: N/A")
        start_button.config(state=tk.DISABLED)


mining_hold_var.trace_add("write", update_estimated_run_time)
mining_yield_var.trace_add("write", update_estimated_run_time)
entry_var.trace_add("write", update_estimated_run_time)

total_time_label = tk.Label(root, text="", font=("Arial", 12))
total_time_label.pack(pady=10)

update_estimated_run_time()


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


def disable_fields() -> None:
    # Disable input fields
    entry.config(state=tk.DISABLED)
    undock_coo_entry.config(state=tk.DISABLED)
    clear_cargo_coo_entry.config(state=tk.DISABLED)
    mining_hold_entry.config(state=tk.DISABLED)
    mining_yield_entry.config(state=tk.DISABLED)
    target_one_coo_entry.config(state=tk.DISABLED)
    target_two_coo_entry.config(state=tk.DISABLED)
    mouse_reset_coo_entry.config(state=tk.DISABLED)
    home_coo_entry.config(state=tk.DISABLED)
    mining_coo_entry.config(state=tk.NORMAL)
    mining_coo_entry.tag_configure("disabled", foreground="gray")
    mining_coo_entry.config(state=tk.DISABLED)
    mining_coo_entry.insert(tk.END, format_list_coo(config.get_mining_coo()))
    mining_coo_entry.tag_add("disabled", "1.0", "end")

    # Disable buttons
    start_button.config(state=tk.DISABLED)
    save_button.config(state=tk.DISABLED)
    clear_cargo_coo_entry.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)


def enable_fields() -> None:
    # Enable input fields
    entry.config(state=tk.NORMAL)
    undock_coo_entry.config(state=tk.NORMAL)
    clear_cargo_coo_entry.config(state=tk.NORMAL)
    mining_hold_entry.config(state=tk.NORMAL)
    mining_yield_entry.config(state=tk.NORMAL)
    target_one_coo_entry.config(state=tk.NORMAL)
    target_two_coo_entry.config(state=tk.NORMAL)
    mouse_reset_coo_entry.config(state=tk.NORMAL)
    home_coo_entry.config(state=tk.NORMAL)
    mining_coo_entry.config(state=tk.NORMAL)
    mining_coo_entry.tag_remove("disabled", "1.0", "end")

    # Enable buttons
    start_button.config(state=tk.NORMAL)
    save_button.config(state=tk.NORMAL)
    clear_cargo_coo_entry.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)


def stop_function() -> None:
    global stop_flag
    stop_flag = True
    stop_button.config(state=tk.DISABLED)
    logger.warning("The mining script will end on next reset!")


def panic_function() -> None:
    logger.warning("Panic! Bring in drones and dock to station")
    panic_button.config(state=tk.DISABLED)

    def execute_function() -> None:
        stop_function()
        activate_eve_window()
        x, y = config.get_mouse_reset_coo()
        pyautogui.moveTo(x, y)
        pyautogui.click(button="left")
        fe.drone_in()
        fe.sleep_and_log(1)
        fe.auto_dock_to_station(config.get_home_coo())
        os._exit(0)

    thread = threading.Thread(target=execute_function)
    thread.start()


def save_properties() -> None:
    config.set_mining_runs(entry.get())
    config.set_undock_coo(undock_coo_entry.get())
    config.set_clear_cargo_coo(clear_cargo_coo_entry.get())
    config.set_mining_hold(mining_hold_entry.get())
    config.set_mining_yield(mining_yield_entry.get())
    config.set_target_one_coo(target_one_coo_entry.get())
    config.set_target_two_coo(target_two_coo_entry.get())
    config.set_mouse_reset_coo(mouse_reset_coo_entry.get())
    config.set_home_coo(home_coo_entry.get())
    config.set_mining_coo(mining_coo_entry.get(1.0, tk.END).strip())
    config.save()
    logger.info("Configuration updated")


def repeat_function(cargo_loading_time: float) -> None:
    disable_fields()
    actual_mining_runs = 0
    mining_runs = config.get_mining_runs()
    update_mining_runs(actual_mining_runs, mining_runs)
    while not stop_flag and actual_mining_runs < mining_runs:
        activate_eve_window()
        fe.set_next_reset(cargo_loading_time, fe.CARGO_LOAD_TIME)
        loaded_in_str = fe.get_remaining_time(cargo_loading_time)
        logger.info(f"The mining cargo is filled in about {loaded_in_str}")
        time.sleep(1)
        undock_x, undock_y = config.get_undock_coo()
        fe.undock(x=undock_x, y=undock_y)
        fe.sleep_and_log(SMALL_SLEEP)
        fe.set_hardener_online(config.get_hardener_keys())
        item = fe.get_random_coord(config.get_mining_coo())
        fe.click_top_left_circle_menu(item[0], item[1])
        fe.sleep_and_log(warping_time)
        activate_eve_window()
        rm_x, rm_y = config.get_mouse_reset_coo()
        fe.drone_out(x=rm_x, y=rm_y)
        tx1, ty1 = config.get_target_one_coo()
        tx2, ty2 = config.get_target_two_coo()
        fe.mining_behaviour(
            tx1=tx1,
            ty1=ty1,
            tx2=tx2,
            ty2=ty2,
            mining_reset=config.get_mining_reset_timer(),
            mining_loop=cargo_loading_time,
            rm_x=rm_x,
            rm_y=rm_y,
            unlock_all_targets_keys=config.get_unlock_all_targets_key(),
            activate_eve_window=activate_eve_window,
            is_stopped=lambda: stop_flag,
            auto_reset_miners=auto_reset_miners,
        )
        activate_eve_window()
        fe.drone_in()
        fe.sleep_and_log(SMALL_SLEEP)
        fe.auto_dock_to_station(config.get_home_coo())
        # sleep long enough to be in station when program wakes up
        fe.sleep_and_log(LONG_SLEEP)
        # docking will take some time, need to refocus window
        activate_eve_window()
        cg_x, cg_y = config.get_clear_cargo_coo()
        fe.clear_cargo(x=cg_x, y=cg_y)
        actual_mining_runs += 1
        update_mining_runs(actual_mining_runs, mining_runs)
        if take_screenshots:
            img = pyautogui.screenshot()
            now_str = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            img.save(f"eve_screenshot_{now_str}.png")
    total_runs_str = f"{actual_mining_runs}/{mining_runs}"
    logger.info(f"Completed {total_runs_str} mining sessions")
    enable_fields()


def start_function() -> None:
    global stop_flag
    stop_flag = False
    save_properties()
    mining_runs = config.get_mining_runs()
    mining_hold_value = config.get_mining_hold()
    mining_yield_value = config.get_mining_yield()
    mining_reset_timer = config.get_mining_reset_timer()
    logger.info("The mining script will run {} mining runs!", mining_runs)
    logger.info("Using miner reset timer of {} seconds.", mining_reset_timer)
    cargo_loading_time = get_cargo_loading_time(mining_hold_value, mining_yield_value)
    estimated_run_time = get_estimated_run_time(
        mining_runs=mining_runs,
        cargo_loading_time=cargo_loading_time,
        cargo_loading_time_adjustment=cargo_loading_time_adjustment,
    )
    estimated_run_time_str = fe.get_remaining_time(estimated_run_time)
    logger.info(f"Estimate for completion is {estimated_run_time_str}")
    thread = threading.Thread(
        target=lambda: repeat_function(cargo_loading_time=cargo_loading_time)
    )
    thread.start()


start_button.config(command=start_function)
stop_button.config(command=stop_function)
panic_button.config(command=panic_function)
save_button.config(command=save_properties)


def start() -> None:
    logger.info("Starting bot")
    logger.trace("Hi")
    # Start Tkinter Window
    root.mainloop()
