#Staff Help
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as ms
import re
import linecache

HEADER_FONT = re.sub('^.*?=', '', linecache.getline('config.txt',11)).strip()
class StaffHelp():
    def __init__(self, root, notebook, user_email):
        self.root = root
        self.notebook = notebook

        staff_help_page = tk.Frame(self.notebook)
        notebook.add(staff_help_page, text="Staff Help Page")

        header_frame = tk.Frame(staff_help_page)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        header = tk.Label(header_frame, text="Staff Help Page", font=HEADER_FONT)
        header.pack(side=tk.TOP)

        large_frame = tk.Frame(staff_help_page)
        large_frame.pack(fill=tk.BOTH, expand=True)

        _help = tk.Label(large_frame, text="""The book database page is responsible for allowing
you as a staff member to do the following, with a description of how to accomplish it:

Issue Book:
    1. Enter the Book's ID in the 'ID' field that matches the ID on the book or optionally enter the Title to find the matching ID, author or genre;
    1.1 There will be an option to autocomplete the rest of the information. Make sure that the autocomplete fills in the correct information for the book you want;
    1.2 Optionally, you can enter the Title and autocomplete the rest of the information that way.
    2. Enter the email address of the patron that wants the book in the 'Recipient Email' field;
    2.1 If the user does not have an account, leave this field empty.
    3. Select the date by which they must return the book on the 'Expected Return Date' field, using the calendar given. The system will allow dates between the current day and 3 months from the current day;
    4. Press 'Issue Book' button.

Return Book:
    1. Enter the Book's ID in the 'ID' field that matches the ID on the book or optionally enter the Title to find the matching ID, author or genre;
    1.1 There will be an option to autocomplete the rest of the information. Make sure that the autocomplete fills in the correct information for the book you want;
    1.2 Optionally, you can enter the Title and autocomplete the rest of the information that way.
    2. Enter the email address of the patron that wants to return the book in the 'Return Email' field;
    2.1 If the user does not have an account, leave this field empty.
    3. Press 'Return Book' button.

Add Book Into System:
    1. Enter the Title of the book in the 'Title' field;
    2. Enter the Author of the book in the 'Author' field;
    3. Select the Genre of the book in the 'Genre' dropdown menu;
    3.1 If the genre you entered is not in the dropdown list, go to instruction set labelled 'Manage Genres';
    4. Press 'Add Book' button.

Remove Book From System:
    1. Enter the Book ID of the book in the 'ID' field;
    1.1 There will be an option to autocomplete the rest of the information. Make sure that the autocomplete fills in the correct information for the book you want;
    1.2 Optionally, you can enter the Title and autocomplete the rest of the information that way.
    2. Press the 'Remove Book' button.

Manage Genres:
    1. Enter the genre name in the 'Genre Name' field;
    2. Press 'Add New Genre' button if you want to add the specified genre to the database;
    2.1 Press 'Remove Genre' button if you want to remove the specified genre from the database.

Using the database at the bottom of the page:
    Use the search parameters to find books in the database and any information regarding them.
    Location refers to their location in the library (what shelf code they are on).
    Issued refers to if the book is currently in someones ownership.
    The issue/return date display when a user issued and must return the book.

    The column headings of the database table can be pressed to sort them in ascending/descending order.

Extra Information:
    You may recieve occasional prompts when returning some books that will alert you that the book is overdue. You may then choose to return it anyway, or cancel the return and let the patron know that it is overdue,
    therefore fees must be paid.

    After every issue/return you will get a prompt that the user has been emailed details regarding the issue/return.
""", justify=tk.LEFT)
        _help.pack()
