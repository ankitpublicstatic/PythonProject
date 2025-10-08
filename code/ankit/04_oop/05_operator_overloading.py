
# Operator overloading demo
# Using __add__ method to add custom objects

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f"Point({self.x}, {self.y})"

def main():
    p1 = Point(2, 3)
    p2 = Point(4, 5)
    p3 = p1 + p2   # calls __add__
    print(p3)

if __name__ == "__main__":
    main()