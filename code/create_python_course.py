import os

# Root folder
root = "python_course_telusko"

# Folder structure
folders = {
    "01_basics": [
        ("00_hello_world.py", """# Hello World program
def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
"""),
        ("01_variables.py", """# Variables demo
def main():
    a = 10
    b = 3.14
    c = "Telusko"
    print(a, b, c)
    a = "Now I'm a string"
    print(a)
if __name__ == "__main__":
    main()
"""),
        ("02_operators.py", """# Operators demo
def main():
    x = 15; y = 4
    print("x + y =", x+y)
    print("x - y =", x-y)
    print("x * y =", x*y)
    print("x / y =", x/y)
    print("x // y =", x//y)
    print("x % y =", x%y)
    print("x ** y =", x**y)
if __name__ == "__main__":
    main()
"""),
        ("03_number_conversion.py", """# Number system conversion demo
def main():
    num = 10
    print("Decimal:", num)
    print("Binary:", bin(num))
    print("Octal:", oct(num))
    print("Hexadecimal:", hex(num))
if __name__ == "__main__":
    main()
"""),
        ("04_bitwise_demo.py", """# Bitwise operators demo
def main():
    a = 5; b = 3
    print("a & b =", a&b)
    print("a | b =", a|b)
    print("a ^ b =", a^b)
    print("~a =", ~a)
    print("a << 1 =", a<<1)
    print("a >> 1 =", a>>1)
if __name__ == "__main__":
    main()
"""),
        ("05_math_module.py", """# Using math module
import math
def main():
    print(math.sqrt(16))
    print(math.factorial(5))
    print(math.ceil(4.2))
    print(math.floor(4.8))
if __name__ == "__main__":
    main()
"""),
        ("06_user_input.py", """# User input demo
def main():
    name = input("Enter name: ")
    age = int(input("Enter age: "))
    print("Hello", name, "age:", age)
if __name__ == "__main__":
    main()
"""),
        ("07_conditions.py", """# if-elif-else demo
def main():
    num = int(input("Enter number: "))
    if num > 0: print("Positive")
    elif num == 0: print("Zero")
    else: print("Negative")
if __name__ == "__main__":
    main()
""")
    ],
    "02_loops": [
        ("01_while_loop.py", """# While loop demo
i = 1
while i <= 5:
    print(i)
    i += 1
"""),
        ("02_for_loop.py", """# For loop demo
for i in range(5):
    print(i)
for fruit in ["apple","banana","cherry"]:
    print(fruit)
"""),
        ("03_break_continue_pass.py", """# break, continue, pass demo
for i in range(1,10):
    if i==5: break
    print(i)
for i in range(1,10):
    if i%2==0: continue
    print(i)
for i in range(5):
    if i==3: pass
    print(i)
"""),
        ("04_pattern_printing.py", """# Pattern printing demo
n=5
for i in range(1,n+1):
    print("*"*i)
for i in range(n,0,-1):
    print("*"*i)
for i in range(1,n+1):
    print(" "*(n-i) + "*"*(2*i-1))
""")
    ],
    "03_data_structures": [
        ("01_list_demo.py", """# List demo
numbers=[10,20,30]
numbers.append(40)
print(numbers)
"""),
        ("02_tuple_set_demo.py", """# Tuple and Set demo
t=("a","b","c")
s={1,2,2,3}
print(t)
print(s)
"""),
        ("03_more_variable_examples.py", """# More variable examples
name="Telusko"
active=True
age=25
print(name, active, age)
""")
    ],
    "04_oop": [
        ("01_class_object.py", """# Class and object demo
class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    def display(self):
        print(self.brand, self.model)
c=Car("Toyota","Corolla")
c.display()
"""),
        ("02_init_and_methods.py", """# __init__ and methods
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
"""),
        ("03_inheritance_overriding.py", """# Inheritance and overriding
class Animal:
    def speak(self): print("Animal speaks")
class Dog(Animal):
    def speak(self): print("Dog barks")
class Cat(Animal):
    def speak(self): print("Cat meows")
for a in [Dog(),Cat(),Animal()]:
    a.speak()
"""),
        ("04_method_overloading.py", """# Method overloading via default args
class Calc:
    def add(self,a,b=0,c=0):
        return a+b+c
c=Calc()
print(c.add(5))
print(c.add(5,10))
print(c.add(5,10,15))
"""),
        ("05_operator_overloading.py", """# Operator overloading demo
class Point:
    def __init__(self,x,y):
        self.x=x; self.y=y
    def __add__(self,other):
        return Point(self.x+other.x,self.y+other.y)
    def __str__(self):
        return f"({self.x},{self.y})"
p1=Point(2,3); p2=Point(4,5)
print(p1+p2)
""")
    ],
    "05_advanced": [
        ("01_exception_handling.py", """# Exception handling demo
def divide(a,b):
    try: return a/b
    except ZeroDivisionError: print("Cannot divide by zero"); return None
print(divide(10,2))
print(divide(5,0))
"""),
        ("02_multithreading_demo.py", """# Multithreading demo
import threading, time
def numbers():
    for i in range(1,6): print(i); time.sleep(1)
def letters():
    for c in "ABCDE": print(c); time.sleep(1)
t1=threading.Thread(target=numbers)
t2=threading.Thread(target=letters)
t1.start(); t2.start()
t1.join(); t2.join()
"""),
        ("03_file_handling.py", """# File handling demo
with open("sample.txt","w") as f:
    f.write("Hello\\nPython\\n")
with open("sample.txt","r") as f:
    for line in f: print(line.strip())
"""),
        ("04_linear_search.py", """# Linear search demo
arr=[5,3,8,6,7]
target=6
index=-1
for i,v in enumerate(arr):
    if v==target: index=i; break
print("Found at index",index if index!=-1 else "Not found")
"""),
        ("05_selection_sort.py", """# Selection sort demo
arr=[64,25,12,22,11]
for i in range(len(arr)):
    min_idx=i
    for j in range(i+1,len(arr)):
        if arr[j]<arr[min_idx]: min_idx=j
    arr[i],arr[min_idx]=arr[min_idx],arr[i]
print(arr)
"""),
        ("06_db_connection.py", """# MySQL connection demo
import mysql.connector
try:
    conn = mysql.connector.connect(
        host="localhost",user="root",password="password",database="testdb")
    print("Connected to", conn.database)
    conn.close()
except mysql.connector.Error as e:
    print("Error:", e)
""")
    ]
}

# README content
readme_content = """# Python Course Programs (Telusko YouTube Video)

This repository contains all example programs from Telusko's Python full course.

Folders:
- 01_basics
- 02_loops
- 03_data_structures
- 04_oop
- 05_advanced

Each file is commented and self-explanatory.
"""

# Create folders and files
os.makedirs(root, exist_ok=True)

for folder, files in folders.items():
    path = os.path.join(root, folder)
    os.makedirs(path, exist_ok=True)
    for fname, code in files:
        with open(os.path.join(path, fname), "w") as f:
            f.write(code)

# Write README
with open(os.path.join(root, "README.md"), "w") as f:
    f.write(readme_content)

print(f"Folder '{root}' created with all programs!")
print("You can now zip it with: zip -r python_course_telusko.zip python_course_telusko/")
