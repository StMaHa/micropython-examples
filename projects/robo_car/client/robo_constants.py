"""Constants for the Robo Car client."""

# Default target name
BLE_TARGET_NAME = "JDY-33-BLE"
SPP_TARGET_NAME = "JDY-33-SPP"

# BLE service and characteristic UUIDs for the Robo Car.
BLE_UUID_SERVICE = '0000ffe0-0000-1000-8000-00805f9b34fb'
BLE_UUID_WRITE = '0000ffe1-0000-1000-8000-00805f9b34fb'
BLE_UUID_NOTIFY = '0000ffe1-0000-1000-8000-00805f9b34fb'

# Key mapping dictionary for controlling the Robo Car via keyboard inputs.
KEY_DICT = {
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
    "enter": "run",
    # escape / exit / cancel
    "esc": "esc"
}