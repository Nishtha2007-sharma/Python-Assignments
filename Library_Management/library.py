# library.py
import json
from pathlib import Path
from book import Book
import logging


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

class Library:
    def __init__(self, storage_path="catalog.json"):
        self.storage_path = Path(storage_path)
        self.books = []
        self.load_from_file()

    def add_book(self, book):
        if self.find_by_isbn(book.isbn):
            logging.error("Attempted to add duplicate ISBN.")
            raise ValueError("A book with this ISBN already exists.")
        self.books.append(book)
        logging.info(f"Book added: {book.title}")
        self.save_to_file()

    def display_all_books(self):
        if not self.books:
            print("No books found.")
            return
        for book in self.books:
            print(book)

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
            logging.error("Issue attempt on non-existent book.")
            raise LookupError("Book not found.")
        if book.status == "Issued":
            logging.error("Issue attempt on already issued book.")
            raise RuntimeError("Book already issued.")
        book.update_status("Issued")
        logging.info(f"Book issued: {book.title}")
        self.save_to_file()
        return book

    def return_book(self, isbn):
        book = self.find_by_isbn(isbn)
        if not book:
            logging.error("Return attempt on non-existent book.")
            raise LookupError("Book not found.")
        if book.status == "Available":
            logging.error("Return attempt on book not issued.")
            raise RuntimeError("Book is not issued.")
        book.update_status("Available")
        logging.info(f"Book returned: {book.title}")
        self.save_to_file()
        return book

    def save_to_file(self):
        data = []
        for book in self.books:
            data.append({
                "title": book.title,
                "author": book.author,
                "isbn": book.isbn,
                "status": book.status
            })
        try:
            self.storage_path.write_text(json.dumps(data, indent=2))
            logging.info("Catalog saved successfully.")
        except Exception as e:
            logging.error(f"Error saving file: {e}")

    def load_from_file(self):
        if not self.storage_path.exists():
            logging.warning("Catalog file missing. Starting with empty library.")
            self.books = []
            return
        try:
            content = self.storage_path.read_text()
            data = json.loads(content)
            self.books = [Book(item["title"], item["author"], item["isbn"], item["status"]) for item in data]
            logging.info("Catalog loaded successfully.")
        except Exception as e:
            logging.error("Catalog corrupted. Starting fresh.")
            print("File corrupted. Loading empty library.")
            self.books = []
