
# List demo
# Lists are mutable, ordered collections of items

def main():
    numbers = [10, 20, 30, 40, 50]
    print("Original list:", numbers)

    # Access
    print("First element:", numbers[0])
    print("Last element:", numbers[-1])

    # Modify
    numbers[2] = 35
    print("After modification:", numbers)

    # Add
    numbers.append(60)
    numbers.insert(1, 15)
    print("After append and insert:", numbers)

    # Remove
    numbers.remove(40)
    popped = numbers.pop()
    print("After remove and pop:", numbers, "| popped:", popped)

    # Iterate
    print("Iterating over list:")
    for num in numbers:
        print(num)

if __name__ == "__main__":
    main()