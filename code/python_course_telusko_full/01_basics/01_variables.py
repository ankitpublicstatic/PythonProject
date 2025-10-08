# Variables demo
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
