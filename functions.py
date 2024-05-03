import keyboard, time, datetime, random
import pyautogui

########################################################

def undock(x, y):

    random_time = random.uniform(1,2)
    log("undocking...")
    # undock
    pyautogui.moveTo(x,y, duration=random_time)
    pyautogui.mouseDown(button='left')
    sleep_and_log(random_time)
    pyautogui.mouseUp(button='left')
    sleep_small()

def set_hardener_online(key_combo):

    log("starting hardener...")
    # set hardener online
    translate_key_combo(key_combo)

def warp_to_pos_dropdown(x, y,rm_x, rm_y):

    random_time = random.uniform(2,3)
    log("warping to position...")
    # warping to belt
    sleep_and_log(10)
    pyautogui.moveTo(x,y, 2)
    pyautogui.click(button='right')
    sleep_and_log(random_time)
    pyautogui.moveRel(rm_x, rm_y)
    sleep_and_log(random_time)
    pyautogui.click(button='left')
    sleep_long()

def click_circle_menu(x, y, x_offset, y_offset):
    random_time = random.uniform(6, 7)
    log("clicking on the circle menu...")
    for _ in range(1):
        sleep_and_log(random_time)
        pyautogui.moveTo(x, y)
        pyautogui.mouseDown()
        sleep_and_log(random_time)
        pyautogui.moveRel(x_offset, y_offset, 1)
        pyautogui.mouseUp()
    sleep_long()

def click_warp_circle_menu(x, y):
    x_offset = -50
    y_offset = random.randint(-51, -49)
    click_circle_menu(x, y, x_offset, y_offset)

def click_dock_circle_menu(x, y):
    x_offset = 0
    y_offset = random.randint(-51, -49)
    click_circle_menu(x, y, x_offset, y_offset)
    # sleep longer when clicking the docking button in the circle menu
    sleep_long()

def drone_out(x,y):

    random_time = random.uniform(1,2)
    log("launching drones...")
    # drone out, random click in space
    pyautogui.click(x, y, button='left', duration=random_time)
    # drone out
    sleep_and_log(5)
    pyautogui.keyDown('shift')
    pyautogui.press('f')
    sleep_and_log(1)
    # Umschalt loslassen
    pyautogui.keyUp('shift')

def drone_in():

    log("drones returning to bay...")
    # drone in
    pyautogui.keyDown('shift')
    pyautogui.press('r')
    sleep_and_log(1)
    pyautogui.keyUp('shift')
    # drone time back to ship
    sleep_small()

def clear_cargo(x, y):

    random_time = random.uniform(3, 4)
    log("clearing cargo...")
    # clear cargo
    pyautogui.click(x + 175, y + 165, button='left', duration=random_time)
    pyautogui.mouseDown(button='left')
    pyautogui.dragRel(-175, -165, duration=random_time)
    pyautogui.mouseUp(button='left')
    pyautogui.mouseDown(button='left')
    pyautogui.dragRel(0, -250, duration=random_time)
    pyautogui.mouseUp(button='left')
    sleep_and_log(random_time)

# Mining Script
########################################################

