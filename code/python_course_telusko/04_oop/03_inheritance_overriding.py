# Inheritance and overriding
class Animal:
    def speak(self): print("Animal speaks")
class Dog(Animal):
    def speak(self): print("Dog barks")
class Cat(Animal):
    def speak(self): print("Cat meows")
for a in [Dog(),Cat(),Animal()]:
    a.speak()
