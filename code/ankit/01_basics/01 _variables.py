
# Variables in Python
# Demonstrates different types of variables and reassignment.

def main():
    a = 10  # integer
    b = 3.14  # float
    c = "Telusko"  # string

    print("a =", a, type(a))
    print("b =", b, type(b))
    print("c =", c, type(c))

    # Reassigning variable
    a = "Now I'm a string"
    print("a =", a, type(a))


if __name__ == "__main__":
    main()