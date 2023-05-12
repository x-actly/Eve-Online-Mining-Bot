import pyautogui
import random
import time


# random time intervall for whole mining functions
random_time = random.uniform(3, 4)
random_sleep_small = random.uniform(12, 15)
random_sleep_medium = random.uniform(65, 70)



########################################################

def undock(x, y):

    random_time = random.uniform(1,2)
    random_sleep_small = random.uniform(12,15)
    #button_pos = [888, 596]

    # console
    print("undocking...")
    # undock
    pyautogui.moveTo(x,y, duration=random_time)
    pyautogui.mouseDown(button='left')
    time.sleep(random_time)
    pyautogui.mouseUp(button='left')
    time.sleep(random_sleep_small)

def set_hardener_online():

    # console
    print("starting hardener...")
    # set hardener online
    pyautogui.press('f3')
    pyautogui.press('f4')

def warp_to_mining_pos(x, y):

    random_time = random.uniform(6,7)
    random_sleep_medium = random.uniform(65, 70)
    #mining_pos = [1739, 230]

    # console
    print("warping to mining position...")
    # warp to belt
    time.sleep(random_time)
    pyautogui.moveTo(x, y)
    pyautogui.mouseDown()
    time.sleep(random_time)
    pyautogui.moveRel(-50,-50)
    pyautogui.mouseUp()
    time.sleep(random_sleep_medium)

def drone_out(x,y):

    random_time = random.uniform(1,2)

    # console
    print("launching drones...")
    # drone out, random click in space
    pyautogui.click(x, y, button='left', duration=random_time)
    pyautogui.press('9')
    time.sleep(1)
    # drone out
    time.sleep(5)
    pyautogui.press('9')

def mining_behaviour(tx1, ty1, tx2, ty2, mr_start, mr_end, ml_start, ml_end, rm_x, rm_y):

    random_time = random.uniform(3, 4)
    # start time to counter looptime
    start_time = time.time()

    #  periodically reset interval while mining - mr_start = 250, mr_end = 260
    mining_reset = random.uniform(mr_start, mr_end)

    #  periodically break while loop - ml_start = 2500, ml_end = 2600
    mining_loop = random.uniform(ml_start, ml_end)

    # target 1 positions - x = tx1, y = ty1
    # target 2 positions - x = tx2, y = ty2
    # reset mouse - x = rm_x, y = rm_y

    # console
    print("mining...")

    while True:

        # reset target 1
        pyautogui.moveTo(tx1, ty1)
        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('shift')
        pyautogui.click(button='left')
        pyautogui.keyUp('ctrl')
        pyautogui.keyUp('shift')

        time.sleep(3)

        # reset target 2
        pyautogui.moveTo(tx2, ty2)
        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('shift')
        pyautogui.click(button='left')
        pyautogui.keyUp('ctrl')
        pyautogui.keyUp('shift')

        # reset mininglaser 1
        pyautogui.keyDown('f1')
        time.sleep(random_time)
        pyautogui.keyUp('f1')

        time.sleep(3)

        # reset mininglaser 2
        pyautogui.keyDown('f2')
        time.sleep(random_time)
        pyautogui.keyUp('f2')

        # reset mouse assigned mining laser random in space
        pyautogui.moveTo(rm_x, rm_y)
        pyautogui.click(button='right')

        time.sleep(2)

        # target 1
        pyautogui.moveTo(tx1, ty1)
        pyautogui.keyDown('ctrl')
        pyautogui.click(button='left')
        pyautogui.keyUp('ctrl')
        time.sleep(3)
        pyautogui.press('f1')

        time.sleep(5)

        # target 2
        pyautogui.moveTo(tx2,ty2)
        pyautogui.keyDown('ctrl')
        pyautogui.click(button='left')
        pyautogui.keyUp('ctrl')
        time.sleep(3)
        # second left click to focus the second target
        pyautogui.click(button='left')
        pyautogui.press('f2')

        # reset every 170 seconds (depends on mining barge)
        time.sleep(mining_reset)

        elapsed_time = time.time() - start_time
        if elapsed_time >= mining_loop:
            break

def drone_in():

    random_sleep_small = random.uniform(12, 15)
    
    # console
    print("drones returning to bay...")
    # drone in
    pyautogui.press('0')
    # drone time back to ship
    time.sleep(random_sleep_small)

def back_to_station(x, y):

    random_time = random.uniform(1,2)
    random_sleep_medium = random.uniform(70, 75)
    #station_pos = [1730, 180]

    # console
    print("warping to station...")
    # back to station
    pyautogui.moveTo(x, y)
    pyautogui.mouseDown()
    time.sleep(random_time)
    pyautogui.moveRel(-50,-50)
    pyautogui.mouseUp()
    time.sleep(random_sleep_medium)

