# Dieser Code enthält 2 Laufzeitfehler!

zahlen = [2, 0, 3]
count = 0
while count <= len(zahlen):
    zahl = zahlen[count]
    ergebnis = 10 / zahl
    print(f"10 / {zahl} = {ergebnis}")
    count = count + 1