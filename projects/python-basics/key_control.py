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
    # escape / exit / cancel
    "esc": "esc"
}

# Key press event handler function (callback function)
def on_key_press(event):
    if event.name in key_dict:
        print(f"Send control key {key_dict[event.name]}...")

def on_key_release(event):
    print("Key release:", event.name)

def on_key_action(event):  # Haupt-Callback-Funktion
    if event.event_type == keyboard.KEY_DOWN:  # on key press
        on_key_press(event)
    elif event.event_type == keyboard.KEY_UP:  # on key release
        on_key_release(event)

print("Press cursor keys or 'esc' to end program.")

# Nur ein Callback-Handler einer Hardwarefunktionalitaet moeglich.
# z.B. Keyboard und Pin Callback koennen gemischt werden.
#keyboard.on_press(on_key_press)
#keyboard.on_release(on_key_release)

# Setting up key press event handler, callback function will be triggered on key press
keyboard.on_press(on_key_action)  # Register Main-Callback-Function
keyboard.wait('esc')

print("Program terminated.")