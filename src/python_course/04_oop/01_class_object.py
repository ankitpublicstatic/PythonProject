# Class and object demo
class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    def display(self):
        print(self.brand, self.model)
c=Car("Toyota","Corolla")
c.display()