def mining_behaviour(tx1, ty1, tx2, ty2, mr_start, mr_end, ml_start, ml_end, rm_x, rm_y, unlock_all_targets_keys):

    random_time = random.uniform(3, 4)
    
    # start time to counter looptime
    start_time = time.time()

    #  periodically reset interval while mining - mr_start = 250, mr_end = 260
    mining_reset = random.uniform(mr_start, mr_end)

    #  periodically break while loop - ml_start = 2500, ml_end = 2600
    mining_loop = random.uniform(ml_start, ml_end)

    mining_sessions = 0
    
    while True:
        mining_sessions += 1

        if len(unlock_all_targets_keys) >= 1:
            # reset mouse assigned mining laser random in space
            pyautogui.moveTo(rm_x, rm_y)
            pyautogui.click(button='right')
            log(f"Using unlock all targets key: {unlock_all_targets_keys}")
            [pyautogui.keyDown(key) for key in unlock_all_targets_keys.split('-')]
            time.sleep(0.5)
            [pyautogui.keyUp(key) for key in unlock_all_targets_keys.split('-')]
            sleep_and_log(3)
        else:
            log("Manually unlocking targets 1 and 2")
            # reset target 1
            pyautogui.moveTo(tx1, ty1)
            pyautogui.keyDown('ctrl')
            pyautogui.keyDown('shift')
            pyautogui.click(button='left')
            pyautogui.keyUp('ctrl')
            pyautogui.keyUp('shift')

            sleep_and_log(3)

            # reset target 2
            pyautogui.moveTo(tx2, ty2)
            pyautogui.keyDown('ctrl')
            pyautogui.keyDown('shift')
            pyautogui.click(button='left')
            pyautogui.keyUp('ctrl')
            pyautogui.keyUp('shift')

        # reset mininglaser 1
        pyautogui.keyDown('f1')
        sleep_and_log(random_time)
        pyautogui.keyUp('f1')

        sleep_and_log(3)

        # reset mininglaser 2
        pyautogui.keyDown('f2')
        sleep_and_log(random_time)
        pyautogui.keyUp('f2')

        # reset mouse assigned mining laser random in space
        pyautogui.moveTo(rm_x, rm_y)
        pyautogui.click(button='right')

        sleep_and_log(2)

        # console
        log("mining...")

        # target 1
        pyautogui.moveTo(tx1, ty1)
        pyautogui.keyDown('ctrl')
        pyautogui.click(button='left')
        pyautogui.keyUp('ctrl')
        sleep_and_log(3)
        pyautogui.press('f1')

        sleep_and_log(5)

        # target 2
        pyautogui.moveTo(tx2,ty2)
        pyautogui.keyDown('ctrl')
        pyautogui.click(button='left')
        pyautogui.keyUp('ctrl')
        sleep_and_log(3)
        # second left click to focus the second target
        pyautogui.click(button='left')
        pyautogui.press('f2')

        # reset every 170 seconds (depends on mining barge)
        set_next_reset(mining_reset, NEXT_RESET_IN)
        sleep_and_log(mining_reset)
        log("reset mining script...")

        elapsed_time = time.time() - start_time
        if elapsed_time >= mining_loop:
            log("Done mining, ran {mining_sessions} mining sessions")
            break
            

# Constants for timers 
TIME_LEFT = "Time left"
NEXT_RESET_IN = "Next reset in"
CARGO_LOAD_TIME = "Cargo loaded in"

# Dictionary to store next reset time for each counter
timers = {
    TIME_LEFT: 0,
    NEXT_RESET_IN: 0,
    CARGO_LOAD_TIME: 0
}

# Function to update the countdown timer
def update_timer(label, counter):
    # Calculate remaining time until the next reset
    remaining_time = max(0, timers[counter] - time.time())

    # Calculate days, hours, minutes, and seconds
    days = int(remaining_time // (60 * 60 * 24))
    remaining_time %= (60 * 60 * 24)
    hours = int(remaining_time // (60 * 60))
    remaining_time %= (60 * 60)
    minutes = int(remaining_time // 60)
    seconds = int(remaining_time % 60)

    # Format the remaining time
    remaining_str = ""
    if days > 0:
        remaining_str += f"{days}d "
    if hours > 0:
        remaining_str += f"{hours}h "
    remaining_str += f"{minutes:02d}m {seconds:02d}s"

    # Update the label text with the remaining time
    label.config(text=f"{counter}: {remaining_str}")

    # Schedule the update function to run again after 1 second
    label.after(1000, update_timer, label, counter)

def translate_key_combo(key_combo):
    if len(key_combo) >= 1:
        keys = key_combo.split('-')
        with pyautogui.hold(keys[0].lower()):
            if len(keys) > 1:
                pyautogui.press(keys[1].lower())

# Function to set the next reset time for a specific counter
def set_next_reset(time_interval, counter):
    timers[counter] = time.time() + time_interval

def sleep_and_log(seconds):
    log(f"sleeping {seconds} seconds")
    time.sleep(seconds)

def log(msg):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] - {msg}")

def sleep_long():
    sleep_and_log(random.uniform(70, 75))

def sleep_small():
    sleep_and_log(random.uniform(12, 15))