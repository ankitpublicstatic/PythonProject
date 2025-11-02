
# Tuple and Set demo
# Tuple = immutable ordered collection
# Set = unordered unique elements

def main():
    # Tuple
    fruits = ("apple", "banana", "cherry")
    print("Tuple:", fruits)
    print("First fruit:", fruits[0])
    # fruits[1] = "mango"  # ERROR: tuples are immutable

    # Set
    nums = {1, 2, 3, 3, 4, 5}
    print("\nSet (duplicates removed):", nums)

    nums.add(6)
    nums.discard(2)
    print("After add and discard:", nums)

    # Set operations
    evens = {2, 4, 6, 8}
    odds = {1, 3, 5, 7}
    print("Union:", evens | odds)
    print("Intersection:", evens & nums)
    print("Difference:", evens - nums)

if __name__ == "__main__":
    main()