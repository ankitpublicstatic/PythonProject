from abc import ABC, abstractmethod

# Abstract Base Class
class Book(ABC):

    def __init__(self, title: str, author: str):
        self.title = title
        self.author = author
        self.is_borrowed = False

    @abstractmethod
    def borrow(self):
        """Abstract method: Must be implemented by subclasses"""
        pass

    def return_book(self) -> str:
        if self.is_borrowed:
            self.is_borrowed = False
            return f"'{self.title}' has been returned."
        return f"'{self.title}' was not borrowed."

    def __str__(self):
        status = "Borrowed" if self.is_borrowed else "Available"
        return f"{self.title} - {self.author} - [{status}]"


# Subclass 1:EBook
class EBook(Book):

    def __init__(self, title: str, author: str, file_size: float, file_format: str):
        super().__init__(title, author)
        self.file_size = file_size
        self.file_format = file_format

    def borrow(self):
        if not self.is_borrowed:
            self.is_borrowed = True
            return f"📱 E-Book '{self.title}' downloaded ({self.file_size}MB, {self.file_format})."
        return f"Sorry, e-book '{self.title}' already borrowed."

    def __str__(self):
        status = "Borrowed" if self.is_borrowed else "Available"
        return f"E-Book: {self.title} by {self.author}, {self.file_size}MB [{status}]"


# Subclass 2: PrintedBook
class PrintedBook(Book):
    def __init__(self, title: str, author: str, pages: int, weight: float):
        super().__init__(title, author)
        self.pages = pages
        self.weight = weight

    def borrow(self):
        if not self.is_borrowed:
            self.is_borrowed = True
            return f"📖 Printed book '{self.title}' issued (Pages: {self.pages}, Weight: {self.weight}kg)."
        return f"Sorry, printed book '{self.title}' already borrowed."

    def __str__(self):
        status = "Borrowed" if self.is_borrowed else "Available"
        return f"PrintedBook: {self.title} by {self.author}, {self.pages} pages [{status}]"

# Library Class (Composition relation Has-a-relation)

class Library:
    def __init__(self, name: str):
        self.name = name
        self.books: list[Book] = []

    def add_book(self, book: Book) -> str:
        self.books.append(book)
        return f"Book '{book.title}' added to library '{self.name}'."

    def show_books(self):
        if not self.books:
            return "No books in library."
        return "\n".join( str(book) for book in self.books)


    def show_borrowed_books(self):
        if not self.books:
            return "No books in library."
        return "\n".join( str(book) for book in self.books if book.is_borrowed)


    def show_available_books(self):
        if not self.books:
            return "No books in library."
        return "\n".join( str(book) for book in self.books if not book.is_borrowed)

    def find_books(self, title: str):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def borrow_book(self, title: str):
        book = self.find_books(title)
        if book:
            return book.borrow()
        return f"Book '{title}' not found in library."

    def return_book(self, title: str):
        book = self.find_books(title)
        if book:
            return book.return_book()
        return f"Book '{title}' not found in library."

# -------------------
# DEMO
# -------------------
my_library = Library("National Library")

print(my_library.add_book(EBook("Python Tricks", "Dan Bader", 4.5, "PDF")))
print(my_library.add_book(PrintedBook("Mahabharata", "Vyasa", 1200, 2.5)))

print("\n📚 All Books:")
print(my_library.show_books())

print("\n🔑 Borrowing Books:")
print(my_library.borrow_book("Python Tricks"))
print(my_library.borrow_book("Mahabharata"))

print("\n📚 Books after borrowing:")
print(my_library.show_books())

print("\n🔙 Returning Books:")
print(my_library.return_book("Python Tricks"))

print("\n📚 Final Books:")
print(my_library.show_books())

"""

Abstract Class (Book):

Cannot be instantiated directly (Book("x","y") → ❌).

Forces subclasses (EBook, PrintedBook) to implement borrow().

Polymorphism:

Library calls book.borrow() without knowing type.

Each subclass provides its own implementation.

self in action:

Each object (EBook, PrintedBook) maintains its own independent state (is_borrowed, file_size, pages, etc.).

"""