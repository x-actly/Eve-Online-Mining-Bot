# Eve Online Mining Bot

The Mining Bot Alpha Owl-Edition is a Python program developed to automate mining in EVE Online. This bot utilizes the pyautogui framework to simulate user inputs. 

[![Video auf YouTube](https://img.youtube.com/vi/-qzjmKXXsqU/maxresdefault.jpg)](https://www.youtube.com/watch?v=-qzjmKXXsqU)
[youtube link]

## Features

- Automated mining in EVE Online
- User-friendly GUI for configuration
- Easy control of bot start and stop
- Display of the current mouse position on the screen

## Requirements

To run this bot, you must install python first! You can find several Tutorials on youtube.com.

If Python is working on your machine correctly, you must install the necessary Python modules. Use the following command:

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

   - mining runs: Specify the desired amount of mining runs you want the bot to complete. This will be a part of the calculation for how long the bot will run.
   - Undock Position: Set the mouse coordinates for the Undock button on the station.
   - Clear Cargo Position: Specify the mouse position for unloading cargo. This transfers the ore to the inventory window above. Use Test Button to make it work correctly. 
   - Mining Hold: Set volume from your mining cargo.
   - Mining Yield: Set mining rate of your mining laser. Check the Calculation below.
   - Target-One Overview Position: Set the first mouse coordinate to the asteroids in the Overview.
   - Target-Two Overview Position Position: Define the second coordinate in the Overview.
   - Mouse-Reset Primary Position: Specify the position for resetting mining targets (an empty space location with no windows, elements or brackets).
   - Home Bookmark: Set the coordinates for the Station Bookmark.
   - Belt Bookmarks: Enter the coordinates for your Belt Bookmarks (one line per bookmark).

   For all the settings above, you can click into the text field, move your mouse into the eve interface and type Ctrl-i to insert the current mouse position in the text field. For text fields the contents will be replaced, for the text area a new line will be appended.

4. Click the "Save" button to hold the entered coordinates so that they persist across sessions.

5. Set Mining Laser to High Power Slot 1-2.

6. Set Shield Hardener to High Power Slot 3, if using a venture that have three high power slots. For a retriever this will be different and you need to configure hardener_key under [SETTINGS] in properties and set it to Alt-F2, for ex if you set the hardener into the second medium power slot.

7. Make sure you set shortcuts on default, but if you want to override "Unlock all targets" under "Combat" in "Shortcut" under "Settings", you can configure unlock_all_targets_key under [SETTINGS] in properties and this will make the bot properly unlock all asteroids with one command instead of using a lot of time to cancel selections for target one and two.
   
8. If you are ready, dock up and click the "Start" button to initiate the mining bot.
   
9. Click the stop button if you want to end the bot prematurely. It will complete the current mining cycle and then stop flying into the belt. 

## Display of Mouse Position
The GUI application continuously displays the current mouse position on the screen. This can be helpful for accurately determining the coordinates for the positions mentioned above.

## Mining Hold Loading Calculation
The "Mining Hold Loading Calculation" refers to the time required to deplete the cargo volume in your mining ship using your mining laser rate (Mining Yield).

Assuming you are using a Venture with a cargo volume of 5000 m³ and two mining lasers, each with a mining yield of 1.5 m³ per second. The calculation would be as follows:
```
Mining Hold Loading Time = 5000 m³ / (2 * 1.5 m³/s) = 1666 seconds
```
In this case, it would take approximately 1666 seconds to deplete the entire cargo volume. Set the mining hold and yield and the script automatically calculate the loading time for you.

## Using something else than a Venture

For a Retriever this config will work, given you have two strip miners that both yield 7 m3 per second. Set your shield hardener in medium slot 2 (alt-f2) and your good to go

```properties
[SETTINGS]
mining_runs = 
mining_hold = 33000
mining_yield = 14
mining_reset_timer = 180
hardener_key = Alt-F2
```

## Notes
This is an open-source project provided without any guarantees. Use it at your own risk.

Please ensure that you comply with EVE Online's terms of use and policies. The use of bots or automation may violate the game's terms of service.
