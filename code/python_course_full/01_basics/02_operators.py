# Operators demo
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
