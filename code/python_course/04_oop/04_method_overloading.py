# Method overloading via default args
class Calc:
    def add(self,a,b=0,c=0):
        return a+b+c
c=Calc()
print(c.add(5))
print(c.add(5,10))
print(c.add(5,10,15))
