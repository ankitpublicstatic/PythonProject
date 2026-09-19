class Student:

    school = "Adani University"

# instance variable with constructor, instance variable assignment
    def __init__ (self, m1,m2, m3):
        self.m1 = m1
        self.m2 = m2
        self.m3 = m3

# Instance method
    def avg(self):
        return (self.m1 + self.m2 + self.m3) / 3

    @classmethod
    def get_school_name(cls):
        return cls.school

    def to_string(self):
        return f"{self.m1} {self.m2} {self.m3}"

    # Not null check utility method / static method
    @staticmethod
    def not_null(obj1):
        return obj1 != None

student1 = Student(80,90,95)
student2 = Student(80,90,90)

print(student1.to_string())
print(student2.to_string())
print(Student.not_null(student1))
print(student1.avg())
print(student2.avg())
print(Student.get_school_name())

