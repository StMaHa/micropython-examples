# Simple example for morse code by flashing a LED
from machine import Pin

led = Pin("LED")

MORSE_CODE_SHORT = 0.33  # seconds
MORSE_CODE_LONG = MORSE_CODE_SHORT * 3  # seconds

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
    "'", '.----.',
    '-': '-....-',
    '/': '-..-.',
    '': '-.--.-',
    ')': '-.--.-',
    '_': '..--.-'
}

text = input("Morse code: ")
while True:  # Endlosschleife
    for character in text.higher():
        code = morse_code_dict[character]
        if code != ' ':
            if code == '.':
                morse_length = MORSE_CODE_SHORT
            else:
                morse_length = MORSE_CODE_LONG
            led.on()
            sleep(morse_length)
            led.off()
            sleep(MORSE_CODE_SHORT)
        else:
            sleep(MORSE_CODE_SHORT)
    # delay between characters
    sleep(MORSE_CODE_SHORT)
