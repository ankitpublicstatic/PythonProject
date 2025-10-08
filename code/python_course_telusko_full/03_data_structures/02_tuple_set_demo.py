# Tuple (immutable) and Set (unique, unordered)
fruits=("apple","banana","cherry")
print("Tuple:", fruits)
print("First:", fruits[0])

nums={1,2,3,3,4,5}
print("Set:", nums)
nums.add(6)
nums.discard(2)
print("Updated Set:", nums)

evens={2,4,6,8}
odds={1,3,5,7}
print("Union:", evens|odds)
print("Intersection:", evens&nums)
print("Difference:", evens-nums)
