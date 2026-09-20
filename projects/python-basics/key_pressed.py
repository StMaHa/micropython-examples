# Key pressed example in Python
import keyboard  # Requires the 'keyboard' library

# Key press event handler function (callback function)
def on_key_press(event):
    print(event.name)

# Setting up key press event handler, callback function will be triggered on key press
keyboard.on_press(on_key_press)

# Running main loop and listening for key events
while True:
    pass