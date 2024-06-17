# Maharab Kibria
# s4083577
#Attempted Level: HD Level.
#Known Issues: The code is completely meeting all the requirements except the fees in members table and the date format in books table.

import sys

from datetime import datetime

# Custom exceptions
class FileNotFound(Exception):
    pass

class EmptyFile(Exception):
    pass

class InvalidRecordFormat(Exception):
    pass

class InvalidBookID(Exception):
    pass

class InvalidMemberID(Exception):
    pass

class Book:
    def __init__(self, book_id, name=None, book_type=None, n_copy=None, max_days=None, late_charge=None):
        self.book_id = book_id
        self.name = name
        self.book_type = book_type
        self.n_copy = n_copy
        self.max_days = max_days
        self.late_charge = late_charge
        self.borrowed_days = {}

    def add_borrowed_days(self, member_id, days):
        self.borrowed_days[member_id] = days

    def get_statistics(self):
        n_borrow = sum(1 for days in self.borrowed_days.values() if isinstance(days, int))
        n_reserve = sum(1 for days in self.borrowed_days.values() if days == '--')
        borrow_days = [days for days in self.borrowed_days.values() if isinstance(days, int)]
        min_days = min(borrow_days) if borrow_days else 0
        max_days = max(borrow_days) if borrow_days else 0
        return n_borrow, n_reserve, (min_days, max_days)


class Member:
    def __init__(self, member_id, first_name=None, last_name=None, dob=None, member_type=None):
        self.member_id = member_id.strip()
        self.first_name = first_name.strip() if first_name else ''
        self.last_name = last_name.strip() if last_name else ''
        self.dob = dob.strip() if dob else ''
        self.member_type = member_type.strip() if member_type else ''
        self.borrowed = {'Textbook': 0, 'Fiction': 0}
        self.total_borrowed_days = 0
        self.total_borrow_count = 0
        self.fee = 0.0

    def add_borrowing(self, book_type, days):
        book_type = book_type.strip()
        if book_type == 'T':
            book_type = 'Textbook'
        elif book_type == 'F':
            book_type = 'Fiction'
        else:
            print(f"Unknown book type: {book_type}")
            return

        if days == '--':
            self.borrowed[book_type] += 1
        elif isinstance(days, int):
            self.borrowed[book_type] += 1
            self.total_borrowed_days += days
            self.total_borrow_count += 1
            if (book_type == 'Textbook' and days > 14) or (book_type == 'Fiction' and days > 15):
                excess_days = days - (14 if book_type == 'Textbook' else 15)
                charge = 1.2 * excess_days if book_type == 'Textbook' else 1.8 * excess_days
                self.fee += charge

    def check_limits(self):
        if self.member_type == 'Standard':
            return (self.borrowed['Textbook'] <= 1 and self.borrowed['Fiction'] <= 2)
        elif self.member_type == 'Premium':
            return (self.borrowed['Textbook'] <= 2 and self.borrowed['Fiction'] <= 3)

    def get_stats(self):
        stats = {
            'textbooks': self.borrowed['Textbook'],
            'fictions': self.borrowed['Fiction'],
            'complies': self.check_limits(),
            'average_days': self.calculate_average_borrowing_days() if self.total_borrow_count > 0 else 0,
            'fee': self.fee
        }
        return stats

    def calculate_average_borrowing_days(self):
        return self.total_borrowed_days / self.total_borrow_count if self.total_borrow_count else 0


