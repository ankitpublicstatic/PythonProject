# Multithreading demo
import threading, time
def numbers():
    for i in range(1,6): print(i); time.sleep(1)
def letters():
    for c in "ABCDE": print(c); time.sleep(1)
t1=threading.Thread(target=numbers)
t2=threading.Thread(target=letters)
t1.start(); t2.start()
t1.join(); t2.join()
