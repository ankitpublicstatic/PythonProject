# __init__ and methods
class Student:
    school="Telusko"
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def show(self):
        print(self.name,self.age)
    @classmethod
    def school_name(cls):
        print(cls.school)
    @staticmethod
    def greet():
        print("Welcome!")
s=Student("Naveen",25)
s.show()
Student.school_name()
Student.greet()
