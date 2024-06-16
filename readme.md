## Pass Level Summary:

* We have defined a Book class to keep track of each book and the days it has been borrowed by members.
* The Member class is defined but not used for any specific purpose in the current implementation.
* The Records class manages the overall record-keeping, including reading from a file, adding data, and displaying the records.
* The read_records method reads data from the provided file and populates the book and member data.
* The display_records method formats and prints the data in a table, ensuring proper alignment of columns.
The main function initializes the Records object and triggers the read and display operations based on the provided file name.

## Credit Level Summary

### Enhanced Book Class
- The `Book` class now includes additional attributes:
  - `name`
  - `book_type`
  - `n_copy`
  - `max_days`
  - `late_charge`
- Methods for adding borrowed days and computing statistics:
  - Number of borrowing members
  - Number of reservations
  - Range of borrowing days

### Validation in Read Books Method
- The `read_books` method in the `Records` class reads book details from a file and performs validation.
  - Ensures that textbooks (`book_type == 'T'`) have a maximum borrowing period of 14 days.
  - Ensures that fiction books (`book_type == 'F'`) have a maximum borrowing period greater than 14 days.
  - Terminates with an error message if these conditions are not met.

### Records Class Enhancements
- The `Records` class manages the overall record-keeping, including reading from files, adding data, and displaying the records.
- Methods to read and validate book data from a file.
- Methods to display detailed book information and save it to a file.

### Display Books Method
- The `display_books` method formats and prints detailed book information, including:
  - Book ID
  - Name
  - Type
  - Number of copies
  - Maximum days
  - Late charge
  - Number of borrowing members
  - Number of reservations
  - Range of borrowing days

### Save Books to File Method
- The `save_books_to_file` method writes the book information to a file named `reports.txt`.
- This method ensures that the book information is stored in a specified format for further analysis or reporting.

### Main Function Enhancements
- The `main` function initializes the `Records` object and triggers the read and display operations based on the provided file names.
- Handles two command-line arguments:
  - One for the record file
  - Another for the book file
- Ensures that both the record table and book information table are displayed.
- Saves the book information to `reports.txt` when the book file is provided.
