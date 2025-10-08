
# Pattern printing demo
# Prints different star patterns using loops

def main():
    n = 5

    print("Right triangle pattern:")
    for i in range(1, n + 1):
        print("*" * i)

    print("\nInverted triangle pattern:")
    for i in range(n, 0, -1):
        print("*" * i)

    print("\nPyramid pattern:")
    for i in range(1, n + 1):
        print(" " * (n - i) + "*" * (2 * i - 1))

if __name__ == "__main__":
    main()