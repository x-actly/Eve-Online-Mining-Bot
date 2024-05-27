import copy
import json
import random
import subprocess
import time
from tkinter import Label
from typing import Callable, List

import psutil
import pyautogui
from loguru import logger

# Functions
########################################################

# Initialize a variable to store the last selected coordinate
last_selected_coord: List[int] = []


def get_random_coord(coords: List[List[int]]) -> List[int]:
    global last_selected_coord
    available_coords = [coord for coord in coords if coord != last_selected_coord]
    selected_coord = random.choice(available_coords)
    last_selected_coord = selected_coord
    return selected_coord


def auto_dock_to_station(coords: List[int]) -> None:
    x, y = coords
    click_top_left_circle_menu(x, y)
    sleep_and_log(1)
    click_top_center_circle_menu(x, y)
    sleep_and_log(0.5)
    translate_key_combo("Ctrl-S")


def undock(x: int, y: int) -> None:
    logger.info("undocking...")
    # undock
    time = random.uniform(1, 2)
    pyautogui.moveTo(x, y, duration=time)
    pyautogui.mouseDown(button="left")
    sleep_and_log(0.5)
    pyautogui.mouseUp(button="left")
    sleep_and_log(0.5)


def set_hardener_online(key_combos: List[str]) -> None:
    logger.info("starting hardeners...")
    for index, key in enumerate(key_combos):
        logger.info(f"Activating hardener {index + 1} with key {key}")
        translate_key_combo(key)
        time.sleep(0.5)


def click_circle_menu(x: int, y: int, x_offset: int, y_offset: int) -> None:
    logger.info("clicking on the circle menu...")
    pyautogui.moveTo(x, y)
    pyautogui.mouseDown()
    sleep_and_log(0.5)
    pyautogui.moveRel(x_offset, y_offset, 1)
    pyautogui.mouseUp()
    sleep_and_log(0.5)


def click_top_left_circle_menu(x: int, y: int) -> None:
    x_offset = -50
    y_offset = random.randint(-51, -49)
    click_circle_menu(x, y, x_offset, y_offset)


def click_top_center_circle_menu(x: int, y: int) -> None:
    x_offset = 0
    y_offset = random.randint(-51, -49)
    click_circle_menu(x, y, x_offset, y_offset)


def drone_out(x: int, y: int) -> None:
    logger.info("launching drones...")
    # drone out, random click in space
    pyautogui.click(x, y, button="left", duration=random.uniform(1, 2))
    # drone out
    sleep_and_log(3)
    pyautogui.keyDown("shift")
    pyautogui.press("f")
    sleep_and_log(0.5)
    # Umschalt loslassen
    pyautogui.keyUp("shift")


def drone_in() -> None:
    logger.info("drones returning to bay...")
    # drone in
    pyautogui.keyDown("shift")
    pyautogui.press("r")
    sleep_and_log(0.5)
    pyautogui.keyUp("shift")


def clear_cargo(x: int, y: int) -> None:
    random_time = random.uniform(3, 4)
    logger.info("clearing cargo...")
    # clear cargo
    pyautogui.click(x + 175, y + 165, button="left", duration=random_time)
    pyautogui.mouseDown(button="left")
    pyautogui.dragRel(-175, -165, duration=random_time, button="left")
    pyautogui.mouseUp(button="left")
    pyautogui.mouseDown(button="left")
    pyautogui.dragRel(0, -250, duration=random_time, button="left")
    pyautogui.mouseUp(button="left")
    sleep_and_log(random_time)


# Mining Script
########################################################


