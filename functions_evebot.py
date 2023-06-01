import keyboard, time, datetime, random, win32api, win32gui
import pyautogui

# random time intervall for whole mining functions
random_time = random.uniform(3, 4)
random_sleep_small = random.uniform(12, 15)
random_sleep_medium = random.uniform(65, 70)



########################################################

def undock(x, y):

    random_time = random.uniform(1,2)
    random_sleep_small = random.uniform(12,15)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # console
    print("")
    print(f"[{timestamp}] - undocking...")
    # undock
    pyautogui.moveTo(x,y, duration=random_time)
    pyautogui.mouseDown(button='left')
    time.sleep(random_time)
    pyautogui.mouseUp(button='left')
    time.sleep(random_sleep_small)

def set_hardener_online():

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # console
    print(f"[{timestamp}] - starting hardener...")
    # set hardener online
    pyautogui.press('f3')
    pyautogui.press('f4')

def warp_to_pos_dropdown(x, y,rm_x, rm_y):

    random_time = random.uniform(2,3)
    random_sleep_medium = random.uniform(70, 75)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # console
    print(f"[{timestamp}] - warping to position...")
    # warping to belt
    time.sleep(10)
    pyautogui.moveTo(x,y, 2)
    pyautogui.click(button='right')
    time.sleep(random_time)
    pyautogui.moveRel(rm_x, rm_y)
    time.sleep(random_time)
    pyautogui.click(button='left')
    time.sleep(random_sleep_medium)

def warp_to_pos_circle_menu(x, y):

    random_time = random.uniform(6,7)
    random_sleep_medium = random.uniform(70, 75)
    y_offset = random.randint(-51,-49)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # console
    print(f"[{timestamp}] - warping to mining position...")
    # warp to belt
    for i in range(1):
        time.sleep(random_time)
        pyautogui.moveTo(x, y)
        pyautogui.mouseDown()
        time.sleep(random_time)
        pyautogui.moveRel(-50, y_offset, 1)
        pyautogui.mouseUp()
    
    time.sleep(random_sleep_medium)

def drone_out(x,y):

    random_time = random.uniform(1,2)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # console
    print(f"[{timestamp}] - launching drones...")
    # drone out, random click in space
    pyautogui.click(x, y, button='left', duration=random_time)
    pyautogui.press('9')
    time.sleep(1)
    # drone out
    time.sleep(5)
    pyautogui.press('9')

def drone_in():

    random_sleep_small = random.uniform(12, 15)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # console
    print(f"[{timestamp}] - drones returning to bay...")
    # drone in
    pyautogui.press('0')
    # drone time back to ship
    time.sleep(random_sleep_small)

def docking_dropdown(x, y, rel_x, rel_y):

    random_time = random.uniform(2,3)
    random_sleep_medium = random.uniform(15, 20)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # console
    print(f"[{timestamp}] - docking...")
    # docking
    time.sleep(2)
    pyautogui.moveTo(x,y, 2)
    pyautogui.click(button='right')
    time.sleep(random_time)
    pyautogui.moveRel(rel_x, rel_y)
    time.sleep(random_time)
    pyautogui.click(button='left')
    time.sleep(random_sleep_medium)

def docking_circle_menu(x, y):

    random_time = random.uniform(6,7)
    random_sleep_medium = random.uniform(65, 70)
    y_offset = random.randint(-81, -79)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # console
    print(f"[{timestamp}] - docking...")
    # docking
    for i in range(1):
        time.sleep(random_time)
        pyautogui.moveTo(x, y)
        pyautogui.mouseDown()
        time.sleep(random_time)
        pyautogui.moveRel(0, y_offset, 1)
        pyautogui.mouseUp()

    time.sleep(random_sleep_medium)