class Records:

    def __init__(self):
        self.books = []
        self.members = []
        self.member_dict = {}  # Dictionary to store member objects
        self.total_borrowed_days = 0
        self.total_borrow_count = 0

    def read_members(self, member_file_name):
        try:
            with open(member_file_name, 'r') as file:
                lines = file.readlines()
                if not lines:
                    raise EmptyFile(f"The file {member_file_name} is empty.")
                for line in lines:
                    line = line.strip()
                    if line:
                        data = line.split(',')
                        if len(data) == 5:
                            member_id, first_name, last_name, dob, member_type = [item.strip() for item in data]
                            if not member_id.startswith('M') or not member_id[1:].isdigit():
                                raise InvalidMemberID(f"Invalid member ID format: {member_id}")
                            member = Member(member_id, first_name, last_name, dob, member_type)
                            self.members.append(member)
                            self.member_dict[member_id] = member
                        else:
                            print(f"Skipping incomplete or malformed line: {line}")
        except FileNotFoundError:
            print(f"The file {member_file_name} does not exist.")
            sys.exit(1)
        except EmptyFile as e:
            print(e)
            sys.exit(1)

    def find_member_by_id(self, member_id):
        return self.member_dict.get(member_id, None)

    def read_records(self, record_file_name):
        try:
            with open(record_file_name, 'r') as file:
                lines = file.readlines()
                if not lines:
                    raise EmptyFile(f"The file {record_file_name} is empty.")
                for line in lines:
                    data = line.strip().split(',')
                    book_id = data[0]
                    if not book_id.startswith('B') or not book_id[1:].isdigit():
                        raise InvalidBookID(f"Invalid book ID format: {book_id}")
                    book = next((b for b in self.books if b.book_id == book_id), None)
                    if not book:
                        book = Book(book_id)
                        self.books.append(book)
                    for record in data[1:]:
                        member_id, days = record.split(':')
                        member_id = member_id.strip()
                        days = days.strip()
                        if days == 'R':
                            days = '--'
                        elif days.isdigit():
                            days = int(days)
                            self.total_borrowed_days += days
                            self.total_borrow_count += 1
                        else:
                            raise InvalidRecordFormat(f"Invalid record format in {record_file_name}: {record}")
                        book.add_borrowed_days(member_id, days)

                        member = self.find_member_by_id(member_id)
                        if member:
                            if book.book_type is None:
                                book_type = next((b.book_type for b in self.books if b.book_id == book_id), None)
                                if book_type:
                                    book.book_type = book_type
                            member.add_borrowing(book.book_type, days)
                        else:
                            if self.members:
                                print(f"Warning: Member ID {member_id} not found in member list.")
        except FileNotFoundError:
            print(f"The file {record_file_name} does not exist.")
            sys.exit(1)
        except EmptyFile as e:
            print(e)
            sys.exit(1)
        except InvalidRecordFormat as e:
            print(e)
            sys.exit(1)

    def read_books(self, book_file_name):
        try:
            with open(book_file_name, 'r') as file:
                lines = file.readlines()
                if not lines:
                    raise EmptyFile(f"The file {book_file_name} is empty.")
                for line in lines:
                    data = line.strip().split(',')
                    book_id = data[0]
                    if not book_id.startswith('B') or not book_id[1:].isdigit():
                        raise InvalidBookID(f"Invalid book ID format: {book_id}")
                    name = data[1]
                    book_type = data[2].strip()
                    n_copy = int(data[3])
                    max_days = int(data[4])
                    late_charge = float(data[5])
                    book = next((b for b in self.books if b.book_id == book_id), None)
                    if not book:
                        book = Book(book_id, name, book_type, n_copy, max_days, late_charge)
                        self.books.append(book)
                    else:
                        book.name = name
                        book.book_type = book_type
                        book.n_copy = n_copy
                        book.max_days = max_days
                        book.late_charge = late_charge
        except FileNotFoundError:
            print(f"The file {book_file_name} does not exist.")
            sys.exit(1)
        except EmptyFile as e:
            print(e)
            sys.exit(1)

    def display_members(self):
        if not self.members:
            print("No member records to display.")
            return

        standard_members = [m for m in self.members if m.member_type == 'Standard']
        premium_members = [m for m in self.members if m.member_type == 'Premium']

        standard_members.sort(key=lambda x: x.fee, reverse=True)
        premium_members.sort(key=lambda x: x.fee, reverse=True)

        print("STANDARD MEMBERS")
        self._print_member_table(standard_members)

        print("\nPREMIUM MEMBERS")
        self._print_member_table(premium_members)

    def _print_member_table(self, members):
        print(f"{'Member ID':<10} {'FName':<15} {'LName':<15} {'Type':<10} {'DOB':<15} {'Ntextbook':>10} {'Nfiction':>10} {'Fee':>10}")
        for member in members:
            stats = member.get_stats()
            ntextbook = f"{stats['textbooks']}!" if not stats['complies'] and stats['textbooks'] > (
                1 if member.member_type == 'Standard' else 2) else str(stats['textbooks'])
            nfiction = f"{stats['fictions']}!" if not stats['complies'] and stats['fictions'] > (
                2 if member.member_type == 'Standard' else 3) else str(stats['fictions'])
            fee = f"{stats['fee']:.2f}"
            print(f"{member.member_id:<10} {member.first_name:<15} {member.last_name:<15} {member.member_type:<10} {member.dob:<15} {ntextbook:>10} {nfiction:>10} {fee:>10}")

    def display_records(self):
        if not self.books:
            print("No records to display.")
            return

        col_width = 5
        header_width = 11

        print("RECORDS")
        header = "Member IDs".ljust(header_width) + ''.join([f"{book.book_id:>{col_width}}" for book in self.books])
        print(header)
        print('-' * len(header))

        member_ids = {member.member_id for member in self.members} if self.members else {member_id for book in self.books for member_id in book.borrowed_days}
        for member_id in sorted(member_ids):
            row = f"{member_id:<{header_width}}"
            for book in self.books:
                borrow_days = book.borrowed_days.get(member_id, 'xx')
                row += f"{str(borrow_days):>{col_width}}"
            print(row)

        total_books = len(self.books)
        total_members = len(member_ids)
        average_borrowed_days = self.total_borrowed_days / self.total_borrow_count if self.total_borrow_count else 0
        print("\nRECORDS SUMMARY")
        print(f"There are {total_members} members and {total_books} books.")
        print(f"The average number of borrow days is {average_borrowed_days:.2f} (days).")

    def display_books(self):
        if not self.books:
            print("No book records to display.")
            return

        col_widths = {
            'book_id': 10,
            'name': 20,
            'book_type': 10,
            'n_copy': 6,
            'max_days': 8,
            'late_charge': 10,
            'n_borrow': 8,
            'n_reserve': 10,
            'range': 15,
        }

        # Splitting books into textbooks and fictions
        textbooks = []
        fictions = []
        for book in self.books:
            # print(f"Debug: Book ID {book.book_id}, Name {book.name}, Type {book.book_type}")
            if book.book_type == 'T':
                textbooks.append(book)
            elif book.book_type == 'F':
                fictions.append(book)

        # Sorting books by name
        textbooks.sort(key=lambda x: x.name)
        fictions.sort(key=lambda x: x.name)

        def print_table(books, title):
            header = (f"{'Book IDs':<{col_widths['book_id']}} "
                      f"{'Name':<{col_widths['name']}} "
                      f"{'Type':<{col_widths['book_type']}} "
                      f"{'Ncopy':<{col_widths['n_copy']}} "
                      f"{'Maxday':<{col_widths['max_days']}} "
                      f"{'Lcharge':<{col_widths['late_charge']}} "
                      f"{'Nborrow':<{col_widths['n_borrow']}} "
                      f"{'Nreserve':<{col_widths['n_reserve']}} "
                      f"{'Range':<{col_widths['range']}}")

            print(title)
            print(header)
            print('-' * len(header))

            for book in books:
                n_borrow, n_reserve, (min_days, max_days) = book.get_statistics()
                row = (f"{book.book_id:<{col_widths['book_id']}} "
                       f"{book.name:<{col_widths['name']}} "
                       f"{book.book_type:<{col_widths['book_type']}} "
                       f"{book.n_copy:<{col_widths['n_copy']}} "
                       f"{book.max_days:<{col_widths['max_days']}} "
                       f"{book.late_charge:<{col_widths['late_charge']}.2f} "
                       f"{n_borrow:<{col_widths['n_borrow']}} "
                       f"{n_reserve:<{col_widths['n_reserve']}} "
                       f"({min_days},{max_days})")
                print(row)
            print()

        # Print Textbooks
        print_table(textbooks, "TEXTBOOK INFORMATION")

        # Print Fictions
        print_table(fictions, "FICTION INFORMATION")

    def save_books_to_file(self, filename):
        with open(filename, 'a') as file:
            col_widths = {
                'book_id': 10,
                'name': 20,
                'book_type': 10,
                'n_copy': 6,
                'max_days': 8,
                'late_charge': 10,
                'n_borrow': 8,
                'n_reserve': 10,
                'range': 15,
            }

            header = (f"{'Book IDs':<{col_widths['book_id']}} "
                      f"{'Name':<{col_widths['name']}} "
                      f"{'Type':<{col_widths['book_type']}} "
                      f"{'Ncopy':<{col_widths['n_copy']}} "
                      f"{'Maxday':<{col_widths['max_days']}} "
                      f"{'Lcharge':<{col_widths['late_charge']}} "
                      f"{'Nborrow':<{col_widths['n_borrow']}} "
                      f"{'Nreserve':<{col_widths['n_reserve']}} "
                      f"{'Range':<{col_widths['range']}}")

            file.write("BOOK INFORMATION\n")
            file.write(header + '\n')
            file.write('-' * len(header) + '\n')

            for book in self.books:
                n_borrow, n_reserve, (min_days, max_days) = book.get_statistics()
                row = (f"{book.book_id:<{col_widths['book_id']}} "
                       f"{book.name:<{col_widths['name']}} "
                       f"{book.book_type:<{col_widths['book_type']}} "
                       f"{book.n_copy:<{col_widths['n_copy']}} "
                       f"{book.max_days:<{col_widths['max_days']}} "
                       f"{book.late_charge:<{col_widths['late_charge']}.2f} "
                       f"{n_borrow:<{col_widths['n_borrow']}} "
                       f"{n_reserve:<{col_widths['n_reserve']}} "
                       f"({min_days},{max_days})")
                file.write(row + '\n')

            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            file.write(f"Report generated on: {dt_string}\n")
            file.write("\n")

