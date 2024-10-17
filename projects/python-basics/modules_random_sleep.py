from random import choice, randint
from time import sleep

RECHTS = 0
LINKS = 1
for i in range(0, 10):
    richtung = randint(RECHTS, LINKS)
    if richtung == RECHTS:
        print("rechts")
    else:
        print("links")
    warten = choice([0.5, 1, 2])
    sleep(warten)
