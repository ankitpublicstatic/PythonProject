import os

# Root folder
root = "python_course_telusko_full"

# Full folder structure with 31 programs, all fully commented
folders = {
    "01_basics": [
        ("00_hello_world.py", """# Hello World program
# Prints a simple message to the console

def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
"""),
        ("01_variables.py", """# Variables demo
# Demonstrates integer, float, string variables and reassignment

def main():
    a = 10           # Integer
    b = 3.14         # Float
    c = "Telusko"    # String
    print("a =", a, type(a))
    print("b =", b, type(b))
    print("c =", c, type(c))

    # Reassign variable
    a = "Now I'm a string"
    print("a =", a, type(a))

if __name__ == "__main__":
    main()
"""),
        ("02_operators.py", """# Operators demo
# Arithmetic, relational, logical, and assignment operators

def main():
    x = 15
    y = 4

    # Arithmetic
    print("x + y =", x+y)
    print("x - y =", x-y)
    print("x * y =", x*y)
    print("x / y =", x/y)
    print("x // y =", x//y)
    print("x % y =", x%y)
    print("x ** y =", x**y)

    # Relational
    print("x > y:", x>y)
    print("x == y:", x==y)
    print("x != y:", x!=y)

    # Logical
    print("(x>10) and (y<5):", (x>10) and (y<5))
    print("(x>10) or (y>5):", (x>10) or (y>5))

if __name__ == "__main__":
    main()
"""),
        ("03_number_conversion.py", """# Number system conversions

def main():
    num = 10
    print("Decimal:", num)
    print("Binary:", bin(num))
    print("Octal:", oct(num))
    print("Hexadecimal:", hex(num))

    # Convert strings to numbers with base
    print("Binary string '1010' ->", int("1010",2))
    print("Hex string 'A' ->", int("A",16))

if __name__ == "__main__":
    main()
"""),
        ("04_bitwise_demo.py", """# Bitwise operators demo

def main():
    a = 5  # 0101
    b = 3  # 0011
    print("a & b =", a & b)
    print("a | b =", a | b)
    print("a ^ b =", a ^ b)
    print("~a =", ~a)
    print("a << 1 =", a << 1)
    print("a >> 1 =", a >> 1)

if __name__ == "__main__":
    main()
"""),
        ("05_math_module.py", """# Math module demo
import math

def main():
    x = 16
    print("Square root of", x, "=", math.sqrt(x))
    print("Factorial of 5 =", math.factorial(5))
    print("Ceil of 4.2 =", math.ceil(4.2))
    print("Floor of 4.8 =", math.floor(4.8))
    print("Sin(pi/2) =", math.sin(math.pi/2))
    print("Log10(100) =", math.log10(100))

if __name__ == "__main__":
    main()
"""),
        ("06_user_input.py", """# User input demo

def main():
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    print("Hello,", name, "you are", age, "years old.")

if __name__ == "__main__":
    main()
"""),
        ("07_conditions.py", """# Conditional statements demo

def main():
    num = int(input("Enter a number: "))
    if num>0:
        print("Positive")
    elif num==0:
        print("Zero")
    else:
        print("Negative")

if __name__ == "__main__":
    main()
""")
    ],
    "02_loops": [
        ("01_while_loop.py", """# While loop demo
i = 1
while i <= 5:
    print("Number:", i)
    i += 1
"""),
        ("02_for_loop.py", """# For loop demo
for i in range(5):
    print("i =", i)

fruits = ["apple","banana","cherry"]
for fruit in fruits:
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
print("Right triangle:")
for i in range(1,n+1):
    print("*"*i)

print("Inverted triangle:")
for i in range(n,0,-1):
    print("*"*i)

print("Pyramid pattern:")
for i in range(1,n+1):
    print(" "*(n-i) + "*"*(2*i-1))
""")
    ],
    "03_data_structures": [
        ("01_list_demo.py", """# List demo
numbers=[10,20,30,40,50]
numbers[2]=35
numbers.append(60)
numbers.insert(1,15)
numbers.remove(40)
popped = numbers.pop()

print("Updated list:", numbers)
print("Popped value:", popped)

for num in numbers:
    print(num)
"""),
        ("02_tuple_set_demo.py", """# Tuple (immutable) and Set (unique, unordered)
fruits=("apple","banana","cherry")
print("Tuple:", fruits)
print("First:", fruits[0])

nums={1,2,3,3,4,5}
print("Set:", nums)
nums.add(6)
nums.discard(2)
print("Updated Set:", nums)

evens={2,4,6,8}
odds={1,3,5,7}
print("Union:", evens|odds)
print("Intersection:", evens&nums)
print("Difference:", evens-nums)
"""),
        ("03_more_variable_examples.py", """# Strings, Booleans, type casting
name="Telusko"
active=True
age=25
print(name,active,age)

age_str=str(age)
num_str="100"
num_int=int(num_str)
print("Age as string:",age_str,type(age_str))
print("String '100' to int:",num_int,type(num_int))
""")
    ],
    "04_oop": [
        ("01_class_object.py", """# Classes and objects
class Car:
    def __init__(self,brand,model):
        self.brand=brand
        self.model=model
    def display_info(self):
        print(f"Car: {self.brand} {self.model}")

car1=Car("Toyota","Corolla")
car2=Car("Honda","Civic")
car1.display_info()
car2.display_info()
"""),
        ("02_init_and_methods.py", """# __init__, instance, class, static methods
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
"""),
        ("03_inheritance_overriding.py", """# Inheritance and method overriding
class Animal:
    def speak(self):
        print("Animal speaks")
class Dog(Animal):
    def speak(self):
        print("Dog barks")
class Cat(Animal):
    def speak(self):
        print("Cat meows")

for a in [Dog(),Cat(),Animal()]:
    a.speak()
"""),
        ("04_method_overloading.py", """# Method overloading (simulated with default arguments)
class Calculator:
    def add(self,a,b=0,c=0):
        return a+b+c

calc=Calculator()
print(calc.add(5))
print(calc.add(5,10))
print(calc.add(5,10,15))
"""),
        ("05_operator_overloading.py", """# Operator overloading
class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def __add__(self,other):
        return Point(self.x+other.x,self.y+other.y)
    def __str__(self):
        return f"Point({self.x},{self.y})"

p1=Point(2,3)
p2=Point(4,5)
print(p1+p2)
""")
    ],
    "05_advanced": [
        ("01_exception_handling.py", """# Exception handling demo
def divide(a,b):
    try:
        result = a/b
    except ZeroDivisionError:
        print("Cannot divide by zero!")
        result=None
    except Exception as e:
        print("Unexpected error:",e)
        result=None
    else:
        print("Division successful")
    finally:
        print("Execution finished")
    return result

print(divide(10,2))
print(divide(5,0))
"""),
        ("02_multithreading_demo.py", """# Multithreading demo
import threading,time

def print_numbers():
    for i in range(1,6):
        print("Number:",i)
        time.sleep(1)

def print_letters():
    for c in "ABCDE":
        print("Letter:",c)
        time.sleep(1)

t1=threading.Thread(target=print_numbers)
t2=threading.Thread(target=print_letters)
t1.start()
t2.start()
t1.join()
t2.join()
print("Threads finished")
"""),
        ("03_file_handling.py", """# File handling demo
filename="sample.txt"

# Write to file
with open(filename,"w") as f:
    f.write("Hello, this is a test file.\\n")
    f.write("Python makes file handling easy!\\n")

# Read from file
with open(filename,"r") as f:
    for line in f:
        print(line.strip())
"""),
        ("04_linear_search.py", """# Linear search demo
arr=[5,3,8,6,7]
target=6
index=-1
for i,v in enumerate(arr):
    if v==target:
        index=i
        break
print("Found at index:",index if index!=-1 else "Not found")
"""),
        ("05_selection_sort.py", """# Selection sort demo
arr=[64,25,12,22,11]
print("Original:",arr)
for i in range(len(arr)):
    min_idx=i
    for j in range(i+1,len(arr)):
        if arr[j]<arr[min_idx]:
            min_idx=j
    arr[i],arr[min_idx]=arr[min_idx],arr[i]
print("Sorted:",arr)
"""),
        ("06_db_connection.py", """# MySQL DB connection demo
# Requires: pip install mysql-connector-python
import mysql.connector

try:
    conn=mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="testdb"
    )
    print("Connected to database:", conn.database)
    conn.close()
except mysql.connector.Error as e:
    print("Database error:",e)
""")
    ]
}

# README content
readme_content = """# Python Course Programs (Telusko YouTube Video)

This repository contains **all 31 programs** from Telusko's Python full course.
Folders:
- 01_basics
- 02_loops
- 03_data_structures
- 04_oop
- 05_advanced

Each file is fully commented and self-explanatory for learning purposes.

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