def docking(x, y):

    random_time = random.uniform(6,7)
    random_sleep_medium = random.uniform(65, 70)
    #station_pos = [1600, 651]
    
    # console
    print("docking...")
    # docking
    pyautogui.moveTo(x, y)
    pyautogui.mouseDown()
    time.sleep(random_time)
    pyautogui.moveRel(0,-80)
    pyautogui.mouseUp()
    time.sleep(random_sleep_medium)

def clear_cargo(x, y):

    random_time = random.uniform(3, 4)
    random_sleep_small = random.uniform(12, 15)

    # console
    print("clearing cargo...")
    # clear cargo
    pyautogui.click(x, y, button='left', duration=random_time)
    pyautogui.mouseDown(button='left')
    pyautogui.dragRel(-175, -165, duration=random_time)
    pyautogui.mouseUp(button='left')
    pyautogui.mouseDown(button='left')
    pyautogui.dragRel(0, -250, duration=random_time)
    pyautogui.mouseUp(button='left')
    time.sleep(random_sleep_small)

########################################################

# old - first version - backup
def fleet_mining_example():

    # abdocken
    pyautogui.click(x=950, y=600, button='left', duration=random_time)
    time.sleep(random_sleep_small)

    # set hardener online
    pyautogui.press('f3')
    pyautogui.press('f4')

    # Fleet Position anwarpen
    pyautogui.click(x=959, y=351, button='right', duration=random_time)
    pyautogui.click(x=1066, y=377, button='left', duration=random_time)
    time.sleep(random_sleep_medium)

    # asteroid 1 auswählen
    pyautogui.click(x=1635, y=648, button='right', duration=random_time)
    pyautogui.click(x=1718, y=775, button='left', duration=random_time)

    # asteroid 2 auswählen
    pyautogui.click(x=1636, y=680, button='right', duration=random_time)
    pyautogui.click(x=1722, y=773, button='left', duration=random_time)
    time.sleep(random_sleep_small)

    # drone out
    time.sleep(3)
    pyautogui.press('9')
    time.sleep(3)

    # Ziel 1 auswählen, aktivieren
    pyautogui.click(x=600, y=100, button='left', duration=random_time)
    pyautogui.keyDown('f1')
    time.sleep(random_time)
    pyautogui.keyUp('f1')

    # Ziel 2 auswählen, aktivieren
    pyautogui.click(x=730, y=100, button='left', duration=random_time)
    pyautogui.keyDown('f2')
    time.sleep(random_time)
    pyautogui.keyUp('f2')

    # belt time in sec.
    time.sleep(1500)

    # drone in
    pyautogui.press('0')

    # drone time back to ship
    time.sleep(random_sleep_small)

    # back to station
    pyautogui.click(x=1636, y=175, button='right', duration=random_time)
    pyautogui.click(x=1706, y=197, button='left', duration=random_time)
    time.sleep(random_sleep_medium)

    # docking
    pyautogui.click(x=1600, y=651, button='right', duration=random_time)
    pyautogui.click(x=1667, y=575, button='left', duration=random_time)
    time.sleep(random_sleep_small)

    # clear cargo
    pyautogui.click(x=1490, y=970, button='left', duration=random_time)
    pyautogui.mouseDown(button='left')
    pyautogui.dragTo(1147, 836, duration=2.0)
    pyautogui.mouseUp(button='left')
    pyautogui.mouseDown(button='left')
    pyautogui.dragTo(1179, 560, duration=2.0)
    pyautogui.mouseUp(button='left')
    time.sleep(random_sleep_small)

# current - example for mining sequence - backup
def solo_mining_example():
    
    undock(774, 846)
    set_hardener_online()
    warp_to_mining_pos(1042, 179)
    drone_out(475, 1059)
    mining_behaviour(979, 1068, 979, 1093, 250, 260, 2500, 2600, 872, 987)
    drone_in()
    back_to_station(1045,156)
    docking(1050, 156)
    clear_cargo(1239, 892)
# current - 1080p Laptop - backup
def mining_script_laptop():

    undock(750, 391)
    set_hardener_online()
    warp_to_mining_pos(190, 277)
    drone_out(1300, 630)
    mining_behaviour(1678, 837, 1679, 865, 250, 260, 2500, 2600, 1257, 723)
    drone_in()
    back_to_station(258, 251)
    docking(1678, 837)
    clear_cargo(1894, 643)
# current - 1440p half screen - backup
def mining_script_pc():

    undock(756, 843)
    set_hardener_online()
    warp_to_mining_pos(1071, 175)
    drone_out(477, 856)
    mining_behaviour(1053, 1069, 1052, 1092, 250, 260, 2400, 2500, 475, 747)
    drone_in()
    back_to_station(1088, 156)
    docking(1051, 1069)
    clear_cargo(1229, 896)

########################################################