
# More on variables and data types
# Demonstrates string, boolean, and type casting

def main():
    name = "Telusko"
    is_active = True
    age = 25

    print("Name:", name)
    print("Active:", is_active)
    print("Age:", age)

    # Type casting
    print("\nCasting examples:")
    age_str = str(age)
    print("Age as string:", age_str, type(age_str))

    num_str = "100"
    num_int = int(num_str)
    print("String '100' to int:", num_int, type(num_int))

if __name__ == "__main__":
    main()