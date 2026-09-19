list1 = [8, 9, 44, 3] # mutable, indexable, supporting all predefined method like del, min, max, append(value),
# insert (index, value), .sort, .reverse, .remove(value), .pop(index) with slicing, .index to get index no of value,

tup1 = (89,33,89) # immutable, only count and index, min, max
tup2 = 98,33,22

set1 = set(tup1) # unique unordered collection of value internally using hashing for storing the value
set2 = {98,98,33,43}

set3 = set('abc') #{'b', 'c', 'a'}
set4 = {'abc'}#{'abc'}

dict1 = {'ankit':89, 'ram':40, 'sita':50} # key will unique, duplicate key will override exiting key and value

list3=['js','python','java']
list4=['vscode','pycharm','sts']

c=zip(list3,list4)
# print(type(c))

dict2 = dict(zip(list3,list4))

# print(dict1['no']) # Will return KeyError
# print(dict1.get('no'))
# print(dict2)

r = range(11)
print(r)

print(list(r))

print(list(range(2,11,2)))