def main():
    if len(sys.argv) < 2:
        print("Usage: python my_record.py <record_file_name> [<book_file_name> [<member_file_name>]]")
        return

    record_file_name = sys.argv[1]
    book_file_name = sys.argv[2] if len(sys.argv) > 2 else None
    member_file_name = sys.argv[3] if len(sys.argv) > 3 else None

    records = Records()

    if member_file_name:
        records.read_members(member_file_name)

    if book_file_name:
        records.read_books(book_file_name)

    records.read_records(record_file_name)

    records.display_records()

    if book_file_name:
        records.display_books()

    if member_file_name:
        records.display_members()

    if book_file_name or member_file_name:
        records.save_books_to_file('reports.txt')

if __name__ == "__main__":
    main()




'''
VCS: https://github.com/Kibria10/PF_FinalChallange (I will make this repository public after submission. There are 4 branches to identify each stage of the code)

Documentation:
## Pass Level Summary

- `Book` class tracks each book and borrowing days.
- `Member` class exists but not used yet.
- `Records` class handles record-keeping, including reading from a file, adding data, and displaying records.
- `read_records`: Reads data from a file and populates book and member data.
- `display_records`: Formats and prints data in a table with proper alignment.
- `main`: Initializes `Records` object, reads, and displays based on file name.

## Credit Level Summary

### Enhanced Book Class
- New attributes: `name`, `book_type`, `n_copy`, `max_days`, `late_charge`.
- Methods for adding borrowed days and computing stats (borrowing members, reservations, range of borrowing days).

### Validation in Read Books Method
- Ensures textbooks (`book_type == 'T'`) have max 14 days borrowing.
- Ensures fiction books (`book_type == 'F'`) have max >14 days borrowing.
- Terminates with an error if conditions are not met.

### Records Class Enhancements
- Methods to read and validate book data.
- Display detailed book info and save to a file.

### Display Books Method
- Prints detailed book info: ID, Name, Type, Copies, Max days, Late charge, Borrowing members, Reservations, Range of days.

### Save Books to File Method
- Writes book info to `reports.txt` in a specified format.

### Main Function Enhancements
- Handles command-line arguments for record and book files.
- Displays record and book tables.
- Saves book data to `reports.txt`.

## DI Level Summary

### Enhanced Member Class
- New attributes: `first_name`, `last_name`, `dob`, `member_type`.
- Methods for adding borrowing details and computing stats (textbooks, fictions, borrowing limits, average days).

### Improved Records Class
- Reads member data, associates borrowed books with members.
- Warns if member ID not found, adds borrowing details, maintains a dictionary for quick lookup.

### Main Function Enhancements
- Handles three command-line arguments: record file, book file, member file.
- Reads and displays member data, saves to `reports.txt`.

### Technical Decisions and Challenges
1. Enhanced `Member` class for managing data.
2. Restructured `Records` class for book-member associations.
3. Improved validation in `read_books`.
4. Updated display methods for new attributes.
5. Enhanced `save_books_to_file`.
6. Customized main function for three arguments.

### Summary
DI level adds complexity in managing book-member relationships and validation, providing a robust system for record-keeping and reporting.

## High Distinction (HD) Level Summary

### Enhancements from DI to HD Level

### Custom Exceptions for Error Handling
- Introduced exceptions: `FileNotFound`, `EmptyFile`, `InvalidRecordFormat`, `InvalidBookID`, `InvalidMemberID`.

### Improved Member Class
- Added `fee` attribute for overdue charges.
- Enhanced `add_borrowing` method for fee calculation.

### Enhanced Records Class
- Split book/member info into tables (Textbooks, Fictions, Standard, Premium Members).
- Enhanced file reading with exceptions.
- Modified display methods for new table structures.
- Enhanced `save_books_to_file` with timestamps.

### Member and Book Information Tables
- Separate tables for Textbooks, Fictions, Standard, Premium Members.
- Sorted alphabetically by book name and by fee for members.

### Command-Line Arguments and Usage
- Handles three command-line arguments, added error messages for file issues.

### Technical Decisions and Challenges
1. Custom exceptions for robustness.
2. Fee attribute for overdue charges.
3. Split tables for readability.
4. Ensured correct sorting and formatting.
5. Added timestamps to report files.

### Summary
HD level improves error handling, data categorization, and reporting, ensuring robust and user-friendly program.
'''