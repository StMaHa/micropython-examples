ware = input("Welche Ware kaufen? ")
preis = input(f"Was kostet {ware}? ")
print(f"1 {ware} kostet {preis} €.")

print(f"3 {ware} kosten {preis * 3} €.")
# Typumwandlung
print(f"3 {ware} kosten {int(preis) * 3} €")

