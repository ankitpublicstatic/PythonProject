class Student:
    def __init__(self, m1, m2):
        self.m1 = m1
        self.m2 = m2

    def __str__(self):
        # return f'Student {self.m1} {self.m2}'
        return '{} {}'.format(self.m1, self.m2)

    # Python only support operand overloading like +,-,/,*
    def __add__(self, other):
        return Student(self.m1+ other.m1, self.m2 + other.m2)

    def __sub__(self, other):
        return Student(self.m1- other.m1, self.m2 - other.m2)

    def __mul__(self, other):
        return Student(self.m1 * other.m1, self.m2 * other.m2)

    def __truediv__(self, other):
        return Student(self.m1 / other.m1, self.m2 / other.m2)

    def __gt__(self, other):
        return Student(self.m1 > other.m1, self.m2 > other.m2)

    def __lt__(self, other):
        return Student(self.m1 < other.m1, self.m2 < other.m2)

    def __eq__(self, other):
        return Student(self.m1 == other.m1, self.m2 == other.m2)

    def __ne__(self, other):
        return Student(self.m1 != other.m1, self.m2 != other.m2)

    # Python doesn't support method overloading. but we can achieve by custom logic
    def sum(self, a = None, b = None, c = None):
        if a != None and b !=None and c != None:
            return a + b + c
        elif a != None and b != None:
            return a + b
        else:
            return a



student1 = Student(89,90)
student2 = Student(99,80)
student3 = student1+student2
print(student3)
print(student1 > student2)
print(student1 < student2)

print(student1.sum(9))