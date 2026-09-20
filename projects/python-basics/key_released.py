# Key released example in Python
import keyboard  # Requires the 'keyboard' library

# Key release event handler function (callback function)
def on_key_release(event):
    print(event.name)

# Setting up key release event handler, callback function will be triggered on key release
keyboard.on_release(on_key_release)

# Running main loop and listening for key events
while True:
    pass