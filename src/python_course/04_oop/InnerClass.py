class Student:
    def __init__ (self, name, roll_no):
        self.name = name
        self.roll_no = roll_no
        self.laptop = self.Laptop()

    def to_string(self):
        self.laptop.to_string()
        return f'Student {self.name}, roll no: {self.roll_no}'

    class Laptop:
        def __init__(self):
            self.brand = "Apple"
            self.cpu = 'M5'
            self.ram = '24GB'
            self.disk = '512GB'

        def to_string(self):
            print(f'Laptop {self.brand}, {self.cpu}, {self.ram}, {self.disk}')

student1 = Student('Ankit',1)
print(student1.to_string())