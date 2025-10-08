
# Linear search demo

def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

def main():
    arr = [5, 3, 8, 6, 7]
    target = 6
    result = linear_search(arr, target)
    if result != -1:
        print(f"Element {target} found at index {result}")
    else:
        print(f"Element {target} not found")

if __name__ == "__main__":
    main()