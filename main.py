import pyautogui, sys, random, time, pygame, time, threading
from datetime import datetime
from functions import emergency_warp
from functions import targeting
import tkinter as tk

alarm_played = False

additional_thread_running = True

# Detection Area
start_x, start_y = 57, 75
end_x, end_y = 257, 941

# safespot
safe_x, safe_y = 1113, 232  
safe_window_size = 6  

# targeting spot
targeting_x, targeting_y = 1074, 689
targeting_window_size = 6  


def close_windows(event=None):
    root.destroy()
    safe_root.destroy()
    targeting_root.destroy()


root = tk.Tk()
root.overrideredirect(True)  
root.attributes("-alpha", 0.1) 


window_width = end_x - start_x
window_height = end_y - start_y
root.geometry(f"{window_width}x{window_height}+{start_x}+{start_y}")

canvas = tk.Canvas(root, width=window_width, height=window_height, highlightthickness=0)
canvas.pack()


def draw_rectangle(start_x, start_y, end_x, end_y):
    canvas.create_rectangle(0, 0, end_x - start_x, end_y - start_y, outline="red", width=3, fill="red")

draw_rectangle(start_x, start_y, end_x, end_y)


safe_root = tk.Tk()
safe_root.overrideredirect(True)  
safe_root.attributes("-alpha", 0.5)  


safe_root.geometry(f"{safe_window_size}x{safe_window_size}+{safe_x-safe_window_size//2}+{safe_y-safe_window_size//2}")


safe_canvas = tk.Canvas(safe_root, width=safe_window_size, height=safe_window_size, highlightthickness=0)
safe_canvas.pack()

def draw_safe_rectangle():
    safe_canvas.create_rectangle(0, 0, safe_window_size, safe_window_size, outline="red", width=3, fill="red")


draw_safe_rectangle()


targeting_root = tk.Tk()
targeting_root.overrideredirect(True) 
targeting_root.attributes("-alpha", 0.5)  


targeting_root.geometry(f"{targeting_window_size}x{targeting_window_size}+{targeting_x-targeting_window_size//2}+{targeting_y-targeting_window_size//2}")


targeting_canvas = tk.Canvas(targeting_root, width=targeting_window_size, height=targeting_window_size, highlightthickness=0)
targeting_canvas.pack()


def draw_targeting_rectangle():
    targeting_canvas.create_rectangle(0, 0, targeting_window_size, targeting_window_size, outline="red", width=3, fill="red")


draw_targeting_rectangle()


root.bind("<Key>", close_windows)
safe_root.bind("<Key>", close_windows)
targeting_root.bind("<Key>", close_windows)

root.mainloop()


image_paths = ['img/neut_4k.png', 'img/red_4k.png', 'img/-5_1440p.png', 'img/-10_1440p.png', 
               'img/neut_1080p.png', 'img/red_1080p.png', 'img/-5_1080p.png', 'img/-5_1440p.png', 
               'img/-10_1080p.png', 'img/-10_1440p.png', 'img/neut_1080p_red.png']  
#image_paths = ['img/neut_1080p.png', 'img/red_1080p.png', 'img/-5.png', 'img/-10.png']


confidence_level = 0.85 

def find_and_execute(image_paths, action_function, start_x, start_y, end_x, end_y, confidence):
    search_region = (start_x, start_y, end_x - start_x, end_y - start_y)
    for image_path in image_paths:
        try:
            position = pyautogui.locateOnScreen(image_path, region=search_region, confidence=confidence)
            if position is not None:
                action_function()
                return True
        except pyautogui.ImageNotFoundException:
            print(f"DEBUG - {image_path} - not found.")
    return False


def additional_thread_function():
    random_interval = random.uniform(50, 60)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    global additional_thread_running
    while additional_thread_running:
        
        time.sleep(random_interval)
        print(f"DEBUG - {current_time} - targeting")
        targeting(targeting_x, targeting_y)



additional_thread = threading.Thread(target=additional_thread_function)
additional_thread.daemon = True 
additional_thread.start()

def perform_action():
    global alarm_played
    if not alarm_played:
        pygame.mixer.init()
        pygame.mixer.music.load('sound/alarm.mp3')
        pygame.mixer.music.play()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{current_time} - emergency warp")
        while pygame.mixer.music.get_busy():
            continue
        alarm_played = True
        emergency_warp(safe_x, safe_y)

    sys.exit()

while True:
    try:
        random_interval = random.uniform(1, 2)
        found = find_and_execute(image_paths, perform_action, start_x, start_y, end_x, end_y, confidence_level)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
        print("")
        print(f"DEBUG - {current_time} - local clear")
        print("")
        time.sleep(random_interval)
        if found:
            additional_thread_running = False
            break
    except KeyboardInterrupt:
        print("Keyboard interruption detected. Exiting the program.")
        pyautogui.moveTo(targeting_x, targeting_y)
        time.sleep(1)
        pyautogui.click(button="left")
        time.sleep(1)
        pyautogui.click(button="left")
        pyautogui.keyDown('shift')
        pyautogui.press('r')
        time.sleep(1)
        pyautogui.keyUp('shift')
        additional_thread_running = False
        break