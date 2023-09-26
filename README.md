# Eve Online Mining Bot

The Mining Bot Alpha Owl-Edition is a Python program developed to automate mining in EVE Online. This bot utilizes the pyautogui framework to simulate user inputs. 

[![Video auf YouTube](https://img.youtube.com/vi/5wEN07A2q3Q/maxresdefault.jpg)](https://www.youtube.com/watch?v=5wEN07A2q3Q)


## Features

- Automated mining in EVE Online
- User-friendly GUI for configuration
- Easy control of bot start and stop
- Display of the current mouse position on the screen

## Requirements

To run the Eve Online Mining Bot, you must install the necessary Python modules. Use the following command:

```bash
pip install -r requirements.txt
```

## Usage

1. Ensure that you have installed the required modules as per the requirements.

2. Initiate the program by executing the main.py file.
```
python main.py
```
3. Configure various settings in the user interface:

   - mining duration: Specify the desired duration of the mining operation in minutes.
   - cargo loading time in seconds: Enter the calculated "loading time" (without decimal places) based on cargo volume and mining rate (see below for the calculation formula).
   - Undock Position: Set the mouse coordinates for the Undock button on the station.
   - Clear Cargo Position: Specify the mouse position for unloading cargo. This transfers the ore to the inventory window above.
   - Station-Overview Position: Set the mouse coordinates of the station in the Overview; it should be at the top when the ship returns to the station's grid.
   - Target-One Overview Position: Set the first mouse coordinate to the asteroids in the Overview.
   - Target-Two Overview Position Position: Define the second coordinate in the Overview.
   - Mouse-Reset Primary Position: Specify the position for resetting mining targets (an empty space location with no windows, elements or brackets).
   - Mouse-Reset Secondary Position: Define the position for resetting drones (an empty space location with no windows, elements or brackets).
   - Home Bookmark: Set the coordinates for the Station Bookmark.
   - Belt Bookmarks: Enter the coordinates for your Belt Bookmarks (one line per bookmark).

4.  Click the "Save" button to hold the entered coordinates so that they persist across sessions.
   
5. Click the "Start" button to initiate the mining bot.
   
6. To stop the bot, click the "Stop" button.

## Display of Mouse Position
The GUI application continuously displays the current mouse position on the screen. This can be helpful for accurately determining the coordinates for the positions mentioned above.

## Belt Time Calculation
The "Belt Time" refers to the time required to deplete the cargo volume in your mining ship using your mining laser rate. The calculation is as follows:
```
Belt Time (seconds) = Cargo Volume (m³) / (Number of mining lasers * Mining rate per second (m³/s))
```
For example:

Assuming you are using a Venture with a cargo volume of 5000 m³ and two mining lasers, each with a mining rate of 1.5 m³ per second. The calculation would be as follows:
```
Belt Time = 5000 m³ / (2 * 1.5 m³/s) = 1666 seconds
```
In this case, it would take approximately 1666 seconds to deplete the entire cargo volume. Enter the calculated "Belt Time" in seconds (without decimal places) into the corresponding field in the GUI to execute the mining bot according to your configuration.

## Notes
This is an open-source project provided without any guarantees. Use it at your own risk.

Please ensure that you comply with EVE Online's terms of use and policies. The use of bots or automation may violate the game's terms of service.
