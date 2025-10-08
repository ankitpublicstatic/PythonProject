
# break, continue, pass demo

def main():
    print("Using break:")
    for i in range(1, 10):
        if i == 5:
            break
        print(i)

    print("\nUsing continue:")
    for i in range(1, 10):
        if i % 2 == 0:
            continue
        print(i)

    print("\nUsing pass:")
    for i in range(5):
        if i == 3:
            pass  # Placeholder, does nothing
        print("i =", i)

if __name__ == "__main__":
    main()