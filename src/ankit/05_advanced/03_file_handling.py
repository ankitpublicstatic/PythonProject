
# File handling demo

def main():
    filename = "sample.txt"

    # Write to file
    with open(filename, "w") as f:
        f.write("Hello, this is a test file.\n")
        f.write("Python makes file handling easy!\n")

    # Read from file
    with open(filename, "r") as f:
        print("File contents:")
        for line in f:
            print(line.strip())

if __name__ == "__main__":
    main()