
"""
Python Core:Python core refers to the fundamental building blocks of the language, including syntax, data types, control structures, functions, and modules. Python is an interpreted, high-level language emphasizing readability. Let's dive deep.
Variables and Data Types
Variables are names that reference objects in memory. Python is dynamically typed, so no need to declare types explicitly.

Primitive Types:
Integers (int): Whole numbers, e.g., x = 5. No size limit in Python 3.
Floats (float): Decimal numbers, e.g., y = 3.14.
Strings (str): Text, e.g., s = "Hello". Immutable, supports slicing (s[1:3] == "el").
Booleans (bool): True or False.

Collection Types:
Lists (list): Mutable, ordered sequences, e.g., lst = [1, 2, 3]. Supports append, pop, indexing.
Tuples (tuple): Immutable lists, e.g., tup = (1, 2, 3). Faster than lists for fixed data.
Dictionaries (dict): Key-value pairs, e.g., d = {'a': 1, 'b': 2}. Keys are hashable (immutable). Ordered since Python 3.7.
Sets (set): Unordered, unique elements, e.g., s = {1, 2, 3}. Great for membership testing and set operations (union, intersection).
"""
# Variables and types

x = 10 # int
y = 3.5 # float
name = "Python" # str
is_true = True # bool

# Collections
my_list = [1,3,4,3] # list
my_tuple = (1,3,4,8) # tuple
my_dict = {'ankit':"iPhone", 'ram':"samsung"} # dict
my_set = {8,3,9} # unique set
# Operations
my_list.append(9)
print(my_dict['ankit'])
my_set.add(10)

"""
Control Structures

Conditionals: if, elif, else
Loops: for(iterates over sequence of elements), while (condition-based)
Comprehensions: list in sorted way like one line collections
Exception Handling: try, except, finally
"""

# Conditional
age = 20
if age >= 18:
    print("You are Adult.")
else:
    print("You are Minor")

# For Loop
for i in range(5): # 0 to 4 index sequence will store into i variables
    print(i)

count = 0
while(count < 3):
    print(count)
    count += 1

# try-except Exception handling

try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
finally:
    print("Cleanup Resource whatever opened in try block")

"""
Functions: Functions are defined with def. They can have parameters, defaults, and return values. 
Python supports *args (Variable args) and **kwargs (Keyword args). 
"""

def greet(name="World"): # Default parameter
    return f"Hello, {name}!"

print(greet())
print(greet(name="Ankit"))

# Variables args

def sum_numbers(*args):
    return sum(args)

print(sum_numbers(1, 2, 3))

# Keyword args
def describe(**kwargs):
    for key, value in kwargs.items():
        print(f"{key} : {value}")

describe(name="Ankit", age=20, mobile= "9828929839283") # name: Ankit\nage:20\mobile: "923982398"

"""
Module and Imports: Modules are file with Python src. Use import to bring them in. 
Standard Library includes mats, os etc. 
"""

import math
print(math.sqrt(81)) # 9.0

# Alias
import random as rnd
print(rnd.randint(1,10)) # Random int between 1-10

# from import
from datetime import  datetime
print(datetime.now()) # Current date-time

"""
Python core also includes concepts like immutability (e.g. String can't be changed in place),
Garbage Collection (automatic memory management), and dynamic typing. 
"""

"""
OOPs (Object-Oriented Programming)
OOP in Python revolves around classes and objects. key principles: Encapsulation (Hiding Data)
Inheritance (Reusing src), Polymorphism (Same interface, different implementation), and Abstraction (Hiding complexity) 

Classes and Objects: A class is a blueprint; an object is an instance of class
"""

class Dog: # class Definition
    def __init__(self,name: str,age: int ):
        self.name = name
        self.age = age

    def bark(self) -> str:
        return f"{self.name} is {self.age} years old"

# Object creation
my_dog = Dog("Dog",2)
print(my_dog.bark())

# Encapsulation: Use _ (Protected) or __ (private) for attributes. Properties for getters/setters.

class Person:
    def __init__(self, name: str, age: int):
        self._name = name # Protected
        self.__age = age # private (name mangled to _Person__age

    @property
    def age(self) -> int:
        return self.__age

    @age.setter
    def age(self, age: int):
        if age > 0:
            self.__age = age

person = Person("John", 18)
print(person.age) # Gets via getter
person.age = 27 # Sets via setter
print(person.age)

# Inheritance : Subclass inherits from superclass. Supports multiple inheritance

class Animal:
    def eat(self):
        return "Eating"

class Cat(Animal):
    def meaw(self):
        return "Meaw"

my_cat = Cat()

print(my_cat.eat()) # eat() Inherited from Animal Supper class
print(my_cat.meaw()) # Cat class has their own function

# Polymorphism: Methods with same name behave differently

class Bird(Animal):
    def eat(self): # Override from Animal class
        return "Peaking food"

animals = [Cat(), Bird()]
for animal in animals:
    print(animal.eat())


