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
