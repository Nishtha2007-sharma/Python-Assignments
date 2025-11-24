from library import Library
from book import Book

def input_nonempty(prompt):
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Please enter a value.")

def main():
    lib = Library()  

    menu = """
Library Menu
1. Add Book
2. View All Books
3. Search by Title
4. Search by ISBN
5. Issue Book
6. Return Book
7. Save and Exit
"""

    while True:
        print(menu)
        choice = input("Enter choice [1-7]: ").strip()

        if choice == "1":
            title = input_nonempty("Title: ")
            author = input_nonempty("Author: ")
            isbn = input_nonempty("ISBN: ")
            try:
                lib.add_book(Book(title, author, isbn))
                print("Book added successfully.")
            except Exception as e:
                print("Error:", e)

        elif choice == "2":
            lib.display_all_books()

        elif choice == "3":
            q = input_nonempty("Enter title search: ")
            results = lib.search_by_title(q)
            if not results:
                print("No matches.")
            else:
                for b in results:
                    print(b)

        elif choice == "4":
            isbn = input_nonempty("Enter ISBN to search: ")
            b = lib.find_by_isbn(isbn)
            if not b:
                print("Book not found.")
            else:
                b.display_details()

        elif choice == "5":
            isbn = input_nonempty("ISBN to issue: ")
            try:
                book = lib.issue_book(isbn)
                print("Issued:", book)
            except Exception as e:
                print("Error:", e)

        elif choice == "6":
            isbn = input_nonempty("ISBN to return: ")
            try:
                book = lib.return_book(isbn)
                print("Returned:", lib.find_by_isbn(isbn))
            except Exception as e:
                print("Error:", e)

        elif choice == "7":
            lib.save_to_file()
            print("Library saved to file. Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
