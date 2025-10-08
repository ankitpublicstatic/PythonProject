class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_borrowed = False

    def borrow(self):
        if not self.is_borrowed:
            self.is_borrowed = True
            return f"{self.title} has been borrowed"
        return f"Sorry, '{self.title}' is not available"

    def return_book(self):
        if self.is_borrowed:
            self.is_borrowed = False
            return f"'{self.title}' has been returned"
        return f"'{self.title}' was not borrowed"

    def __str__(self):
        status = "Borrowed" if self.is_borrowed else "Available"
        return f"{self.title} by {self.author}  [{status}]"

"""
class Library:
    def __init__(self,name):
        self.name = name
        self.books = [] # list to store Books objects

    def add_book(self, book):
        self.books.append(book)
        return f"Book '{book.title}' has been added to  {self.name} the library"

    def show_books(self):
        if not self.books:
            return f"No book has been added to {self.name}"
        return "\n".join(str(book) for book in self.books)

    def find_book(self, title):
        for book in self.books:
            if book.title == title:
                return book
        return None

    def borrow_book(self, title):
        book = self.find_book(title)
        if book:
            return book.borrow()
        return f"Book '{title}' not found in library"

    def return_book(self, title):
        book = self.find_book(title)
        if book:
            return book.return_book()
        return f"Book '{title}' not found in library"

my_library = Library("Babhangama City")

print(my_library.add_book(Book("Geeta","Krishna")))
print(my_library.add_book(Book("Ramayan","Mharshi Balmiki")))
print(my_library.add_book(Book("Mahabharat","Mharshi Bedbyas")))

print("\n📚 Available Books:")
print(my_library.show_books())

# Borrow books
print("\n🔑 Borrowing a book:")

print(my_library.borrow_book("Geeta"))
print(my_library.borrow_book("Ramayan"))
print(my_library.borrow_book("Geeta"))


# Show books after borrowing
print("\n📚 Available Books after borrowing:")
print(my_library.show_books())


# Return books
print("\n🔙 Returning a book:")
print(my_library.return_book("Geeta"))
print(my_library.return_book("Ramayan"))


# Final state
print("\n📚 Final List of Books:")
print(my_library.show_books())

"""

# Subclass 1: EBook

class EBook(Book):
    def __init__(self, title: str, author: str, file_size: float, file_format: str ):
        super().__init__(title,author)
        self.file_size = file_size
        self.file_format = file_format

    def borrow(self) -> str:
        if not self.is_borrowed:
            self.is_borrowed = True
            return f"📱 E-Book '{self.title}' downloaded ({self.file_size}MB, {self.file_format})."
        return f"Sorry, e-book '{self.title}' already borrowed."

    def __str__(self):
        status = "Borrowed" if self.is_borrowed else "Available"
        return f"E-Book '{self.title}' by {self.author}, {self.file_size}MB, {self.file_format}  [{status}]"

# Subclass 2: PrintedBook

class PrintedBook(Book):
    def __init__(self, title: str, author: str, pages: int, weight: float):
        super().__init__(title,author)
        self.pages = pages
        self.weight = weight

    def borrow(self) -> str:
        if not self.is_borrowed:
            self.is_borrowed = True
            return f"📖 Printed book '{self.title}' issued (Pages: {self.pages}, Weight: {self.weight}kg)."
        return f"Sorry, printed book '{self.title}' already borrowed."

    def __str__(self):
        status = "Borrowed" if self.is_borrowed else "Available"
        return f"PrintedBook: {self.title} by {self.author}, {self.pages} pages [{status}]"


# Library class

class Library:
    def __init__(self, name: str):
        self.name = name
        self.books: list[Book] = []

    def add_book(self, book: Book):
        self.books.append(book)
        return f"Book '{book.title}' has been added to  {self.name} the library"

    def show_books(self):
        if not self.books:
            return "No books in library"
        return "\n".join( str(book) for book in self.books)

    def find_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def borrow_book(self, title):
        book = self.find_book(title)
        if book:
            return book.borrow()
        return f"Book '{title}' not found in library"

    def return_book(self, title):
        book = self.find_book(title)
        if book:
            return book.return_book()
        return f"Book '{title}' not found in library"


my_library = Library("Babhangama City")
print(my_library.add_book(EBook("Python Crash Course", "Eric Matthes", 5.2, "PDF")))
print(my_library.add_book(PrintedBook("Sherlock Holmes", "Arthur Conan Doyle", 320, 0.7)))
print(my_library.add_book(EBook("Deep Learning", "Ian Goodfellow", 45.0, "EPUB")))
print(my_library.add_book(PrintedBook("Ramayan", "Valmiki", 500, 1.2)))


print("\n📚 All Books in Library:")
print(my_library.show_books())

# Borrow books (notice polymorphism)
print("\n🔑 Borrowing Books:")
print(my_library.borrow_book("Python Crash Course"))
print(my_library.borrow_book("Sherlock Holmes"))
print(my_library.borrow_book("Python Crash Course"))  # already borrowed
print(my_library.borrow_book("Deep Learning"))
print(my_library.borrow_book("Ramayan"))
print(my_library.borrow_book("Ramayan"))

print("\n📚 Books after borrowing:")
print(my_library.show_books())


# Return books
print("\n🔙 Returning a book:")
print(my_library.return_book("Ramayan"))
print(my_library.return_book("Python Crash Course"))
print(my_library.return_book("Deep Learning"))
print(my_library.return_book("Sherlock Holmes"))


print("\n📚 Books after returning:")
print(my_library.show_books())