def mining_behaviour(
    tx1: int,
    ty1: int,
    tx2: int,
    ty2: int,
    mining_reset: int,
    mining_loop: float,
    rm_x: int,
    rm_y: int,
    unlock_all_targets_keys: str,
    activate_eve_window: Callable[[], None],
    is_stopped: Callable[[], bool],
    auto_reset_miners: bool,
) -> None:

    # start time to counter looptime
    start_time = time.time()

    while True:
        activate_eve_window()
        if unlock_all_targets_keys:
            # reset mouse assigned mining laser random in space
            pyautogui.moveTo(rm_x, rm_y)
            pyautogui.click(button="left")
            logger.info(f"Using unlock all targets key: {unlock_all_targets_keys}")
            for key in unlock_all_targets_keys.split("-"):
                pyautogui.keyDown(key)
            sleep_and_log(0.5)
            for key in unlock_all_targets_keys.split("-"):
                pyautogui.keyUp(key)
            sleep_and_log(0.5)
        else:
            logger.info("Manually unlocking targets 1 and 2")
            # reset target 1
            pyautogui.moveTo(tx1, ty1)
            pyautogui.keyDown("ctrl")
            pyautogui.keyDown("shift")
            pyautogui.click(button="left")
            pyautogui.keyUp("ctrl")
            pyautogui.keyUp("shift")

            sleep_and_log(0.5)

            # reset target 2
            pyautogui.moveTo(tx2, ty2)
            pyautogui.keyDown("ctrl")
            pyautogui.keyDown("shift")
            pyautogui.click(button="left")
            pyautogui.keyUp("ctrl")
            pyautogui.keyUp("shift")

        if auto_reset_miners:
            # reset mininglaser 1
            pyautogui.keyDown("f1")
            sleep_and_log(0.5)
            pyautogui.keyUp("f1")

            sleep_and_log(1)

            # reset mininglaser 2
            pyautogui.keyDown("f2")
            sleep_and_log(0.5)
            pyautogui.keyUp("f2")

        # reset mouse assigned mining laser random in space
        pyautogui.moveTo(rm_x, rm_y)
        pyautogui.click(button="right")

        sleep_and_log(0.5)

        # console
        logger.info("mining...")

        # target 1
        pyautogui.moveTo(tx1, ty1)
        pyautogui.keyDown("ctrl")
        pyautogui.click(button="left")
        pyautogui.keyUp("ctrl")
        sleep_and_log(3)
        activate_eve_window()
        pyautogui.press("f1")

        sleep_and_log(0.5)

        # target 2
        pyautogui.moveTo(tx2, ty2)
        pyautogui.keyDown("ctrl")
        pyautogui.click(button="left")
        pyautogui.keyUp("ctrl")
        sleep_and_log(3)
        activate_eve_window()
        # second left click to focus the second target
        pyautogui.click(button="left")
        pyautogui.press("f2")

        # reset every 170 seconds (depends on mining barge)
        set_next_reset(mining_reset, NEXT_RESET_IN)
        sleep_and_log(mining_reset)
        logger.info("reset mining script...")

        elapsed_time = time.time() - start_time
        if elapsed_time >= mining_loop or is_stopped():
            logger.info("Done mining")
            break


# Constants for timers
NEXT_RESET_IN = "Next reset in"
CARGO_LOAD_TIME = "Cargo loaded in"

# Dictionary to store next reset time for each counter
timers = {NEXT_RESET_IN: 0.0, CARGO_LOAD_TIME: 0.0}


# Function to update the countdown timer
def update_timer(label: Label, counter: str) -> None:
    remaining_time = max(0, timers[counter] - time.time())
    remaining_str = get_remaining_time(remaining_time)

    # Update the label text with the remaining time
    label.config(text=f"{counter}: {remaining_str}")

    # Schedule the update function to run again after 1 second
    label.after(1000, update_timer, label, counter)