# Abstraction: Use abstract classes ABC from abc module

from abc import ABC, abstractmethod

class Shape(ABC):

    @abstractmethod
    def area(self):
        # Force to implement subclass implementation
        pass

class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self):
        return math.pi * self.radius * self.radius # pi radius square
        # return math.pi * self.radius ** 2

circle = Circle(5)
print(circle.area())

# shape = Shape() # TypeError: Can't instantiate abstract class


class Vechile(ABC): # Abstract base class

    def __init__(self, brand, wheels):
        self._brand = brand # Encapsulation: protected
        self.__wheels = wheels # Private: name-mangled to _Vechile__wheels

    @abstractmethod
    def start(self): # Must be implemented by subclass
        pass

    def __str__(self): # Polymorphism: custom string rep
        return f"{self._brand} with {self.__wheels} wheels"

class Car(Vechile):
    def __init__(self, brand, wheels, doors=4):
        super().__init__(brand, 4) # Call parent init
        self.doors = doors

    def start(self): # Polymorphism: override abstract method
        return f"{self._brand} with car engine roars to life"

    def __add__(self, other): # Operator overload
        if isinstance(other, Car):
            return f"Combined fleet: {self._brand} + {other._brand}"
        return "Invalid addition"

class Bike(Vechile):
    def start(self):
        return f"Bike {self._brand} pedals away"

# Usage
car = Car("Safari")
bike = Bike("TVS Jupiter")

print(car) # Uses __str__
print(bike.start()) # Polymorphism
print(car.start())

# Inheritance check
print(isinstance(car, Vechile))
print(isinstance(bike, Vechile))

# Operator overload
print(car+Car("BMW")) # Combined fleet: Safari + BMW

# Encapsulation access (Conventionally avoided)
print(car.__wheels) # AttributeError (name-mangled)
print(car._Vechile__wheels) # 4 (but don't do this)

"""
Decorator: Decorators are functions that modify the behavior of other functions or 
classes without changing their src. They use @ syntax and are higher-order functions (take/return functions).
"""

# Basic Decorator

import time
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Execution time: {end - start}")
        return result
    return wrapper

@timer
def slow_add(*args):
    time.sleep(1)
    return sum(args)

print(slow_add(4,6))

import functools
import time
import logging

logging.basicConfig(level=logging.INFO)

