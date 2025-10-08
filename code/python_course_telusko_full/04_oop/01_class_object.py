"""

# Classes and objects
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


class Person:
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello {self.name} and I am {self.age} years old"


# Creating objects (instance of Person class)

person1 = Person("ankit", 26)
person2 = Person("ram", 26)

print(person1.greet())
print(person2.greet())



class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1
        return self.count

counter = Counter()
counter2 = Counter()

print(counter.increment())
print(counter2.increment())
print(counter2.increment())


class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance # private attribute (name mangling)

    def deposit(self, amount):
        self.__balance += amount
        return self.__balance

    def withdraw(self, amount):
        if amount <= self.__balance:
            self.__balance -= amount
            return self.__balance
        else:
            print("You don't have enough money!")
            raise Exception("Not enough money")

account_1 = BankAccount("ankit", 100)
print(account_1.deposit(100))
print(account_1.withdraw(50))
# print(
#     account_1.__balance
# )



class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound"

class Dog(Animal):
    def speak(self):
        return f"{self.name} barks"

class Cat(Animal):
    def eat(self):
        return f"{self.name} eat"
    # def speak(self):
    #     return f"{self.name} meows"

dog = Dog("Tommy")
cat = Cat("Kitty")
print(dog.speak())
print(cat.speak())




def lowercase_decorator(func):
    def wrapper(*args, **kwargs):
        return "hello ankit".lower()
    return wrapper

@lowercase_dacorator
def greet():
    return "Hello greet"

print(greet())
print(greet().upper())

"""

class Student:
    school_name = "GLS University" # class variable (shared by all objects

    def __init__(self, name):
        self.name = name # instance variable (Unique per object

student1 = Student("James")
student2 = Student("ankit")

print(student1.name, student1.school_name)
print(student2.name, student2.school_name)

# If we change school_name using className

Student.school_name = "AKS University"
print(student1.school_name)
print(student2.school_name)

# Deep Insight on self
#
# When you define a method inside a class, you must explicitly declare self as the first parameter.
#
# But when calling the method via an object, Python automatically passes the instance → so you don’t pass it manually.
#
# Without self, methods cannot access instance variables.