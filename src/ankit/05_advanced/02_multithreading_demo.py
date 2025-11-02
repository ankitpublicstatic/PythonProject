
# Multithreading demo
import threading
import time

def print_numbers():
    for i in range(1, 6):
        print("Number:", i)
        time.sleep(1)

def print_letters():
    for c in "ABCDE":
        print("Letter:", c)
        time.sleep(1)

def main():
    t1 = threading.Thread(target=print_numbers)
    t2 = threading.Thread(target=print_letters)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("Both threads finished.")

if __name__ == "__main__":
    main()