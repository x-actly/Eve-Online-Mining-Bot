import keyboard, time, datetime, random
import pyautogui



def targeting(x, y):

    # reset target 
    pyautogui.moveTo(x, y)
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('shift')
    pyautogui.click(button='left')
    time.sleep(1)
    pyautogui.click(button='left')
    pyautogui.keyUp('ctrl')
    pyautogui.keyUp('shift')
    time.sleep(1)
    # targeting
    pyautogui.moveTo(x, y)
    pyautogui.keyDown('ctrl')
    pyautogui.click(button='left')
    time.sleep(1)
    pyautogui.click(button='left')
    pyautogui.keyUp('ctrl')
    time.sleep(10)
    pyautogui.press('f1')
    time.sleep(1)
    pyautogui.press('f')


def emergency_warp(x, y):

    random_time = random.uniform(1,2)
    y_offset_align = random.randint(77, 79)
    y_offset_warp = random.randint(-51,-49)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    
    for i in range(1):


        ######### drones in #########
        #time.sleep(1)
        pyautogui.keyDown('shift')
        pyautogui.press('r')
        time.sleep(1)
        pyautogui.keyUp('shift')
        ######### align #############
        # time.sleep(random_time)
        # pyautogui.press('f3')
        # pyautogui.moveTo(x, y)
        # pyautogui.mouseDown()
        # time.sleep(random_time)
        # pyautogui.moveRel(-45, y_offset_align, 1)
        # pyautogui.mouseUp()
        # time.sleep(5)
        ######### warp ##############
        pyautogui.press('f3') 
        time.sleep(random_time)
        pyautogui.moveTo(x, y)
        pyautogui.mouseDown()
        time.sleep(random_time)
        pyautogui.moveRel(-50, y_offset_warp, 1)
        pyautogui.mouseUp()
    