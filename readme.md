## Pass Level Summary

* We have defined a Book class to keep track of each book and the days it has been borrowed by members.
* The Member class is defined but not used for any specific purpose in the current implementation.
* The Records class manages the overall record-keeping, including reading from a file, adding data, and displaying the records.
* The read_records method reads data from the provided file and populates the book and member data.
* The display_records method formats and prints the data in a table, ensuring proper alignment of columns.
* The main function initializes the Records object and triggers the read and display operations based on the provided file name.

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

## DI Level Summary

### Enhanced Member Class
- The `Member` class includes additional attributes:
  - `first_name`
  - `last_name`
  - `dob`
  - `member_type`
- Methods for adding borrowing details and computing statistics:
  - Number of textbooks borrowed
  - Number of fiction books borrowed
  - Compliance with borrowing limits
  - Average borrowing days

### Improved Records Class
- The `Records` class now includes methods for reading member data and associating borrowed books with members.
- Member validation and addition of borrowing details:
  - Warns if a member ID is not found in the member list.
  - Adds borrowing details to the corresponding member.
- Maintains a dictionary for quick member lookup.

### Main Function Enhancements
- The `main` function now handles three command-line arguments:
  - One for the record file
  - Another for the book file
  - Another for the member file
- Ensures that member data is read and displayed if the member file is provided.
- Displays the member information table and saves it to `reports.txt`.

### Technical Decisions and Challenges
1. **Member Class Enhancement**: Enhancing the `Member` class required additional attributes and methods for managing member-specific data, such as names and borrowing limits.
2. **Records Class Restructuring**: Significant restructuring was necessary to accommodate the new `Member` class and to ensure proper association between books and members. This involved maintaining a dictionary for quick member lookup and updating the reading methods to incorporate member details.
3. **Validation and Error Handling**: Enhanced validation in the `read_books` method ensures that the constraints on book types and borrowing days are strictly enforced, with appropriate error handling and termination.
4. **Display Enhancements**: Methods for displaying member and book information were updated to include the new attributes and ensure proper formatting and alignment.
5. **File Handling and Saving**: Updated the `save_books_to_file` method to save detailed member and book information to a file for further analysis or reporting.
6. **Command-Line Arguments**: Customizing the `main` function to handle three command-line arguments required careful consideration to ensure that the order of arguments was maintained and appropriate actions were taken based on the provided files.

### Summary
The DI level implementation introduced significant complexity, especially in managing the relationships between books and members and ensuring accurate record-keeping and validation. The enhancements to the `Member` and `Records` classes, along with the customized main function and detailed error handling, provide a robust system for managing library records and generating detailed reports.
