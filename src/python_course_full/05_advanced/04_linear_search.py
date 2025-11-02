# Linear search demo
arr=[5,3,8,6,7]
target=6
index=-1
for i,v in enumerate(arr):
    if v==target:
        index=i
        break
print("Found at index:",index if index!=-1 else "Not found")
