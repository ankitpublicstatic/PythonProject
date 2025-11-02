
# Number system conversion demo

def main():
    num = 10
    print("Decimal:", num)
    print("Binary:", bin(num))
    print("Octal:", oct(num))
    print("Hexadecimal:", hex(num))

    # Converting string to int with base
    print("Binary string '1010' ->", int("1010", 2))
    print("Hex string 'A' ->", int("A", 16))


if __name__ == "__main__":
    main()