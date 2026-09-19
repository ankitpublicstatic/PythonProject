class Student:
    def __init__(self):
        self.name = 'Ankit'
        self.age = 27
        self.lap = self.Laptop()

    def display(self):
        print(self.name+' ' , self.age)
        self.lap.display()

    class Laptop:
        def __init__(self):
            self.brand = 'Apple'
            self.cpu = 'M5'
            self.ram = 24

        def display(self):
            print(self.brand + ' ' + self.cpu + ' ' , self.ram)
    
s1 = Student()
s1.display()