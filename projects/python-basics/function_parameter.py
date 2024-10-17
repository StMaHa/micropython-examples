# Example 1
def print_hello_world():
    print("Hello World!")

print_hello_world()

# Example 2
def print_worte_1(wort1, wort2):
    print(f"{wort1} {wort2}")

print_worte_1("Hallo", "python")

# Example 3
def print_worte_2(wort1="Hello", wort2="World"):
    print(f"{wort1} {wort2}")

print_worte_2()
print_worte_2("Hallo", "python")
print_worte_2(wort1="Hallo", wort2="Python")

# Example 4
def print_gruss(name, gruss_wort="Hello", satzzeichen="!"):
    print(f"{gruss_wort} {name}{satzzeichen}")

print_gruss("Stefan")
print_gruss("Stefan", gruss_wort="Hallo")
print_gruss("Stefan", satzzeichen=".")
print_gruss("Stefan", gruss_wort="Hallo")
print_gruss("Stefan", satzzeichen=".", gruss_wort="Hey")
