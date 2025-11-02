# List demo
numbers=[10,20,30,40,50]
numbers[2]=35
numbers.append(60)
numbers.insert(1,15)
numbers.remove(40)
popped = numbers.pop()

print("Updated list:", numbers)
print("Popped value:", popped)

for num in numbers:
    print(num)
