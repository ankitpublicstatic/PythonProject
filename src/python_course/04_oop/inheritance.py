class A:
    def __init__(self):
        print('A init working')
    def feature1(self):
        print('Feature 1')

    def feature2(self):
        print('Feature 2')

# Single level inheritance
class B(A):
    def __init__(self):
        super().__init__()
        print('B init working')
    def feature3(self):
        print('Feature 3')
    def feature4(self):
        print('Feature 4')

# Multi level inheritance
class C(B):
    def feature5(self):
        print('Feature 5')

class X:
    def feature6(self):
        print('Feature 6')

# Multiple inheritance
class Y(C,X):

    def __init__(self):
        super().__init__() # It will follow always MRO Method resolution order Left to Right, first It will class C method, then it will call class X methods. 
        print('Y init working')


    def feature7(self):
        print('Feature 7')
# a1 = A()
# a1.feature1()

b1 = B()
b1.feature1()
# c1 = C()
# c1.feature1()
# y1 = Y()
# y1.feature1()