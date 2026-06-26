import numpy
import numpy as np

"""
a = np.zeros((10,10), dtype=np.float64)
a = np.arange(1,101)
a = a.reshape(10,10)
a = np.identity(3)

# 1. numpy defines several functions to perform complex mathematical operations.
# 2. to fulfill performance gaps 
    most fo the numpy is implemented in C language 
    superfast
# 3. nd array 
    -----> n dimensional array or numpy array
    numpy acts as backbone for remaining libraries also. 
    
History of Numpy:
=====================
Origin of Numpy ----> Numeric Library 
Numeric Library ====> Jim Hugunin
Numpy --------> Travis Oliphant & Other Contributors 2005
Open Source Library and Freeware

Q. In which languages Numpy was written?
C and Python

Q. What is nd array in numpy?
 The Fundamental data type to store our data: nd array
 arrays are objects of ndarray class present in numpy module. 
 
 Array: an indexed collection of homogeneous elements
 1 dimensional array -----> Vector
 2 dimensional array -----> Matrix
 3 dimensional array -----> Qube
 ..
 n dimensional array
 
 Application areas of Numpy?
 AI,ML,DL,DS
 
Array Creation: 10 ways
Attributes
How to access elements of array
    Basic Indexing
    Slice Operation
    Advanced Indexing
    Condition Based Selection
    
How to iterate elements of array:
    python's normal loops
    nditer()
    ndenumerate()
    
Arithmetic operators
    +
    -
    *
    /
    %
Broadcasting
Array Manipulation functions
    reshape()
    resize()
    flatten()
    ravel()
    transpose()
    
Matrix class

Linear Algebra Problem solving

x+y = 2200
3x+8y = 10100

coefficient matrix
a = [1,1
     3, 8 ] 
     
a = np.array([[1,1],[3,8]]


value matrix
     
b = [2200, 10100]

b = np.array([2200, 10100])

result = numpy.linalg.solve(a,b)

data type in python: list, tuple, set, dict etc












a = np.ones((2,3))

# one_d_array = np.ones((10,))
# print(one_d_array)
a = np.arange(1,21)

a = a[a%6==0] # Condition Based Selection
a = numpy.array([[1,1],[3,8]])
b = numpy.array( [2200,10100])
a = numpy.linalg.solve(a,b)

a = [10, 20, 30]
b = [1, 2, 3]
c = [7,8,9,10]
for i, j, k in zip(a, b, c):
    print(i, j, k)


a = np.array([10,20,30])
b = np.array([1,2,3])

# dot product: A.B = 10x1 + 20 x 2 + 30 x 3 = 140
def dot_product(a, b):
    result = 0
    for i, j in zip(a, b):
        result += i * j
    return result

print(dot_product(a,b))

from datetime import datetime

before = datetime.now()
for i in range(1000000):
    dot_product(a,b)

after = datetime.now()
print('Time taken by traditional python:',after - before)

# Numpy library code
before = datetime.now()
for i in range(1000000):
    numpy.dot(a,b) # this is from numpy

after = datetime.now()
print('Time taken by numpy Library:',after - before)



 Array: an indexed collection of homogeneous elements
 1 dimensional array -----> Vector
 2 dimensional array -----> Matrix
 3 dimensional array -----> Qube
 ..
 n dimensional array
 
 Application areas of Numpy?
 AI,ML,DL,DS
 
Array Creation: 10 ways
How to create arrays in python:
=================================
inbuilt arrays concept is not there in python

2 ways
1. By using array module
2. By using numpy module



import array
a = array.array('i',[1,2,3]) # i is represents types: int array

for x in a:
    print(x)

# Note: array module is not recommended because much library support is not available.

2. numpy module
================

import numpy
a = numpy.array([1,2,3])
print(a)
print(type(a))

for x in a:
    print(x)

Python's List vs numpy ndarray

1. Similarties:
====================
1. Both can be used to store data 
2. The order will preserved in both. Hence indexing and slicing concepts are applicable. 
3. Both are mutalbe, ie we can change the content. 

2. Differences: 
=====================

1. list is python's inbuilt type. we have to install numpy
2. List can contain heterogeneous element, but numpy ndarray contains only homogeneous elements.

3. On list we cannot perform vector operation. but on ndarray we can perform vector, matrix operation. 

4. arrays consume less memory compare to list
print('The size of the array:', sys.getsizeof(a))
print('The size of the list:', sys.getsizeof(l))

5. Arrays are superfast when compared with list. 
6. Numpy arrays are more convent to use while performing complex mathematical operations.

How to Create Numpy Arrays:
=============================
1. numpy.array([1,2,3])
2. numpy.arange(1,101)
3. numpy.linspace(0,1,100)

4. np.zeros([3,3])
5. np.ones([10,10])
6. numpy.full([10,10],7) # full of custom number
7. np.eye()
8. np.identity(3)
9. np.empty((3,3))
10. np.random library
    1. randint()
    2. rand()
    3. uniform()
    4. randn()
    5. normal()
    6. shuffle()

1. Creation of Numpy Array:
l = [20,30,40,50]
a = numpy.array(l)
print(type(a)) # find type of array

print(a.ndim) # find of dimension of ndarray
print(a.shape) # find of shape of ndarray
print(a.dtype) # find of data type of ndarray

Note:
a.dnim----> To know dimension of ndarray
a.dtype---> To know data type of elements

2-D array creation:
[[10,20,30],[40,50,60],[70,80,90]] -----> Nested list
a = numpy.array([[10,20,30],[40,50,60],[70,80,90]])

a.dnim > 2
a.shape > (3,3)
a.size -> 9
a.ndim

a = np.array([1,2,3])
a.shape > (2,)
a.size > 3
a.ndim > 1D


a = np.array(("ankit","ram","sita")

a.ndim > 1D
a.shape > (3,)

Note: array store only homogenous elements.
if tuple having int,float element then np.array() will promote all elements to float element. if string having then all elements will promote to String. 










"""