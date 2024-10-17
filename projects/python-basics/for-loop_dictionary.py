wb = {"Bayern": "München",
      "Sachsen": "Dresden",
      "Hessen": "Frankfurt"}

print("Bundesländer:")
for key in wb.keys():
    print(f"- {key}")

print("Hauptstädte:")
for value in wb.values():
    print(f"- {value}")

for key, value in wb.items():
    print(f"Die Hauptstadt von {key} ist {value}.")
