import platform
import random
import re
import time
from tkinter import Label
from typing import Callable, List, NamedTuple

import PIL
import pyautogui
import pytesseract  # type: ignore
from loguru import logger

# Tesseract functions
########################################################

CLOSE_WORDS_THRESHOLD = 30
LOCATION_SPOT_PATTERN = re.compile(r"spot (\d+)", re.IGNORECASE)
HOME_SPOT_PATTERN = re.compile(r"home", re.IGNORECASE)
ASTEROID_SPOT_PATTERN = re.compile(r"(\d+\s*(?:km|m))\s+asteroid", re.IGNORECASE)


class Sentence(NamedTuple):
    word: str
    x: float
    y: float
    w: float
    h: float
    c_x: float
    c_y: float


def get_mining_spots(sentences: List[Sentence]) -> List[Sentence]:
    return [item for item in sentences if LOCATION_SPOT_PATTERN.search(item[0])]


def get_distance_from_str(s: str) -> int:
    if s.endswith("km"):
        return int(s.split(" ")[0]) * 1000
    if s.endswith("m"):
        return int(s.split(" ")[0])
    return 20000  # default to 100km which is basically too far


def get_asteroids(sentences: List[Sentence]) -> List[Sentence]:
    processed_sentences = [
        (match.group(1), item)
        for item in sentences
        for match in [ASTEROID_SPOT_PATTERN.search(item.word)]
        if match
    ]
    sorted_sentences = sorted(
        processed_sentences, key=lambda x: get_distance_from_str(x[0])
    )
    return [sentence for _, sentence in sorted_sentences]


def get_undock_button(sentences: List[Sentence]) -> Sentence | None:
    return next((item for item in sentences if item[0] == "Undock"), None)


def get_home_spot(sentences: List[Sentence]) -> Sentence | None:
    return next((item for item in sentences if HOME_SPOT_PATTERN.search(item[0])), None)


def collect_sentences(screenshot: PIL.Image.Image) -> List[Sentence]:
    # Perform OCR on the screenshot with English language setting
    d = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)

    # Initialize variables to store combined words and their coordinates
    combined_words = []
    current_word = ""
    x_start, x_end, y_start, y_end = (
        float("inf"),
        float("-inf"),
        float("inf"),
        float("-inf"),
    )

    # Loop through detected text boxes
    for i in range(len(d["level"])):
        level = d["level"][i]
        text = d["text"][i].strip()

        # Only consider text boxes containing meaningful words
        if level == 5 and text:
            x, y, w, h = d["left"][i], d["top"][i], d["width"][i], d["height"][i]

            # Check if the word is close to the previous word horizontally
            if (
                abs(x - x_end) <= CLOSE_WORDS_THRESHOLD
            ):  # Adjust the threshold as needed
                current_word += " " + text
                x_end = max(x_end, x + w)
                y_end = max(y_end, y + h)
            else:
                if current_word:
                    combined_words.append(
                        Sentence(
                            current_word,
                            x_start,
                            y_start,
                            x_end - x_start,
                            y_end - y_start,
                            (x_start + x_end) / 2,
                            (y_start + y_end) / 2,
                        )
                    )
                current_word = text
                x_start, x_end = x, x + w
                y_start, y_end = y, y + h

    # Append the last word
    if current_word:
        combined_words.append(
            Sentence(
                current_word,
                x_start,
                y_start,
                x_end - x_start,
                y_end - y_start,
                (x_start + x_end) / 2,
                (y_start + y_end) / 2,
            )
        )

    return combined_words


# Functions
########################################################

# Initialize a variable to store the last selected coordinate
last_selected_coord: Sentence = Sentence("", 0, 0, 0, 0, 0.0, 0.0)


def get_random_coord(coords: List[Sentence]) -> Sentence:
    global last_selected_coord
    available_coords = [coord for coord in coords if coord != last_selected_coord]
    selected_coord = random.choice(available_coords)
    last_selected_coord = selected_coord
    return selected_coord


def auto_dock_to_station(x: int, y: int) -> None:
    current_os = platform.system()

    if current_os == "Darwin":  # macOS
        pyautogui.rightClick(x, y)
        sleep_and_log(0.5)
        sentences = collect_sentences(pyautogui.screenshot())
        dock_button = get_dock_button_from_within_range(sentences)
        if dock_button:
            pyautogui.moveTo(dock_button.c_x, dock_button.c_y)
            pyautogui.click(dock_button.c_x, dock_button.c_y)
            sleep_and_log(0.5)
        else:
            logger.error("No dock button found! Panic!")
            raise Exception("No dock button found! Panic!")
    else:
        click_top_left_circle_menu(x, y)
        sleep_and_log(1)
        click_top_center_circle_menu(x, y)
        sleep_and_log(0.5)
    translate_key_combo("Ctrl-S")


def get_dock_button_from_within_range(sentences: List[Sentence]) -> Sentence | None:
    return next((item for item in sentences if item.word == "Dock"), None)


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
        pyautogui.click(button="left")

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
