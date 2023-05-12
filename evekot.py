import keyboard, time, os
import functions_evekot as fe

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

def mining_script_pc():

    fe.undock(585, 850)
    fe.set_hardener_online()
    fe.warp_to_mining_pos(1071, 175)
    fe.drone_out(477, 856)
    fe.mining_behaviour(1053, 1069, 1052, 1092, 250, 260, 250, 260, 475, 747)
    fe.drone_in()
    fe.back_to_station(1088, 156)
    fe.docking(1051, 1069)
    fe.clear_cargo(1229, 896)

def mining_script_laptop():

    fe.undock(750, 391)
    fe.set_hardener_online()
    fe.warp_to_mining_pos(190, 323)
    fe.drone_out(1300, 630)
    fe.mining_behaviour(1678, 837, 1679, 865, 250, 260, 2500, 2600, 1257, 723)
    fe.drone_in()
    fe.back_to_station(200, 298)
    fe.docking(1678, 837)
    fe.clear_cargo(1894, 643)

owl_signature()

print("press 'space' to continue or 'q' to quit...")

while True:
    key = keyboard.read_key()

    if key == "space":
        looptime = int(input("set looptime in minutes: "))
        looptime_sec = looptime * 60
        starttime = time.time()
        elapsed_time = 0
        
        time.sleep(10)

        while elapsed_time < looptime_sec:
            #mining_script_laptop()
            mining_script_pc()
            elapsed_time = time.time() - starttime

        print("Loop time elapsed.")
        os.system('shutdown /s  /t 1')
        break
    
    elif key == "q":
        print("Quitting...")
        break

    else:
        print("Wrong key, please try again!")
        continue


        

    