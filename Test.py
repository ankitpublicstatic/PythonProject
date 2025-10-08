nums = [3,4,2,5] # List Array
names = ['ankit','vaishnavi','ram']

mil = [nums,names]
#print(mil[0:2])

nums.append(33)
print(nums)

tuple = (21,3,2,3,4) # immutable list of data.
print( tuple.count)

set = {1,2,3,4,5} # unique object store in set collection, using hash to improve the performance. not maintaining the order and sequence.

id(tuple) # will fetch address of the variable.

""" 
None = null
Numeric = int:2, float : 2.5, complex : 6+9j, bool : True, False

Sequence: Collection of Data
List : []
Tuple : ()
Set : {}
String : ""
Range : range(10)

list(range(10))
list(range(2,10,2))

Map:
Dictionary : d = {'ram':"iPhone",'rahul':"Samsung"}
print(d) 
d['rahul'] # for fetch the value from dictionary
d['ram'] # for fetch the value from dictionary
d.get('rahul') # for fetch the value from dictionary


num = int(input("Enter a number : "))
result = eval(input("Enter an expression: "))
print(result)
print(type(result))
print(num)

import sys

x = int(sys.argv[1])
y = int(sys.argv[2])
print(x+y)
"""
i = 1

while i <= 5:
    print("Ankit ",end="")
    j = 1
    while j <= 4:
        print("Rock ",end="")
        j +=1
    i += 1
    print()