import tkinter as tk
import threading
import time
import ctypes
from ctypes import windll
import functions_evebot as fe
from PIL import ImageTk, Image



mining_target_reset = [(250, 260)]

# Undock Koordinaten
UNDOCK_COO_FILE = "config/undock_coo.txt"

def load_undock_coo():
    try:
        with open(UNDOCK_COO_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

def save_undock_coo():
    with open(UNDOCK_COO_FILE, "w") as file:
        file.write(undock_coo_entry.get())

# Drone Mouse Reset Koordinaten
DRONE_MOUSE_RESET_COO_FILE = "config/drone_mouse_reset_coo.txt"

def load_drone_mouse_reset_coo():
    try:
        with open(DRONE_MOUSE_RESET_COO_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

def save_drone_mouse_reset_coo():
    with open(DRONE_MOUSE_RESET_COO_FILE, "w") as file:
        file.write(drone_mouse_reset_coo_entry.get())

# Mining Loop Reset
MINING_LOOP_VALUE_FILE = "config/mining_loop_value.txt"

def load_mining_loop_value():
    try:
        with open(MINING_LOOP_VALUE_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

def save_mining_loop_value():
    with open(MINING_LOOP_VALUE_FILE, "w") as file:
        file.write(mining_loop_reset_entry.get())

# Warp to Koordinaten
WARP_TO_COO_FILE = "config/warp_too_coo.txt"

def load_warp_to_coo():
    try:
        with open(WARP_TO_COO_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

def save_warp_to_coo():
    with open(WARP_TO_COO_FILE, "w") as file:
        file.write(warp_to_coo_entry.get())

# Docking Koordinaten
DOCKING_FILE = "config/docking_coo.txt"

def load_docking_coo():
    try:
        with open(DOCKING_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

def save_docking_coo():
    with open(DOCKING_FILE, "w") as file:
        file.write(docking_coo_entry.get())

# Clear Cargo Koordinaten
CLEAR_CARGO_FILE = "config/clear_cargo_coo.txt"

def load_clear_cargo_coo():
    try:
        with open(CLEAR_CARGO_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

def save_clear_cargo_coo():
    with open(CLEAR_CARGO_FILE, "w") as file:
        file.write(clear_cargo_coo_entry.get())

# Target-One-Koordinaten
TARGET_ONE_COO_FILE = "config/target_one_coo.txt"

def load_target_one_coo():
    try:
        with open(TARGET_ONE_COO_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

def save_target_one_coo():
    with open(TARGET_ONE_COO_FILE, "w") as file:
        file.write(target_one_coo_entry.get())

# Target-One-Koordinaten
TARGET_TWO_COO_FILE = "config/target_two_coo.txt"

def load_target_two_coo():
    try:
        with open(TARGET_TWO_COO_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

def save_target_two_coo():
    with open(TARGET_TWO_COO_FILE, "w") as file:
        file.write(target_two_coo_entry.get())

# Target-Two-Koordinaten
TARGET_TWO_COO_FILE = "config/target_two_coo.txt"

def load_target_two_coo():
    try:
        with open(TARGET_TWO_COO_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

def save_target_two_coo():
    with open(TARGET_TWO_COO_FILE, "w") as file:
        file.write(target_two_coo_entry.get())

# Mining Mouse Reset
MINING_MOUSE_RESET_FILE = "config/mining_mouse_reset.txt"

def load_mining_mouse_reset_coo():
    try:
        with open(MINING_MOUSE_RESET_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

def save_mining_mouse_reset_coo():
    with open(MINING_MOUSE_RESET_FILE, "w") as file:
        file.write(mining_mouse_reset_coo_entry.get())

# Mining Koordinaten
MINING_COO_FILE = "config/mining_coo.txt"

def load_mining_coo():
    try:
        with open(MINING_COO_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""

def save_mining_coo():
    with open(MINING_COO_FILE, "w") as file:
        file.write(mining_coo_entry.get('1.0', 'end'))

def start_function():
    global stop_flag
    stop_flag = False
    minutes = int(entry.get())
    undock_coo_value = [int(x.strip()) for x in undock_coo_entry.get().split(",")]
    drone_mouse_reset_coo_value = [int(x.strip()) for x in drone_mouse_reset_coo_entry.get().split(",")]
    mining_coo_values = mining_coo_entry.get("1.0", tk.END).strip().split("\n")
    mining_coo_values = [(int(x.strip()), int(y.strip())) for x, y in (value.split(",") for value in mining_coo_values)]
    mining_loop_reset_value = int(mining_loop_reset_entry.get())
    warp_to_coo_values = [int(x.strip()) for x in warp_to_coo_entry.get().split(",")]
    docking_coo_values = [int(x.strip()) for x in docking_coo_entry.get().split(",")]
    clear_cargo_coo_values = [int(x.strip()) for x in clear_cargo_coo_entry.get().split(",")]
    target_one_coo_values = [int(x.strip()) for x in target_one_coo_entry.get().split(",")]
    target_two_coo_values = [int(x.strip()) for x in target_two_coo_entry.get().split(",")]
    mining_mouse_reset_coo_values = [int(x.strip()) for x in mining_mouse_reset_coo_entry.get().split(",")]
    thread = threading.Thread(target=repeat_function, args=(minutes, undock_coo_value, drone_mouse_reset_coo_value, mining_coo_values, mining_loop_reset_value, warp_to_coo_values, docking_coo_values, clear_cargo_coo_values, target_one_coo_values, target_two_coo_values, mining_mouse_reset_coo_values))
    thread.start()

def repeat_function(minutes, undock_coo_value, drone_mouse_reset_coo_value, mining_coo_values, mining_loop_reset_value, warp_to_coo_values, docking_coo_values, clear_cargo_coo_values, target_one_coo_values, target_two_coo_values, mining_mouse_reset_coo_values):
    print(f"Die Funktion wird für {minutes} Minute(n) gestartet!")
    end_time = time.time() + (minutes * 60)

    while not stop_flag and time.time() < end_time:
        time.sleep(5)

        fe.undock(undock_coo_value[0], undock_coo_value[1])
        fe.set_hardener_online()

        for item in mining_coo_values:
            fe.warp_to_pos_circle_menu(item[0], item[1])
            break

        fe.drone_out(drone_mouse_reset_coo_value[0], drone_mouse_reset_coo_value[1])
        fe.mining_behaviour(target_one_coo_values[0], target_one_coo_values[1], target_two_coo_values[0], target_two_coo_values[1], mining_target_reset[0][0], mining_target_reset[0][1], mining_loop_reset_value, mining_loop_reset_value, mining_mouse_reset_coo_values[0], mining_mouse_reset_coo_values[1])
        fe.drone_in()
        fe.warp_to_pos_circle_menu(warp_to_coo_values[0], warp_to_coo_values[1])
        fe.docking_circle_menu(docking_coo_values[0], docking_coo_values[1])
        fe.clear_cargo(clear_cargo_coo_values[0], clear_cargo_coo_values[1])


def stop_function():
    global stop_flag
    print("Die Funktion wird gestoppt!")
    stop_flag = True


def get_mouse_position():
    # Mausposition mit Hilfe der Windows-API abrufen
    user32 = windll.user32
    point = POINT()
    user32.GetCursorPos(ctypes.byref(point))
    return point.x, point.y


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long),
                ("y", ctypes.c_long)]


stop_flag = False

root = tk.Tk()
root.title("Mining Bot v0.2a Owl-Edition")
root.geometry("400x500")  # Setzen der Fenstergröße

# Fenster nicht in der Größe änderbar machen
root.resizable(False, False)

# Laden des Speicher-Symbols
save_icon = Image.open("config/icons/save_icon.png")  # Pfade und Dateinamen anpassen
save_icon = save_icon.resize((16, 16))  # Größe anpassen
save_icon = ImageTk.PhotoImage(save_icon)

# Erstellen Sie ein Frame für die Eingabe und die Buttons
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# Erstellen Sie ein Frame für die Start- und Stop-Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

#########################################################

# Erstellen Sie ein Eingabefeld für die Minuten
entry_label = tk.Label(input_frame, text="Minuten:")
entry_label.grid(row=0, column=0, sticky="w")
entry = tk.Entry(input_frame)
entry.grid(row=0, column=1, padx=5, pady=4, sticky="w")

##########################################################

# Funktion zum Speichern der Koordinaten
def save_button_clicked_mining_loop_reset():
    save_mining_loop_value()
    print("Koordinaten gespeichert!")

# Erstellen Sie ein Textfeld für die Mining-Loop-Reset-Werte
mining_loop_reset_label = tk.Label(input_frame, text="Mining Loop Reset:")
mining_loop_reset_label.grid(row=1, column=0, sticky="w")
mining_loop_reset_entry = tk.Entry(input_frame)
mining_loop_reset_entry.grid(row=1, column=1, padx=5, pady=4, sticky="w")

# Laden der gespeicherten Koordinaten beim Programmstart
mining_loop_reset_entry.insert(tk.END, load_mining_loop_value())

# Erstellen Sie einen Speichern-Button
save_button = tk.Button(input_frame, image=save_icon, compound="left", command=save_button_clicked_mining_loop_reset)
save_button.grid(row=1, column=2, padx=5, pady=4, sticky="w")

#########################################################

# Funktion zum Speichern der Koordinaten
def save_button_clicked_undock():
    save_undock_coo()
    print("Koordinaten gespeichert!")
    
# Erstellen Sie ein Eingabefeld für die Undock-Koordinaten
undock_coo_label = tk.Label(input_frame, text="Undock-Koordinaten:")
undock_coo_label.grid(row=2, column=0, sticky="w")
undock_coo_entry = tk.Entry(input_frame)
undock_coo_entry.grid(row=2, column=1, padx=5, pady=4, sticky="w")

# Laden der gespeicherten Koordinaten beim Programmstart
undock_coo_entry.insert(tk.END, load_undock_coo())

# Erstellen Sie einen Speichern-Button
save_button = tk.Button(input_frame, image=save_icon, compound="left", command=save_button_clicked_undock)
save_button.grid(row=2, column=2, padx=5, pady=4, sticky="w")

##########################################################

# Funktion zum Speichern der Koordinaten
def save_button_clicked_drone_reset():
    save_drone_mouse_reset_coo()
    print("Koordinaten gespeichert!")

# Erstellen Sie ein Eingabefeld für die Drone Mouse Reset-Koordinaten
drone_mouse_reset_coo_label = tk.Label(input_frame, text="Drone Mouse Reset-Koordinaten:")
drone_mouse_reset_coo_label.grid(row=3, column=0, sticky="w")
drone_mouse_reset_coo_entry = tk.Entry(input_frame)
drone_mouse_reset_coo_entry.grid(row=3, column=1, padx=5, pady=4, sticky="w")

# Laden der gespeicherten Koordinaten beim Programmstart
drone_mouse_reset_coo_entry.insert(tk.END, load_drone_mouse_reset_coo())

# Erstellen Sie einen Speichern-Button
save_button = tk.Button(input_frame, image=save_icon, compound="left", command=save_button_clicked_drone_reset)
save_button.grid(row=3, column=2, padx=5, pady=4, sticky="w")

##########################################################

# Funktion zum Speichern der Koordinaten
def save_button_clicked_warp_to_coo():
    save_warp_to_coo()
    print("Koordinaten gespeichert!")

# Erstellen Sie ein Eingabefeld für die Warp-to-Koordinaten
warp_to_coo_label = tk.Label(input_frame, text="Warp-to-Koordinaten:")
warp_to_coo_label.grid(row=4, column=0, sticky="w")
warp_to_coo_entry = tk.Entry(input_frame)
warp_to_coo_entry.grid(row=4, column=1, padx=5, pady=4, sticky="w")

# Laden der gespeicherten Koordinaten beim Programmstart
warp_to_coo_entry.insert(tk.END, load_warp_to_coo())

# Erstellen Sie einen Speichern-Button
save_button = tk.Button(input_frame, image=save_icon, compound="left", command=save_button_clicked_warp_to_coo)
save_button.grid(row=4, column=2, padx=5, pady=4, sticky="w")

##########################################################

# Funktion zum Speichern der Koordinaten
def save_button_clicked_docking():
    save_docking_coo()
    print("Koordinaten gespeichert!")

# Erstellen Sie ein Eingabefeld für die Docking-Koordinaten
docking_coo_label = tk.Label(input_frame, text="Docking-Koordinaten:")
docking_coo_label.grid(row=5, column=0, sticky="w")
docking_coo_entry = tk.Entry(input_frame)
docking_coo_entry.grid(row=5, column=1, padx=5, pady=4, sticky="w")

# Laden der gespeicherten Koordinaten beim Programmstart
docking_coo_entry.insert(tk.END, load_docking_coo())

# Erstellen Sie einen Speichern-Button
save_button = tk.Button(input_frame, image=save_icon, compound="left", command=save_button_clicked_docking)
save_button.grid(row=5, column=2, padx=5, pady=4, sticky="w")

#########################################################

# Funktion zum Speichern der Koordinaten
def save_button_clicked_clear_cargo():
    save_clear_cargo_coo()
    print("Koordinaten gespeichert!")

# Erstellen Sie ein Eingabefeld für die Clear-Cargo-Koordinaten
clear_cargo_coo_label = tk.Label(input_frame, text="Clear-Cargo-Koordinaten:")
clear_cargo_coo_label.grid(row=6, column=0, sticky="w")
clear_cargo_coo_entry = tk.Entry(input_frame)
clear_cargo_coo_entry.grid(row=6, column=1, padx=5, pady=4, sticky="w")

# Laden der gespeicherten Koordinaten beim Programmstart
clear_cargo_coo_entry.insert(tk.END, load_clear_cargo_coo())

# Erstellen Sie einen Speichern-Button
save_button = tk.Button(input_frame, image=save_icon, compound="left", command=save_button_clicked_clear_cargo)
save_button.grid(row=6, column=2, padx=5, pady=4, sticky="w")

########################################################

# Funktion zum Speichern der Koordinaten
def save_button_clicked_target_one():
    save_target_one_coo()
    print("Koordinaten gespeichert!")

# Erstellen Sie ein Eingabefeld für die Target-One-Koordinaten
target_one_coo_label = tk.Label(input_frame, text="Target-One-Koordinaten:")
target_one_coo_label.grid(row=7, column=0, sticky="w")
target_one_coo_entry = tk.Entry(input_frame)
target_one_coo_entry.grid(row=7, column=1, padx=5, pady=4, sticky="w")

# Laden der gespeicherten Koordinaten beim Programmstart
target_one_coo_entry.insert(tk.END, load_target_one_coo())

# Erstellen Sie einen Speichern-Button
save_button = tk.Button(input_frame, image=save_icon, compound="left", command=save_button_clicked_target_one)
save_button.grid(row=7, column=2, padx=5, pady=4, sticky="w")

#######################################################

# Funktion zum Speichern der Koordinaten
def save_button_clicked_target_two():
    save_target_two_coo()
    print("Koordinaten gespeichert!")

# Erstellen Sie ein Eingabefeld für die Target-Two-Koordinaten
target_two_coo_label = tk.Label(input_frame, text="Target-Two-Koordinaten:")
target_two_coo_label.grid(row=8, column=0, sticky="w")
target_two_coo_entry = tk.Entry(input_frame)
target_two_coo_entry.grid(row=8, column=1, padx=5, pady=4, sticky="w")

# Laden der gespeicherten Koordinaten beim Programmstart
target_two_coo_entry.insert(tk.END, load_target_two_coo())

# Erstellen Sie einen Speichern-Button
save_button = tk.Button(input_frame, image=save_icon, compound="left", command=save_button_clicked_target_two)
save_button.grid(row=8, column=2, padx=5, pady=4, sticky="w")

#######################################################

# Funktion zum Speichern der Koordinaten
def save_button_clicked_mining_mouse_reset():
    save_mining_mouse_reset_coo()
    print("Koordinaten gespeichert!")

# Erstellen Sie ein Eingabefeld für die Mining-Mouse-Reset-Koordinaten
mining_mouse_reset_coo_label = tk.Label(input_frame, text="Mining Mouse Reset-Koordinaten:")
mining_mouse_reset_coo_label.grid(row=9, column=0, sticky="w")
mining_mouse_reset_coo_entry = tk.Entry(input_frame)
mining_mouse_reset_coo_entry.grid(row=9, column=1, padx=5, pady=4, sticky="w")

# Laden der gespeicherten Koordinaten beim Programmstart
mining_mouse_reset_coo_entry.insert(tk.END, load_mining_mouse_reset_coo())

# Erstellen Sie einen Speichern-Button
save_button = tk.Button(input_frame, image=save_icon, compound="left", command=save_button_clicked_mining_mouse_reset)
save_button.grid(row=9, column=2, padx=5, pady=4, sticky="w")

#########################################################

def save_button_clicked_mining():
    save_mining_coo()
    print("Koordinaten gespeichert!")

# Erstellen Sie ein Textfeld für die Mining-Koordinaten
mining_coo_label = tk.Label(input_frame, text="Mining Koordinaten:")
mining_coo_label.grid(row=10, column=0, sticky="w")
mining_coo_entry = tk.Text(input_frame, width=15, height=5)
mining_coo_entry.grid(row=10, column=1, padx=5, pady=4, sticky="w")

# Laden der gespeicherten Koordinaten beim Programmstart
mining_coo_entry.insert(tk.END, load_mining_coo())

# Erstellen Sie einen Speichern-Button
save_button = tk.Button(input_frame, image=save_icon, compound="left", command=save_button_clicked_mining)
save_button.grid(row=10, column=2, padx=5, pady=4, sticky="w")

#########################################################

# Erstellen Sie einen Start-Button
start_button = tk.Button(button_frame, text="Start", command=start_function)
start_button.grid(row=0, column=0, padx=(0, 10), ipadx=5)

# Erstellen Sie einen Stop-Button
stop_button = tk.Button(button_frame, text="Stop", command=stop_function)
stop_button.grid(row=0, column=1, padx=(10, 0), ipadx=5)

########################################################

# Erstellen Sie ein Label zur Anzeige der Mausposition
mouse_position_label = tk.Label(root, text="")
mouse_position_label.pack(pady=10)

# Funktion zum Aktualisieren der Mausposition
def update_mouse_position():
    x, y = get_mouse_position()
    mouse_position_label.config(text=f"Mausposition: {x}, {y}")
    mouse_position_label.after(100, update_mouse_position)

# Starten Sie die Funktion zum Aktualisieren der Mausposition
update_mouse_position()

# Starten Sie das Tkinter-Fenster
root.mainloop()