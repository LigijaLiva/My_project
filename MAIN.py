import mysql.connector
from configparser import ConfigParser

def connect_to_database():
    """Establish connection to the database."""
    config = ConfigParser()
    config.read('CONFIGURATION.ini')
    try:
        connection = mysql.connector.connect(
            host=config['database']['host'],
            user=config['database']['user'],
            password=config['database']['password'],
            database=config['database']['database']
        )
        return connection
    except mysql.connector.Error as e:
        if "Unknown database" in str(e):
            print("Database not found! Please run IMPORT_DATA.py to set up the database.")
        else:
            print(f"Error connecting to the database: {e}")
        return None

def add_record(connection):
    """Add a new book record."""
    try:
        cursor = connection.cursor()
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        cursor.execute("INSERT INTO books (title, author) VALUES (%s, %s)", (title, author))
        connection.commit()
        print("Book added successfully!")
    except mysql.connector.Error as e:
        print(f"Error adding record: {e}")

def edit_record(connection):
    """Edit an existing book record."""
    try:
        cursor = connection.cursor()
        book_id = input("Enter the ID of the book to edit: ")
        title = input("Enter new title: ")
        author = input("Enter new author: ")
        cursor.execute("UPDATE books SET title = %s, author = %s WHERE id = %s", (title, author, book_id))
        connection.commit()
        print("Book updated successfully!")
    except mysql.connector.Error as e:
        print(f"Error updating record: {e}")

def delete_record(connection):
    """Delete a book record."""
    try:
        cursor = connection.cursor()
        book_id = input("Enter the ID of the book to delete: ")
        cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
        connection.commit()
        print("Book deleted successfully!")
    except mysql.connector.Error as e:
        print(f"Error deleting record: {e}")

def view_records(connection):
    """View all book records."""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM books")
        records = cursor.fetchall()
        if not records:
            print("No records found.")
        else:
            print("\nBooks in Database:")
            print(f"{'ID':<5} {'Title':<30} {'Author':<30}")
            print("-" * 70)
            for row in records:
                print(f"{row[0]:<5} {row[1]:<30} {row[2]:<30}")
    except mysql.connector.Error as e:
        print(f"Error fetching records: {e}")

def add_publisher(connection):
    """Add a new publisher record."""
    try:
        cursor = connection.cursor()
        name = input("Enter publisher name: ")
        address = input("Enter publisher address: ")
        cursor.execute("INSERT INTO publishers (name, address) VALUES (%s, %s)", (name, address))
        connection.commit()
        print("Publisher added successfully!")
    except mysql.connector.Error as e:
        print(f"Error adding publisher: {e}")

def view_publishers(connection):
    """View all publisher records."""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM publishers")
        records = cursor.fetchall()
        if not records:
            print("No publishers found.")
        else:
            print("\nPublishers in Database:")
            print(f"{'ID':<5} {'Name':<30} {'Address':<30}")
            print("-" * 70)
            for row in records:
                print(f"{row[0]:<5} {row[1]:<30} {row[2]:<30}")
    except mysql.connector.Error as e:
        print(f"Error fetching publishers: {e}")

def main():
    """Main program loop."""
    connection = connect_to_database()
    if not connection:
        return

    while True:
        print("\nBook Management Menu:")
        print("1. Add Book")
        print("2. Edit Book")
        print("3. Delete Book")
        print("4. View All Books")
        print("5. Exit")
        print("6. Add Publisher")
        print("7. View All Publishers")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_record(connection)
        elif choice == '2':
            edit_record(connection)
        elif choice == '3':
            delete_record(connection)
        elif choice == '4':
            view_records(connection)
        elif choice == '5':
            print("Exiting program. Goodbye!")
        elif choice == '6':
            add_publisher(connection)
        elif choice == '7':
            view_publishers(connection)
            break
        else:
            print("Invalid choice. Please try again.")

    if connection and connection.is_connected():
        connection.close()

if __name__ == "__main__":
    main()
