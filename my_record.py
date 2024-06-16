import sys

# Class to represent a Book with its borrowing details
class Book:
    def __init__(self, book_id):
        self.book_id = book_id
        self.borrowed_days = {}

    # Method to add the number of days a member borrowed the book
    def add_borrowed_days(self, member_id, days):
        self.borrowed_days[member_id] = days

# Class to represent a Member (currently not used for any specific purpose)
class Member:
    def __init__(self, member_id):
        self.member_id = member_id

# Class to manage the records of books and members
class Records:
    def __init__(self):
        self.books = []
        self.members = set()
        self.total_borrowed_days = 0
        self.total_borrow_count = 0

    # Method to read the records from a file
    def read_records(self, record_file_name):
        try:
            with open(record_file_name, 'r') as file:
                for line in file:
                    data = line.strip().split(',')
                    book_id = data[0]
                    book = Book(book_id)
                    self.books.append(book)
                    for record in data[1:]:
                        member_id, days = record.split(':')
                        member_id = member_id.strip()  # Remove extra spaces
                        days = days.strip()  # Remove extra spaces
                        if days == 'R':
                            days = '--'  # Represent 'R' as '--' for readability
                        else:
                            days = int(days)  # Convert days to integer
                            self.total_borrowed_days += days
                            self.total_borrow_count += 1
                        book.add_borrowed_days(member_id, days)
                        self.members.add(member_id)
        except FileNotFoundError:
            print(f"The file {record_file_name} does not exist.")
            sys.exit(1)

    # Method to display the records in a tabular format
    def display_records(self):
        if not self.books:
            print("No records to display.")
            return

        # Set fixed widths for columns to ensure alignment
        col_width = 5  # Fixed width for each book column
        header_width = 11  # Width for the "Member IDs" column

        # Display the header row
        print("RECORDS")
        header = "Member IDs".ljust(header_width) + ''.join([f"{book.book_id:>{col_width}}" for book in self.books])
        print(header)
        print('-' * len(header))

        # Display each member's borrowing details
        for member_id in sorted(self.members):
            row = f"{member_id:<{header_width}}"
            for book in self.books:
                borrow_days = book.borrowed_days.get(member_id, 'xx')
                row += f"{str(borrow_days):>{col_width}}"
            print(row)

        # Display the summary section
        total_books = len(self.books)
        total_members = len(self.members)
        average_borrowed_days = self.total_borrowed_days / self.total_borrow_count if self.total_borrow_count else 0
        print("\nRECORDS SUMMARY")
        print(f"There are {total_members} members and {total_books} books.")
        print(f"The average number of borrow days is {average_borrowed_days:.2f} (days).")

def main():
    if len(sys.argv) < 2:
        print("Usage: python my_record.py <record_file_name>")
        return

    record_file_name = sys.argv[1]
    records = Records()
    records.read_records(record_file_name)
    records.display_records()

if __name__ == "__main__":
    main()