def clear_cargo(x, y):

    random_time = random.uniform(3, 4)
    random_sleep_small = random.uniform(12, 15)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # console
    print(f"[{timestamp}] - clearing cargo...")
    # clear cargo
    pyautogui.click(x, y, button='left', duration=random_time)
    pyautogui.mouseDown(button='left')
    pyautogui.dragRel(-175, -165, duration=random_time)
    pyautogui.mouseUp(button='left')
    pyautogui.mouseDown(button='left')
    pyautogui.dragRel(0, -250, duration=random_time)
    pyautogui.mouseUp(button='left')
    time.sleep(random_sleep_small)

# Mining Script
########################################################

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

        # console
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] - mining...")

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
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] - reset mining script...")

        elapsed_time = time.time() - start_time
        if elapsed_time >= mining_loop:
            break

# Draw Function
########################################################

def draw_point(x, y, r,g,b):

    # Color
    red = win32api.RGB(r, g, b)
        
    # Get Desktop-Window
    desktop_window = win32gui.GetDesktopWindow()

    # Set Device Context for Desktop-Window
    desktop_dc = win32gui.GetWindowDC(desktop_window)

    # Set Pixel Color
    for i in range(x-3, x+3):
        for j in range(y-3, y+3):
            win32gui.SetPixel(desktop_dc, i, j, red)
        
    # Release Devicecontext
    win32gui.ReleaseDC(desktop_window, desktop_dc)

# Owl Signature
########################################################

def owl_signature():

    owl = ["                            ",
           "⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀",
           "⠀⠀⠀⠀⠀⠀⠐⣶⣾⣿⣿⣿⣿⣿⣶⡆⠀⠀⠀⠀⠀⠀",
           "⠀⠀⠀⠀⠀⠀⢰⡏⢤⡎⣿⣿⢡⣶⢹⣧⠀⠀⠀⠀⠀⠀",
           "⠀⠀⠀⠀⠀⠀⢸⣿⣶⣶⣇⣸⣷⣶⣾⣿⠀⠀⠀⠀⠀⠀",
           "⠀⠀⠀⠀⠀⠀⢨⣿⣿⣿⢟⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀",
           "⠀⠀⠀⠀⠀⠀⢸⣿⣿⡏⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀",
           "⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣜⠿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀",
           "⠀⠀⠀⠀⠀⠀⠀⠐⣷⣿⡿⣷⣮⣙⠿⣿⣿⣿⣿⣿⡄⠀",
           "        ⠀⠫⡯⢿⣿⣿⣿⣶⣯⣿⣻⣿⣿⠀ ",
           "           ⠙⢻⣿⣿⠿⠿⠿⢻⣿⠙⠇ ",
           "           ⣠⡶⠿⣟⠀⠀⠀⠀ ⠻⡀   ",
           "         ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ ",
           "         ⣿⣿⣿   OWL  ⣿⣿⣿   ",
           "         ⣿⣿⣿ MINING ⣿⣿⣿  ",
           "         ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿  ",
           "                                "]
    delay = 0.5
    acceleration = 0.025

    for i in range(len(owl)):
        print(owl[i])
        time.sleep(delay)
        delay -= acceleration

# Explanation
########################################################

def explanation():

    print(" ")
    print(" Check Interaction Coordinates!")
    print("#################################")
    print("# Orange = Mining Positions     #")
    print("# Yellow = Undock Position      #")
    print("# White = Drone Reset Position  #")
    print("# Blue = Warping to Station     #")
    print("# Green = Docking               #")
    print("# Pink = Clear Cargo            #")
    print("# Red = Targeting Positions     #")
    print("# Violett = Mining Mouse Reset  #")
    print("#################################")
    print("")
    print("Press escape to continue..")

#######################################################

def check_abort(xw,yw, relxw,relyw, xd, yd, relxd, relyd):
    
    if keyboard.is_pressed('q'):
        drone_in()
        warp_to_pos_dropdown(xw, yw, relxw, relyw)
        docking_dropdown(xd, yd, relxd, relyd)



#######################################################