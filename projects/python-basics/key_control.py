# Control by keyboard example in Python
import keyboard  # Requires the 'keyboard' library


key_dict = {
    # up / forward
    "up": "up",     
    "nach-oben": "up",
    # down / backward
    "down": "dn",
    "nach-unten": "dn",
    # left / turn left
    "left": "lt",   
    "nach-links": "lt",
    # right / turn right
    "right": "rt",
    "nach-rechts": "rt",
    # stop
    "end": "sp",
    "ende": "sp",
    "clear": "sp",
    # escape / exit / cancel
    "esc": "esc"
}

# Key press event handler function (callback function)
def on_key_press(event):
    if event.name in key_dict:
        print(f"Send control key {key_dict[event.name]}...")

# Setting up key press event handler, callback function will be triggered on key press
keyboard.on_press(on_key_press)
keyboard.wait('esc')

print("Program terminated.")