import time, os, random, win32api, win32con
import functions_evebot as fe




# Variables # Bookmark Positions
mining_coo = [(150, 202),(150, 227),(150,255),(150,281),(150,308),(150, 334),(150,359),(150,385),(150,411),(150,437),(150,465)]
undock_coo = [(751, 395)]
drone_mouse_reset_coo = [(490, 382)]
warp_to_coo = [(194, 180)]
docking_coo = [(461, 570)]
clear_cargo_coo = [(1883, 630)]
target_one_coo = [(455, 570)]
target_two_coo = [(455, 600)]
mining_mouse_reset_coo = [(479, 382)]
mining_target_reset = [(250, 260)] 
mining_loop_reset = [(1200, 1300)]

# Signature
fe.owl_signature()

# Explanation
fe.explanation()

# loop to draw points until escape
running = True
while running:

    for point in mining_coo:
        fe.draw_point(*point, 255, 165, 0) # Belt Positions  = Orange
    for point in undock_coo:
        fe.draw_point(*point, 255, 255, 0) # Undock Position = Yellow
    for point in drone_mouse_reset_coo:
        fe.draw_point(*point, 240,255,255) # Drone Reset = White
    for point in warp_to_coo:
        fe.draw_point(*point, 0,0,255) # Warping to Pos "Station" = Blue
    for point in docking_coo:
        fe.draw_point(*point, 0,255,0) # Docking = Green
    for point in clear_cargo_coo:
        fe.draw_point(*point, 255,20,147) # Clear Cargo = Pink
    for point in target_one_coo:
        fe.draw_point(*point, 255,0,0) # Target One = Red
    for point in target_two_coo:
        fe.draw_point(*point, 255,0,0) # Target Two = Red
    for point in mining_mouse_reset_coo:
        fe.draw_point(*point, 191,62,255) # Mining Mouse Reset = Violett
                                    

    # waiting periods in seconds
    time.sleep(0.1)

    # end the the script with 
    if win32api.GetAsyncKeyState(win32con.VK_ESCAPE):
        running = False

shutdown_choice = input("Do you want to shut down the system when the loop is completed? (yes/no)")

looptime = int(input("Set mining time in minutes: "))
looptime_sec = looptime * 60
starttime = time.time()
elapsed_time = 0

while elapsed_time < looptime_sec:

    time.sleep(5)

    fe.undock(undock_coo[0][0], undock_coo[0][1])
    fe.set_hardener_online()

    for item in mining_coo:
        item = random.choice(mining_coo)
        #fe.warp_to_pos_dropdown(item[0], item[1],50,20)
        fe.warp_to_pos_circle_menu(item[0], item[1])
        break

    fe.drone_out(drone_mouse_reset_coo[0][0], drone_mouse_reset_coo[0][1])
    fe.mining_behaviour(target_one_coo[0][0], target_one_coo[0][1], target_two_coo[0][0], target_two_coo[0][1], mining_target_reset[0][0], mining_target_reset[0][1], mining_loop_reset[0][0],mining_loop_reset[0][1], mining_mouse_reset_coo[0][0], mining_mouse_reset_coo[0][1])
    fe.drone_in()
    #fe.warp_to_pos_dropdown(warp_to_coo[0][0], warp_to_coo[0][1],50,20)
    fe.warp_to_pos_circle_menu(warp_to_coo[0][0], warp_to_coo[0][1])
    #fe.docking_dropdown(docking_coo[0][0], docking_coo[0][1], 50, 105)
    fe.docking_dropdown(docking_coo[0][0], docking_coo[0][1])
    fe.clear_cargo(clear_cargo_coo[0][0], clear_cargo_coo[0][1])

    elapsed_time = time.time() - starttime


    if elapsed_time >= looptime_sec:
        if shutdown_choice.lower() == "yes" or shutdown_choice.lower() == " yes":
            os.system('shutdown /s /t 1')
        else: 
            print("loop time elapsed.")
            break



        

    