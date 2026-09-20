# Key event example in Python
import keyboard  # Requires the 'keyboard' library

# Key press event handler function (callback function)
def on_key_event(event):
    if event.event_type == 'down':
        print(f"Key {event.name} pressed")
    elif event.event_type == 'up':
        print(f"Key {event.name} released")

# Setting up key press event handler, callback function will be triggered on key press
    keyboard.hook(on_key_event)

# Running main loop and listening for key events
while True:
    pass