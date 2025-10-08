
# __init__ method and different types of methods

class Student:
    school_name = "Telusko Academy"  # class variable

    def __init__(self, name, age):
        self.name = name    # instance variable
        self.age = age

    # instance method
    def show(self):
        print(f"Student: {self.name}, Age: {self.age}")

    # class method
    @classmethod
    def school(cls):
        print("School:", cls.school_name)

    # static method
    @staticmethod
    def greet():
        print("Welcome to Telusko Academy!")

def main():
    s1 = Student("Naveen", 25)
    s1.show()

    Student.school()   # calling class method
    Student.greet()    # calling static method

if __name__ == "__main__":
    main()