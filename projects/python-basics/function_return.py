# Example 1
def print_hello_world():
    print("Hello World!")

print_hello_world()

# Example 2
def addieren(wert1, wert2):
    summe = wert1 + wert2
    return summe

print("Summe:", addieren(3, 5))

def addieren_2(wert1, wert2):
    return wert1 + wert2

print("Summe:", addieren_2(3, 5))

# Example 3
def get_address_from_db():
    strasse = "Lindenstrasse"
    hausnummer = 123
    ort = "Bärstadt"
    return strasse, hausnummer, ort

print(get_address_from_db())

def get_address_from_db_2():
    adresse = ["Lindenstrasse",
               123, "Bärstadt"]
    # Rückgabewert ist eine Liste
    return adresse

print(get_address_from_db_2())
