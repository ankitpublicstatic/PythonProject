# Operators demo
def main():
    x = 15; y = 4
    print("x",x, "y", y)
    print("x + y =", x+y)
    print("x - y =", x-y)
    print("x * y =", x*y)
    print("x / y =", x/y)
    print("x // y =", x//y)
    print("x % y =", x%y)
    print("x ** y =", x**y)
if __name__ == "__main__":
    main()
"""
With x = 15 and y = 4, the first print statement outputs x // y = 3 since floor division (//) computes 15 / 4 = 3.75 and rounds down to the nearest integer toward negative infinity. The second print statement outputs x ** y = 50625 because exponentiation (**) raises 15 to the power of 4 (15^4 = 15 * 15 * 15 * 15).

Outputs Explained
Floor division result: 15 // 4 yields 3, as it truncates the decimal part of 3.75 (unlike regular division / which gives 3.75).

Exponentiation result: 15 ** 4 equals 50625, a standard power operation in Python.

Full Code Execution
text
x // y = 3
x ** y = 50625
"""