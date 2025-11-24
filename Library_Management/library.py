from book import Book
import os

class Library:
    def __init__(self, storage_path="library.txt"):
        self.storage_path = storage_path
        self.books = []
        self.load_from_file()

    def add_book(self, book):
        if self.find_by_isbn(book.isbn):
            raise ValueError("A book with this ISBN already exists.")
        self.books.append(book)

    def display_all_books(self):
        if not self.books:
            print("No books in library.")
            return
        for i, book in enumerate(self.books, start=1):
            print(f"{i}. {book}")

    def find_by_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def search_by_title(self, query):
        query = query.lower()
        return [b for b in self.books if query in b.title.lower()]

    def issue_book(self, isbn):
        book = self.find_by_isbn(isbn)
        if not book:
            raise LookupError("Book not found.")
        if book.status == "Issued":
            raise RuntimeError("Book is already issued.")
        book.update_status("Issued")
        self.save_to_file()
        return book

    def return_book(self, isbn):
        book = self.find_by_isbn(isbn)
        if not book:
            raise LookupError("Book not found.")
        if book.status == "Available":
            raise RuntimeError("Book is not issued.")
        book.update_status("Available")
        self.save_to_file()
        return book

    def save_to_file(self):
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                for book in self.books:
                    f.write(book.to_record() + "\n")
        except Exception as e:
            print("Error saving to file:", e)

    def load_from_file(self):
        if not os.path.exists(self.storage_path):
            self.books = []
            return
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            self.books = []
            for line in lines:
                book = Book.from_record(line)
                if book:
                    self.books.append(book)
        except Exception as e:
            print("Error loading file (file might be corrupted). Starting with empty library.")
            print("Details:", e)
            self.books = []
