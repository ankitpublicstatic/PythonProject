# Class and object demo
class Car:
    def __init__(self, brand: str, model: str):
        self.brand = brand
        self.model = model

    def display(self):
        print(self.brand, self.model)

car = Car("Tata","Safari")
car.display()