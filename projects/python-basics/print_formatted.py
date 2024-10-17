name = "John"  # Variable mit einem Text
alter = 30     # Variable mit einer Zahl
print(name)
print(alter)
print(name, "ist", alter, "Jahre alt.")

alter = alter + 1
print(name, "ist", alter, "Jahre alt.")
alter = alter + 1
print(name, "ist", alter, "Jahre alt.")

###
name = "Welt"
zahl = 123

print("Hallo", name, zahl, "!")

# nun richtig formatiert...
print(f"Hallo {name} {zahl}!")
# oder…
print("Hallo {} {}!".format(name, zahl))

###
name = "Welt"
zahl = 123

# Zeilenwechsel
print("Das ist ein Zeilen-\nwechsel.")

# formatiert per Variable
text = f"Hallo {name}\n{zahl}!"
print(text)
