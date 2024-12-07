import mysql.connector
from mysql.connector import Error

# Connect to MySQL Database
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',          # host
            user='root',               # MySQL username
            password='sajan',               #  password
            database='library_management'
        )
        if conn.is_connected():
            print("Connected to MySQL database")
            return conn
        else:
            print("Connection failed")
            return None
    except Error as e:
        print(f"Error: {e}")
        return None

# Add new book to the library
def add_book(conn, title, author, quantity):
    try:
        cursor = conn.cursor()
        query = "INSERT INTO books (title, author, quantity) VALUES (%s, %s, %s)"
        cursor.execute(query, (title, author, quantity))
        conn.commit()
        print(f"Book '{title}' by {author} added successfully!")
    except Error as e:
        print(f"Error: {e}")

# Display all available books
def display_books(conn):
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM books"
        cursor.execute(query)
        books = cursor.fetchall()
        if books:
            print(f"{'ID':<5}{'Title':<30}{'Author':<30}{'Quantity':<10}")
            for book in books:
                print(f"{book[0]:<5}{book[1]:<30}{book[2]:<30}{book[3]:<10}")
        else:
            print("No books available in the library.")
    except Error as e:
        print(f"Error: {e}")

# Issue a book (mark as 'taken')
def issue_book(conn, book_id):
    try:
        cursor = conn.cursor()

        # Check if the book is available
        cursor.execute("SELECT quantity FROM books WHERE book_id = %s", (book_id,))
        result = cursor.fetchone()
        
        if result and result[0] > 0:
            # Decrease quantity of available books
            cursor.execute("UPDATE books SET quantity = quantity - 1 WHERE book_id = %s", (book_id,))
            conn.commit()
            
            # Insert into transactions table
            cursor.execute("INSERT INTO transactions (book_id, transaction_type) VALUES (%s, 'taken')", (book_id,))
            conn.commit()
            print(f"Book with ID {book_id} has been taken successfully!")
        else:
            print(f"Book with ID {book_id} is not available!")
    except Error as e:
        print(f"Error: {e}")

# Return a book (mark as 'returned')
def return_book(conn, book_id):
    try:
        cursor = conn.cursor()

        # Increase quantity of available books
        cursor.execute("UPDATE books SET quantity = quantity + 1 WHERE book_id = %s", (book_id,))
        conn.commit()
        
        # Insert into transactions table
        cursor.execute("INSERT INTO transactions (book_id, transaction_type) VALUES (%s, 'returned')", (book_id,))
        conn.commit()
        print(f"Book with ID {book_id} has been returned successfully!")
    except Error as e:
        print(f"Error: {e}")

# Main menu function
def main():
    conn = connect_to_db()
    if conn is None:
        return
    
    while True:
        print("\nLibrary Management System")
        print("1. Add a new book")
        print("2. Display all books")
        print("3. Issue a book")
        print("4. Return a book")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            quantity = int(input("Enter quantity: "))
            add_book(conn, title, author, quantity)
        
        elif choice == '2':
            display_books(conn)
        
        elif choice == '3':
            book_id = int(input("Enter book ID to issue: "))
            issue_book(conn, book_id)
        
        elif choice == '4':
            book_id = int(input("Enter book ID to return: "))
            return_book(conn, book_id)
        
        elif choice == '5':
            print("Exiting the Library Management System. Goodbye!")
            conn.close()
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
