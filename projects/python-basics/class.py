class MyClass():
    # Konstruktor
    def __init__(self, value):
        # Instanzattribute
        self.__value = value
    
    # Setter-Methode
    def set_value(self, value):
        self.__value = value

    # Getter-Methode
    def get_value(self):
        return self.__value
    
    # Methode addiert einen Wert
    def add_value(self, value):
        self.__value += value

# Erzeuge Instanz von Klasse
instance = MyClass(2)

print(instance.get_value())

instance.set_value(3)

print(instance.get_value())

instance.add_value(4)

print(instance.get_value())