def timer_logger(func):
    @functools.wraps(func)  # Preserves func.__name__, docstring
    def wrapper(*args, **kwargs):
        start = time.time()
        logging.info(f"Starting {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        end = time.time()
        logging.info(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timer_logger  # Decorator application
def factorial(n):
    """Compute factorial of n."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# Class decorator example: Add a method to a class
def add_method(cls):
    def new_method(self):
        return f"Added method for {cls.__name__}"
    cls.extra_method = new_method
    return cls

@add_method
class MyClass:
    pass

# Usage
print(factorial(5))
obj = MyClass()
print(obj.extra_method())

# Inspect: Decorator preserved metadata
print(factorial.__name__)  # 'factorial' (thanks to wraps)
print(factorial.__doc__)   # 'Compute factorial of n.'


# Decorator with Arguments: Use a nested decorator

def repeat(n: int): # Decorator factory
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def say_hello(name):
    print(f"Hello, {name}")

say_hello("John") # Prints Hello John three times

# class Decorator : Decorators can modify classes

def add_method(cls): # Class Decorator
    def hello(self):
        return "Hello from added method"
    cls.hello = hello
    return cls

@add_method
class MyClass:
    pass

obj = MyClass()
print(obj.hello())

# Decorators are used in framework like Flask/Fast API for routing, authentication, logging etc.

"""
List Comprehension: List comprehension provide a concise way to create lists from iterables, 
often with conditions or transformations. Syntax: [expression for item in iterable if condition]. 

List comprehensions are concise ways to create lists via for loops in one line. Syntax: [expr for item in iterable if condition]. They support nested loops, dict/set comprehensions too. More efficient than loops due to optimized bytecode.
Depth: Compare performance, handle side effects carefully (e.g., no prints inside).

List comps reduce src while improving readability/speed, but avoid complex logic inside.
"""

# Basic
# Without comprehension
squares: list[int] = []

for i in range(5):
    squares.append(i**2)

# With Comprehension
squares = [i ** 2 for i in range(5)] # same result

# With Condition

evens = [i ** 2 for i in range(1, 11) if i % 2 == 0]

print(squares)
print(evens)

# Nested

matrix = [[1, 2], [3, 4]]

flat = [num for row in matrix for num in row] # [1, 2, 3, 4]

# Dict ans Set Comprehensions

my_dict = {x: x**2 for x in range(5)}

my_set = {x for x in 'abcabc'}

# They are faster and more readable than loops but can be less efficient for very large data due to memory usage

# Basic
squares = [x**2 for x in range(10)]  # [0,1,4,9,16,25,36,49,64,81]

# With condition
evens_squared = [x**2 for x in range(10) if x % 2 == 0]  # [0,4,16,36,64]

# Nested
matrix = [[i*j for j in range(3)] for i in range(3)]
# [[0,0,0], [0,1,2], [0,2,4]]

# Dict comprehension
word_lengths = {word: len(word) for word in ["python", "oop", "decorator"] if len(word) > 3}
# {'python': 6, 'decorator': 9}

# Set comprehension
unique_squares = {x**2 for x in [1,1,2,3,3]}  # {1,4,9}

# Generator expression (lazy version, similar but in () )
gen_squares = (x**2 for x in range(10))  # Use with sum(gen_squares)

# Performance comparison (hypothetical, but comprehensions are faster)
import time
start = time.time()
loop_list = []
for x in range(1000000):
    loop_list.append(x**2)
print(f"Loop: {time.time() - start:.4f}s")

start = time.time()
comp_list = [x**2 for x in range(1000000)]
print(f"Comp: {time.time() - start:.4f}s")  # Typically faster


"""
MRO (Method Resolution Order): MRO determines the order in which base classes are searched for a method
in multiple inheritance. Python uses C3 Linearization algorithm (since 2.3) to compute it. View with 
Class.__mro__ or inspect.getmro().

MRO defines the order Python searches classes for methods/attributes during inheritance, especially in multiple inheritance (MI). Python uses C3 linearization: Depth-first, left-to-right, monotonic (no duplicates, respects order).
View via ClassName.__mro__ or ClassName.mro(). Crucial for diamond inheritance problems.
Example: Diamond inheritance with MI.
"""
class A:
    def method(self):
        return "A"

class B(A):
    def method(self):  # Overrides A
        return "B"

class C(A):
    pass  # Inherits A's method

class D(B, C):  # MI: B then C
    pass

d = D()
print(d.method())  # "B" (searches D -> B -> C -> A)

print(D.__mro__)  # (<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)

# Diamond: If D had no method, it would go B -> A (via B), skipping C's path to A to avoid duplicates
class E(B, C):  # Same as D
    pass

# To force order, adjust super() calls, but MRO is fixed at class def time


class A:
    def method(self):
        print("A")

class B(A):
    def method(self):
        print("B")

class C(A):
    def method(self):
        print("C")

class D(B, C): # Multiple inheritance
    pass

d = D()
d.method() # B (searches D -> B -> C -> A)

print(D.__mro__) #(<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)

"""
if there's a diamond problem (Common ancestor), C3 ensures consistent order. Invalid if cycles or inconsistent hierarchies.
"""

class X: pass
class Y: pass
class Z: pass

class A(X, Y): pass
class B(Y, Z): pass
class M(A,B,Z): pass # MRO:

print(M.__mro__) # (<class '__main__.M'>, <class '__main__.A'>, <class '__main__.X'>, <class '__main__.B'>, <class '__main__.Y'>, <class '__main__.Z'>, <class 'object'>)

# MRO Prevents ambiguity in method calls.

"""
Generator: Generators are functions that yield values one at a time, pausing exception between yields. They use yield instead of return, 
creating iterators lazily ( memory-efficient) for large data. 

Generators yield values lazily (on-demand), saving memory vs. lists. Defined with yield in functions or (expr for ...) expressions. Support send(), close(), state via itertools.
Depth: Custom iterable, coroutines basics.
"""

# Basic Generator

def count_up_to(n):
    i = 1
    while i <= n:
        yield i
        i += 1

gen = count_up_to(5)

print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))

# Generator Expression Like list comp, but with () for lazy eval.

gen_expr = (x**2 for x in range(5)) # Generator object
for square in gen_expr: print(square)

# with yield from: For delegating to sub-generators

def sub_gen():
    yield 1
    yield 2

def main_gen():
    yield from sub_gen() # yield 1, 2
    yield 3

for val in main_gen():
    print(val)

# Generators are used in async src, data pipelines. They save memory vs lists (e.g., for infinite sequences).

# Generator function
def fibonacci(limit):
    a, b = 0, 1
    while a < limit:
        yield a  # Pauses here, resumes next call
        a, b = b, a + b

fib_gen = fibonacci(100)
print(list(fib_gen))  # [0,1,1,2,3,5,8,13,21,34,55,89] (consumes gen)

# Generator expression
squares_gen = (x**2 for x in range(10))
print(sum(squares_gen))  # 285 (lazy, no full list in mem)

# Advanced: Generator with send (coroutine-like)
def echo_generator():
    while True:
        received = yield  # First next() yields None, then send values
        yield f"Echo: {received}"

gen = echo_generator()
print(next(gen))  # None (prime it)
gen.send("Hello")  # Yields 'Echo: Hello'
print(next(gen))   # 'Echo: Hello' (next after send)

# Infinite generator, but close it
def infinite():
    n = 0
    while True:
        yield n
        n += 1

inf_gen = infinite()
print(next(inf_gen))  # 0
inf_gen.close()  # Stops iteration