# Example 6
wert = None
if wert is not None:
    print("Wert ist nicht None!")
else:
    print("Wert ist None!")

wert = None
if wert:
    print("Wert ist nicht None!")
else:
    print("Wert ist None!")

text = input("Eingabe [Enter]: ")  # [Enter]
if not text == "":  # text != ""
    print("Text ist nicht leer!")
else:
    print("Text ist leer!")

text = input("Eingabe [Enter]: ")  # [Enter]
if text:
    print("Text ist nicht leer!")
else:
    print("Text ist leer!")