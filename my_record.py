import sys

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
            'average_days': self.calculate_average_borrowing_days() if self.total_borrow_count > 0 else 0
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
                for line in file:
                    line = line.strip()
                    if line:
                        data = line.split(',')
                        if len(data) == 5:
                            member_id, first_name, last_name, dob, member_type = [item.strip() for item in data]
                            member = Member(member_id, first_name, last_name, dob, member_type)
                            self.members.append(member)
                            self.member_dict[member_id] = member
                        else:
                            print(f"Skipping incomplete or malformed line: {line}")
        except FileNotFoundError:
            print(f"The file {member_file_name} does not exist.")
            sys.exit(1)

    def find_member_by_id(self, member_id):
        return self.member_dict.get(member_id, None)

    def read_records(self, record_file_name):
        try:
            with open(record_file_name, 'r') as file:
                for line in file:
                    data = line.strip().split(',')
                    book_id = data[0]
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
                        else:
                            days = int(days)
                            self.total_borrowed_days += days
                            self.total_borrow_count += 1
                        book.add_borrowed_days(member_id, days)

                        member = self.find_member_by_id(member_id)
                        if member:
                            if book.book_type is None:
                                book_type = next((b.book_type for b in self.books if b.book_id == book_id), None)
                                if book_type:
                                    book.book_type = book_type
                            member.add_borrowing(book.book_type, days)
                        else:
                            # Only print warnings if the member list is provided
                            if self.members:
                                print(f"Warning: Member ID {member_id} not found in member list.")
        except FileNotFoundError:
            print(f"The file {record_file_name} does not exist.")
            sys.exit(1)

    def read_books(self, book_file_name):
        try:
            with open(book_file_name, 'r') as file:
                for line in file:
                    data = line.strip().split(',')
                    book_id = data[0]
                    name = data[1]
                    book_type = data[2].strip()
                    n_copy = int(data[3])
                    max_days = int(data[4])
                    late_charge = float(data[5])
                    if book_type == 'T' and max_days != 14:
                        print(f"Error: Textbook {book_id} has invalid max days {max_days}.")
                        sys.exit(1)
                    if book_type == 'F' and max_days <= 14:
                        print(f"Error: Fiction book {book_id} has invalid max days {max_days}.")
                        sys.exit(1)
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

    def display_members(self):
        if not self.members:
            print("No member records to display.")
            return

        print("MEMBER INFORMATION")
        print(f"{'Member ID':<10} {'FName':<15} {'LName':<15} {'Type':<10} {'DOB':<15} {'Ntextbook':>10} {'Nfiction':>10} {'Average':>10}")

        member_objects = [m for m in self.members if isinstance(m, Member)]
        for member in sorted(member_objects, key=lambda x: x.member_id):
            stats = member.get_stats()
            ntextbook = f"{stats['textbooks']}!" if not stats['complies'] and stats['textbooks'] > (
                1 if member.member_type == 'Standard' else 2) else str(stats['textbooks'])
            nfiction = f"{stats['fictions']}!" if not stats['complies'] and stats['fictions'] > (
                2 if member.member_type == 'Standard' else 3) else str(stats['fictions'])
            average = f"{stats['average_days']:.2f}"

            print(f"{member.member_id:<10} {member.first_name:<15} {member.last_name:<15} {member.member_type:<10} {member.dob:<15} {ntextbook:>10} {nfiction:>10} {average:>10}")

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

        member_ids = {member.member_id for member in self.members} if self.members else {member_id for book in self.books for member_id in book.borrowed_days}  # Set of member IDs
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

        header = (f"{'Book IDs':<{col_widths['book_id']}} "
                  f"{'Name':<{col_widths['name']}} "
                  f"{'Type':<{col_widths['book_type']}} "
                  f"{'Ncopy':<{col_widths['n_copy']}} "
                  f"{'Maxday':<{col_widths['max_days']}} "
                  f"{'Lcharge':<{col_widths['late_charge']}} "
                  f"{'Nborrow':<{col_widths['n_borrow']}} "
                  f"{'Nreserve':<{col_widths['n_reserve']}} "
                  f"{'Range':<{col_widths['range']}}")

        print("BOOK INFORMATION")
        print(header)
        print('-' * len(header))

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
            print(row)

    def save_books_to_file(self, filename):
        with open(filename, 'w') as file:
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

