# File handling demo
with open("sample.txt","w") as f:
    f.write("Hello\nPython\n")
with open("sample.txt","r") as f:
    for line in f: print(line.strip())
