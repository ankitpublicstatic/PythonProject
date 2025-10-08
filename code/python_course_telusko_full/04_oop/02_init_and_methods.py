# __init__, instance, class, static methods
class Student:
    school_name="Telusko Academy"
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def show(self):
        print(f"Student: {self.name}, Age: {self.age}")
    @classmethod
    def school(cls):
        print("School:",cls.school_name)
    @staticmethod
    def greet():
        print("Welcome to Telusko Academy!")

s1=Student("Naveen",25)
s1.show()
Student.school()
Student.greet()
