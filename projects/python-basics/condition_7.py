# Example 6
text = input("Eingabe: ") 
if len(text) > 1:
    print("Text hat mehr als 1 Zeichen!")

text = input("Eingabe von kleinen Buchstaben: ")  # python
if text.islower():
    print("Alle Buchstaben sind klein!")

text = "Python"
if "th" in text:
    print("Wort enthält 'th'!")
