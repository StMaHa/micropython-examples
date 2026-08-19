# Simple example for morse code by flashing a LED
from machine import Pin
from time import sleep

led = Pin("LED", Pin.OUT)

MORSE_CODE_SHORT_DELAY = 0.33  # seconds
MORSE_CODE_LONG_DELAY = MORSE_CODE_SHORT_DELAY * 3  # seconds
MORCE_CODE_WORD_DELAY = MORSE_CODE_SHORT_DELAY * 6  # seconds

morse_code_dict = {
    'A': '.-',
    'B': '-...',
    'C': '-.-.',
    'D': '-..',
    'E': '.',
    'F': '..-.',
    'G': '--.',
    'H': '....',
    'I': '..',
    'J': '.---',
    'K': '-.-',
    'L': '.-..',
    'M': '--',
    'N': '-.',
    'O': '---',
    'P': '.--.',
    'Q': '--.-',
    'R': '.-.',
    'S': '...',
    'T': '-',
    'U': '..-',
    'V': '...-',
    'W': '.--',
    'X': '-..-',
    'Y': '-.--',
    'Z': '--..',
    '0': '-----',
    '1': '.----',
    '2': '..---',
    '3': '...--',
    '4': '....-',
    '5': '.....',
    '6': '-....',
    '7': '--...',
    '8': '---..',
    '9': '----.',
    ' ': ' ',
    ',': '--..--',
    '.': '.-.-.-',
    '?': '..--..',
    ';': '-.-.-.',
    ':': '---...',
    "'": '.----.',
    '-': '-....-',
    '/': '-..-.',
    '': '-.--.-',
    ')': '-.--.-',
    '_': '..--.-'
}
text = input("Enter text to morse: ")  # e.g. sos
try:
    while True:  # Endlosschleife
        for character in text:
            morse_code = morse_code_dict[character.upper()]
            for code in morse_code:
                if code == ' ':  # White space, e.g. between words
                    sleep(MORSE_CODE_SHORT_DELEAY)
                    continue
                elif code == '.':
                    morse_length = MORSE_CODE_SHORT_DELAY
                elif code == "-":
                    morse_length = MORSE_CODE_LONG_DELAY
                else:
                   continue
                led.on()
                sleep(morse_length)
                led.off()
                sleep(MORSE_CODE_SHORT_DELAY)
        sleep(MORSE_CODE_LONG_DELAY)  # Delay after text send.
except KeyboardInterrupt:
    print("Programmende")
    led.off()
