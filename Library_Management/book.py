class Book:
    def __init__(self, title, author, isbn, status="Available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def display_details(self):
        print(f"Title : {self.title}")
        print(f"Author: {self.author}")
        print(f"ISBN  : {self.isbn}")
        print(f"Status: {self.status}")

    def update_status(self, new_status):
        self.status = new_status

    def to_record(self):
        return f"{self.title},{self.author},{self.isbn},{self.status}"

    @staticmethod
    def from_record(line):
        parts = line.strip().split(",")
        if len(parts) < 4:
            return None
        title, author, isbn, status = parts[0], parts[1], parts[2], parts[3]
        return Book(title, author, isbn, status)

    def __str__(self):
        return f'"{self.title}" by {self.author} (ISBN: {self.isbn}) - {self.status}'
