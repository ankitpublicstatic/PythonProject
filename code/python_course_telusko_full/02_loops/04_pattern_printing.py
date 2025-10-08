# Pattern printing demo
n=5
print("Right triangle:")
for i in range(1,n+1):
    print("*"*i)

print("Inverted triangle:")
for i in range(n,0,-1):
    print("*"*i)

print("Pyramid pattern:")
for i in range(1,n+1):
    print(" "*(n-i) + "*"*(2*i-1))