def get_remaining_time(remaining_time: float) -> str:
    # Calculate days, hours, minutes, and seconds
    days = int(remaining_time // (60 * 60 * 24))
    remaining_time %= 60 * 60 * 24
    hours = int(remaining_time // (60 * 60))
    remaining_time %= 60 * 60
    minutes = int(remaining_time // 60)
    seconds = int(remaining_time % 60)

    # Format the remaining time
    remaining_str = ""
    if days > 0:
        remaining_str += f"{days}d "
    if hours > 0:
        remaining_str += f"{hours}h "
    remaining_str += f"{minutes:02d}m {seconds:02d}s"
    return remaining_str


def translate_key_combo(key_combo: str) -> None:
    if key_combo:
        keys = key_combo.split("-")
        with pyautogui.hold(keys[0].lower()):
            if len(keys) > 1:
                pyautogui.press(keys[1].lower())


# Function to set the next reset time for a specific counter
def set_next_reset(time_interval: float, counter: str) -> None:
    timers[counter] = time.time() + time_interval


def sleep_and_log(seconds: float) -> None:
    seconds = seconds + random.uniform(0, 1)
    logger.trace("sleeping {} seconds", seconds)
    time.sleep(seconds)

# Sanderling, eve memory reading
############################################################

root_address: str = None
current_pid: str = None

def get_process_pid_by_name(process_name: str) -> str:
    """
    Retrieve a proccess pid by process name

    :param process_name: The name of the process to search for.
    :return: The pid or none
    """
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # Check if the process name matches
            if proc.info['name'] == process_name:
                return str(proc.info['pid'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    raise Exception("process " + process_name + " was not found")

def read_eve_process_memory(pid: str | None  = None) -> dict:
    global root_address, current_pid

    pid = pid or get_process_pid_by_name("exefile.exe")

    # Define the path to your .exe file and the arguments
    exe_path = 'read-memory-64-bit.exe'
    arguments = ['read-memory-eve-online', '--pid', pid]

    # Check if the PID has changed and reset root_address if it has
    if pid != current_pid:
        root_address = None
        current_pid = pid
    
    # Add --root-address only if root_address is defined
    if root_address:
        arguments += ['--root-address', root_address]

    # Run the .exe file with arguments and capture the output
    result = subprocess.run([exe_path] + arguments, capture_output=True, text=True)

    # Check if the command was successful
    if result.returncode == 0:
        output = result.stdout
        data = json.loads(output)
        
        # Update root_address with pythonObjectAddress from the JSON response
        if 'pythonObjectAddress' in data:
            root_address = data['pythonObjectAddress']
        
        return data
    else:
        raise Exception(f"Error running the executable: {result.stderr}")

def write_to_file(str: str) -> None:
    f = open("demofile3.json", "w")
    f.write(str)
    f.close()

def find_element_by_property(json_obj, property_name, property_value):
    """
    Recursively searches through the JSON object to find the first element with the specified property.

    Parameters:
    json_obj (dict or list): The JSON object to search through.
    property_name (str): The name of the property to search for.
    property_value (str): The value of the property to search for.

    Returns:
    dict or None: The JSON object containing the specified property or None if not found.
    """
    if isinstance(json_obj, dict):
        # Check if the current dictionary has the specified property
        if json_obj.get(property_name) == property_value:
            return json_obj
        
        # Recursively search through each value in the dictionary
        for key, value in json_obj.items():
            result = find_element_by_property(value, property_name, property_value)
            if result is not None:
                return result

    elif isinstance(json_obj, list):
        # Recursively search through each item in the list
        for item in json_obj:
            result = find_element_by_property(item, property_name, property_value)
            if result is not None:
                return result
    
    # If no matching element is found, return None
    return None

def find_elements_by_property(json_obj, property_name, property_value):
    """
    Recursively searches through the JSON object to find all elements with the specified property.

    Parameters:
    json_obj (dict or list): The JSON object to search through.
    property_name (str): The name of the property to search for.
    property_value (str): The value of the property to search for.

    Returns:
    list: A list of JSON objects containing the specified property.
    """
    results = []

    if isinstance(json_obj, dict):
        # Check if the current dictionary has the specified property
        if json_obj.get(property_name) == property_value:
            results.append(json_obj)
        
        # Recursively search through each value in the dictionary
        for key, value in json_obj.items():
            results.extend(find_elements_by_property(value, property_name, property_value))

    elif isinstance(json_obj, list):
        # Recursively search through each item in the list
        for item in json_obj:
            results.extend(find_elements_by_property(item, property_name, property_value))

    return results

def adjust_display_positions(json_obj, parent_display=None, is_top_level=True):
    if is_top_level:
        json_obj = copy.deepcopy(json_obj)

    if parent_display is None:
        parent_display = {'_displayX': 0, '_displayY': 0}

    if isinstance(json_obj, dict):
        # Check if the current dictionary has display position attributes
        if 'dictEntriesOfInterest' in json_obj:
            for attr in ['_displayX', '_displayY']:
                if attr in json_obj['dictEntriesOfInterest']:
                    if isinstance(json_obj['dictEntriesOfInterest'][attr], dict):
                        if 'int_low32' in json_obj['dictEntriesOfInterest'][attr]:
                            json_obj['dictEntriesOfInterest'][attr]['int_low32'] = json_obj['dictEntriesOfInterest'][attr]['int_low32'] + parent_display[attr]
                    else:
                        json_obj['dictEntriesOfInterest'][attr] += parent_display[attr]

        current_display = {
            '_displayX': json_obj.get('dictEntriesOfInterest', {}).get('_displayX', {'int_low32': 0}).get('int_low32', 0)
            if isinstance(json_obj.get('dictEntriesOfInterest', {}).get('_displayX', 0), dict) 
            else json_obj.get('dictEntriesOfInterest', {}).get('_displayX', 0),

            '_displayY': json_obj.get('dictEntriesOfInterest', {}).get('_displayY', {'int_low32': 0}).get('int_low32', 0)
            if isinstance(json_obj.get('dictEntriesOfInterest', {}).get('_displayY', 0), dict) 
            else json_obj.get('dictEntriesOfInterest', {}).get('_displayY', 0)
        }

        if 'children' in json_obj and isinstance(json_obj['children'], list):
            for child in json_obj['children']:
                adjust_display_positions(child, current_display, is_top_level=False)

    elif isinstance(json_obj, list):
        for item in json_obj:
            adjust_display_positions(item, parent_display, is_top_level=False)

    if is_top_level:
        return json_obj

def find_undock_button(json_obj):
    # Find the LobbyWnd object
    lobby_window = find_element_by_property(json_obj, 'pythonObjectTypeName', 'LobbyWnd')
    # Find the first button with the text 'Undock'
    return find_element_by_property(lobby_window, '_setText', 'Undock')

def find_bookmarks(json_obj):
    # Find all PlaceEntry objects
    place_entries = find_elements_by_property(json_obj, 'pythonObjectTypeName', 'PlaceEntry')

    bookmarks = []
    # For each PlaceEntry, find the first EveLabelMedium
    for place_entry in place_entries:
        eve_label_medium = find_element_by_property(place_entry, 'pythonObjectTypeName', 'EveLabelMedium')
        if eve_label_medium is not None:
            bookmarks.append(eve_label_medium)

    return bookmarks

def calculate_center_position(json_obj):
    """
    Calculate the center position of a given object.

    WARNING: This function should only be used for leaf nodes.

    Parameters:
    json_obj (dict): The JSON object to calculate the center position for.

    Returns:
    dict: The JSON object with the center position added.
    """
    json_obj = copy.deepcopy(json_obj)

    data = json_obj.get('dictEntriesOfInterest', json_obj)

    display_width = min(data.get('_displayWidth', 0), 100)
    display_height = data.get('_displayHeight', 0)
    display_x = data.get('_displayX', 0)
    display_y = data.get('_displayY', 0)

    if isinstance(display_width, dict):
        display_width = display_width.get('int_low32', 0)
    if isinstance(display_height, dict):
        display_height = display_height.get('int_low32', 0)

    data['_centerX'] = display_x + (display_width / 2)
    data['_centerY'] = display_y + (display_height / 2)

    return json_obj