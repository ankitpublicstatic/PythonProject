python
# Inheritance and method overriding demo

class Animal:
    def speak(self):
        print("Animal speaks")

class Dog(Animal):
    def speak(self):
        print("Dog barks")

class Cat(Animal):
    def speak(self):
        print("Cat meows")

def main():
    animals = [Dog(), Cat(), Animal()]
    for a in animals:
        a.speak()

if __name__ == "__main__":
    main()