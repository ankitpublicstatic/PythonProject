
# Method overloading in Python
# Python does not support true overloading,
# but we can use default arguments to simulate it.

class Calculator:
    def add(self, a, b=0, c=0):
        return a + b + c

def main():
    calc = Calculator()
    print("Add two numbers:", calc.add(5, 10))
    print("Add three numbers:", calc.add(5, 10, 15))
    print("Add one number:", calc.add(7))

if __name__ == "__main__":
    main()