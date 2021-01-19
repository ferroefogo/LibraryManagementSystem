# BookDatabase page

# Imports
import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox as ms
import string
from tkcalendar import DateEntry
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re
import linecache

# File Imports
from email_sys import Email

# Connect to database
conn = sqlite3.connect('LibrarySystem.db')
c = conn.cursor()

# File Configurations
WIDTH = re.sub('^.*?=', '', linecache.getline('config.txt',1))
PADX = re.sub('^.*?=', '', linecache.getline('config.txt',2))
PADY = re.sub('^.*?=', '', linecache.getline('config.txt',3))
BG = re.sub('^.*?=', '', linecache.getline('config.txt',6)).strip()
MAIN_APP_BG = re.sub('^.*?=', '', linecache.getline('config.txt',9)).strip()
FONT = re.sub('^.*?=', '', linecache.getline('config.txt',10)).strip()
HEADER_FONT = re.sub('^.*?=', '', linecache.getline('config.txt',11)).strip()

# List of genres
c.execute("SELECT genre FROM Genres")
genres_list_fetch = c.fetchall()
genre_choice_list = [x[0] for x in genres_list_fetch]


# List of locations
location_choice_list = list(string.ascii_uppercase)
location_alphabet_symbol = location_choice_list.append('*')
location_empty_insert = location_choice_list.insert(0, '-EMPTY-')

# List of issued
issued_choice_list = ['-EMPTY-', '0', '1']


class BookDatabase():
    '''
    Access Level: STAFF ONLY
    Functions: Update the database when book information is moved around,
               by cause of:
                    - Issuing Books
                    - Returning Books
                    - Adding Books
                    - Removing Books
                    - Adding Genres
                    - Removing Genres
    '''
    def __init__(self, root, notebook, current_user_email):
        '''
        Initiates the visual window of the system.
        '''

        # Class variables
        self.tree_ids = []
        self.lista = []
        self.root = root
        self.notebook = notebook

        # Create notebook tab
        book_database_page = tk.Frame(self.notebook)
        notebook.add(book_database_page, text='Book Database')

        # Page header
        header_frame = tk.Frame(book_database_page)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        header = tk.Label(header_frame, text='Book Database', font=HEADER_FONT)
        header.pack(side=tk.TOP)

        #  Book database TreeView
        tree_container = tk.Frame(book_database_page, bg=BG)
        tree_container.pack(side=tk.BOTTOM, anchor=tk.N, padx=PADX, pady=PADY)

        tree_header = tk.Label(tree_container, text='Database', font=FONT, bg=BG)
        tree_header.pack(padx=PADX, pady=PADY)

        # Set up TreeView table
        self.columns = ('Book ID', 'Title', 'Author', 'Genre', 'Location', 'Issued', 'Issue Date', 'Return Date')
        self.tree = ttk.Treeview(tree_container, columns=self.columns, show='headings')
        self.tree.heading("Book ID", text='Book ID')
        self.tree.heading("Title", text='Title')
        self.tree.heading("Author", text='Author')
        self.tree.heading("Genre", text='Genre')
        self.tree.heading("Location", text='Location')
        self.tree.heading("Issued", text='Issued')
        self.tree.heading("Issue Date", text='Issued Date')
        self.tree.heading("Return Date", text='Return Date')

        self.tree.column("Book ID", width=WIDTH, anchor=tk.CENTER)
        self.tree.column("Title", width=WIDTH, anchor=tk.CENTER)
        self.tree.column("Author", width=WIDTH, anchor=tk.CENTER)
        self.tree.column("Genre", width=WIDTH, anchor=tk.CENTER)
        self.tree.column("Location", width=WIDTH, anchor=tk.CENTER)
        self.tree.column("Issued", width=WIDTH, anchor=tk.CENTER)
        self.tree.column("Issue Date", width=WIDTH, anchor=tk.CENTER)
        self.tree.column("Return Date", width=WIDTH, anchor=tk.CENTER)

        # Run database fetch function
        db_fetch = self.database_fetch()

        # Extract return values from function.
        bookID_list = db_fetch[0]
        title_list = db_fetch[1]
        author_list = db_fetch[2]
        genre_list = db_fetch[3]
        location_list = db_fetch[4]
        issued_list = db_fetch[5]

        # Delete all rows on the table to start with a fresh table.
        for k in self.tree.get_children():
            self.tree.delete(k)

        # Populate the table with all the relevant information in the database,
        # by iterating over the information of each book and adding it onto the table.
        for i in range(len(bookID_list)):
            # Issue Date
            c.execute("SELECT date_issued FROM MyBooks WHERE user_id=(SELECT user_id WHERE bookID=?)",(bookID_list[i],))
            date_issued_fetch = c.fetchall()
            date_issued_list = [x[0] for x in date_issued_fetch]

            # Return Date
            c.execute("SELECT return_date FROM MyBooks WHERE user_id=(SELECT user_id WHERE bookID=?)",(bookID_list[i],))
            return_date_fetch = c.fetchall()
            return_date_list = [x[0] for x in return_date_fetch]

            # Check if the current book iteration has an issue date and therefore a return date.
            if len(date_issued_list)==0 or len(return_date_list)==0:
                # No issue date, then set the corresponding issue_date and return_date column values to N/A
                self.tree_ids.append(self.tree.insert("", "end", values=(bookID_list[i], title_list[i], author_list[i], genre_list[i], location_list[i], issued_list[i], 'N/A', 'N/A')))
            else:
                # Issue date and return date exists, therefore set them on the table.
                self.tree_ids.append(self.tree.insert("", "end", values=(bookID_list[i], title_list[i], author_list[i], genre_list[i], location_list[i], issued_list[i], date_issued_list[0], return_date_list[0])))
        self.tree.pack()

        # Search the Treeview Container
        self.db_search_container = tk.Frame(tree_container)
        self.db_search_container.pack(side=tk.BOTTOM, anchor=tk.N, padx=PADX, pady=PADY)

        # BookID Search DB
        db_search_label_bookID = tk.Label(self.db_search_container, text='ID: ', bg=BG)
        db_search_label_bookID.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self._detached = set()
        self.db_search_bookID_var = tk.StringVar()
        self.db_search_bookID_var.trace("w", self._columns_searcher)

        self.db_search_bookID_entry = ttk.Entry(self.db_search_container, textvariable=self.db_search_bookID_var)
        self.db_search_bookID_entry.pack(side=tk.LEFT, anchor=tk.E, padx=PADX, pady=PADY)

        # Title Search DB
        db_search_label_title = tk.Label(self.db_search_container, text='Title: ', bg=BG)
        db_search_label_title.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.db_search_title_var = tk.StringVar()
        self.db_search_title_var.trace("w", self._columns_searcher)

        self.db_search_title_entry = ttk.Entry(self.db_search_container, textvariable=self.db_search_title_var)
        self.db_search_title_entry.pack(side=tk.LEFT, anchor=tk.E, padx=PADX, pady=PADY)

        # Author Search DB
        db_search_label_author = tk.Label(self.db_search_container, text='Author: ', bg=BG)
        db_search_label_author.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.db_search_author_var = tk.StringVar()
        self.db_search_author_var.trace("w", self._columns_searcher)

        self.db_search_author_entry = ttk.Entry(self.db_search_container, textvariable=self.db_search_author_var)
        self.db_search_author_entry.pack(side=tk.LEFT, anchor=tk.E, padx=PADX, pady=PADY)

        # Genre Search DB
        db_search_label_genre = tk.Label(self.db_search_container, text='Genre: ', bg=BG)
        db_search_label_genre.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.db_search_genre_var = tk.StringVar()
        self.db_search_genre_var.set("-EMPTY-")

        from functools import partial
        self.db_search_genre_menu = ttk.OptionMenu(self.db_search_container, self.db_search_genre_var, genre_choice_list[0], *genre_choice_list, command=partial(self._columns_searcher))
        self.db_search_genre_menu.pack(side=tk.LEFT, anchor=tk.E, padx=PADX, pady=PADY)

        # Location Search DB
        db_search_label_location = tk.Label(self.db_search_container, text='Location: ', bg=BG)
        db_search_label_location.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.db_search_location_var = tk.StringVar()
        self.db_search_location_var.set("-EMPTY-")
        self.db_search_location_var.trace("w", self._columns_searcher)

        self.db_search_location_menu = ttk.OptionMenu(self.db_search_container, self.db_search_location_var, location_choice_list[0], *location_choice_list)
        self.db_search_location_menu.pack(side=tk.LEFT, anchor=tk.E, padx=PADX, pady=PADY)

        # Issued Search DB
        db_search_label_issued = tk.Label(self.db_search_container, text='Issued(1/0): ', bg=BG)
        db_search_label_issued.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.db_search_issued_var = tk.StringVar()
        self.db_search_issued_var.set("-EMPTY-")
        self.db_search_issued_var.trace('w', self._columns_searcher_issued)

        self.db_search_issued_menu = ttk.OptionMenu(self.db_search_container, self.db_search_issued_var, issued_choice_list[0], *issued_choice_list)
        self.db_search_issued_menu.pack(side=tk.LEFT, anchor=tk.E, padx=PADX, pady=PADY)

        # For each column in the list of columns, call the function that sorts each column.
        # Each column will be sorted according to its inherent data type. (integers sorted numerically, strings sorted alphabetically)
        # Sort function described in more detail in the function.
        for self.col in self.columns:
                self.tree.heading(self.col, text=self.col,
                                      command=lambda c=self.col: self.sort_upon_press(c))

        # Issue/Return Books UI
        filter_container = tk.Frame(book_database_page, bg=BG)
        filter_container.pack(side=tk.LEFT, anchor=tk.N, padx=PADX, pady=PADY)

        filter_header = tk.Label(filter_container, text='Issue Book', font=FONT, bg=BG)
        filter_header.pack(anchor=tk.W, padx=PADX, pady=PADY)

        # BookID Entry Field
        self.search_container_bookID = tk.Frame(filter_container, bg=BG)
        self.search_container_bookID.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        bookID_label = tk.Label(self.search_container_bookID, text='ID: ', bg=BG)
        bookID_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.bookID_reg = root.register(self.bookID_validate)
        self.bookID_var = tk.StringVar()

        self.bookID_entry = ttk.Entry(self.search_container_bookID)
        self.bookID_entry.config(textvariable=self.bookID_var, validate="key",
                            validatecommand=(self.bookID_reg, "%P"))
        self.bookID_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        #  Filler frame for the autocomplete function
        self.search_container_canvas = tk.Canvas(filter_container, height=50, width=50, bg=BG)
        self.search_container_canvas.pack(fill=tk.X, expand=True)

        self.search_container_autocomplete = tk.Frame(self.search_container_canvas, bg=BG)
        self.search_container_autocomplete.pack(anchor=tk.W, fill=tk.X, side=tk.TOP)

        # Title Entry Field
        self.search_container_title = tk.Frame(filter_container, bg=BG)
        self.search_container_title.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        title_label = tk.Label(self.search_container_title, text='Title: ', bg=BG)
        title_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.title_var = tk.StringVar()

        self.title_entry = ttk.Entry(self.search_container_title, textvariable=self.title_var)
        self.title_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # Author Entry Field
        self.search_container_author = tk.Frame(filter_container, bg=BG)
        self.search_container_author.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        author_label = tk.Label(self.search_container_author, text='Author: ', bg=BG)
        author_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.author_var = tk.StringVar()

        self.author_entry = ttk.Entry(self.search_container_author, textvariable=self.author_var, state=tk.DISABLED)
        self.author_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # Book recipient frame
        recipient_container = tk.Frame(filter_container, bg=BG)
        recipient_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        recipient_label = tk.Label(recipient_container, text='Recipient Email: ', bg=BG)
        recipient_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.recipient_var = tk.StringVar()

        recipient_entry = ttk.Entry(recipient_container, textvariable=self.recipient_var)
        recipient_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # Date entry frame
        issue_date_container = tk.Frame(filter_container, bg=BG)
        issue_date_container.pack(anchor=tk.W, fill=tk.X, expand=True)

        recipient_label = tk.Label(issue_date_container, text='Date of Issuing: ', bg=BG)
        recipient_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.issue_date_entry = DateEntry(issue_date_container, width=12, background='darkblue',
                    foreground='white', borderwidth=2, mindate=datetime.now(), maxdate=datetime.now(), locale='en_UK')
        self.issue_date_entry.pack(padx=PADX, pady=PADY)

        # Return date frame
        return_date_container = tk.Frame(filter_container, bg=BG)
        return_date_container.pack(anchor=tk.W, fill=tk.X, expand=True)

        return_date_label = tk.Label(return_date_container, text='Expected Return Date: ', bg=BG)
        return_date_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        three_months_from_now = relativedelta(months=3)
        return_date_calc = self.issue_date_entry.get_date() + three_months_from_now

        self.actual_return_date_entry = DateEntry(return_date_container, width=12, background='darkblue',
                    foreground='white', borderwidth=2, mindate=datetime.now(), maxdate=return_date_calc, locale='en_UK')
        self.actual_return_date_entry.pack(padx=PADX, pady=PADY)

        # Issue Book Button Frame
        issue_book_container = tk.Frame(filter_container, bg=BG)
        issue_book_container.pack(anchor=tk.W, fill=tk.X, expand=True)

        issue_book_btn = ttk.Button(issue_book_container)
        issue_book_btn.config(text='    Issue Book    ', command=self.issue_book)
        issue_book_btn.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        #  Gather an updated list of books to be displayed correctly on the autocomplete box.
        #  Send all the required variables to allow the autocomplete function to manipulate the entry data the user is entering and find the closest match, as well as manipulating the window that it displays the autocomplete information in.
        AutoCompleteEntryBD_IssueBookID(self.search_container_autocomplete, self.title_entry, self.title_var, self.author_entry, self.author_var, self.bookID_var, self.bookID_entry, self.search_container_canvas)

        # # #  Book Return ('ret' following the variable name is short for 'return' to differentiate between the variables above and below)
        # Return Books UI
        ret_filter_container = tk.Frame(book_database_page, bg=BG)
        ret_filter_container.pack(side=tk.LEFT, anchor=tk.N, padx=PADX, pady=PADY)

        ret_filter_header = tk.Label(ret_filter_container, text='Return Book', font=FONT, bg=BG)
        ret_filter_header.pack(anchor=tk.W, padx=PADX, pady=PADY)

        # BookID Entry Field
        self.ret_search_container_bookID = tk.Frame(ret_filter_container, bg=BG)
        self.ret_search_container_bookID.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        ret_bookID_label = tk.Label(self.ret_search_container_bookID, text='ID: ', bg=BG)
        ret_bookID_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.ret_bookID_reg = root.register(self.ret_bookID_validate)
        self.ret_bookID_var = tk.StringVar()

        self.ret_bookID_entry = ttk.Entry(self.ret_search_container_bookID)
        self.ret_bookID_entry.config(textvariable=self.ret_bookID_var, validate="key",
                            validatecommand=(self.ret_bookID_reg, "%P"))
        self.ret_bookID_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # Filler frame for the autocomplete function
        self.ret_search_container_canvas = tk.Canvas(ret_filter_container, height=50, width=50, bg=BG)
        self.ret_search_container_canvas.pack(fill=tk.X, expand=True)

        self.ret_search_container_autocomplete = tk.Frame(self.ret_search_container_canvas, bg=BG)
        self.ret_search_container_autocomplete.pack(anchor=tk.W, fill=tk.X, side=tk.TOP)

        # Title Entry Field
        self.ret_search_container_title = tk.Frame(ret_filter_container, bg=BG)
        self.ret_search_container_title.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        ret_title_label = tk.Label(self.ret_search_container_title, text='Title: ', bg=BG)
        ret_title_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.ret_title_var = tk.StringVar()

        self.ret_title_entry = ttk.Entry(self.ret_search_container_title, textvariable=self.ret_title_var)
        self.ret_title_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # Author Entry Field
        self.ret_search_container_author = tk.Frame(ret_filter_container, bg=BG)
        self.ret_search_container_author.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        ret_author_label = tk.Label(self.ret_search_container_author, text='Author: ', bg=BG)
        ret_author_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.ret_author_var = tk.StringVar()

        self.ret_author_entry = ttk.Entry(self.ret_search_container_author, textvariable=self.ret_author_var, state=tk.DISABLED)
        self.ret_author_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # Book recipient frame
        ret_recipient_container = tk.Frame(ret_filter_container, bg=BG)
        ret_recipient_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        ret_recipient_label = tk.Label(ret_recipient_container, text='Return Email: ', bg=BG)
        ret_recipient_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.return_email_var = tk.StringVar()

        ret_recipient_entry = ttk.Entry(ret_recipient_container, textvariable=self.return_email_var)
        ret_recipient_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # Date entry frame
        ret_date_container = tk.Frame(ret_filter_container, bg=BG)
        ret_date_container.pack(anchor=tk.W, fill=tk.X, expand=True)

        ret_recipient_label = tk.Label(ret_date_container, text='Date of Return: ', bg=BG)
        ret_recipient_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.ret_date_entry = DateEntry(ret_date_container, width=12, background='darkblue',
                    foreground='white', borderwidth=2, mindate=datetime.now(), maxdate=datetime.now(), locale='en_UK')
        self.ret_date_entry.pack(padx=PADX, pady=PADY)

        # Return Book Button Frame
        return_book_container = tk.Frame(ret_filter_container, bg=BG)
        return_book_container.pack(anchor=tk.W, fill=tk.X, expand=True)

        return_book_btn = ttk.Button(return_book_container)
        return_book_btn.config(text='    Return Book    ', command=self.return_book)
        return_book_btn.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        #  Send all the required variables to allow the autocomplete function to manipulate the entry data the user is entering and find the closest match, as well as manipulating the window that it displays the autocomplete information in.
        AutoCompleteEntryBD_ReturnBookID(self.ret_search_container_autocomplete, self.ret_title_entry, self.ret_title_var, self.ret_author_entry, self.ret_author_var, self.ret_bookID_var, self.ret_bookID_entry, self.ret_date_entry, self.ret_search_container_canvas)

        # Remove Books UI
        remove_book_container = tk.Frame(book_database_page, bg=BG)
        remove_book_container.pack(side=tk.RIGHT, anchor=tk.N, padx=PADX, pady=PADY)

        remove_book_header = tk.Label(remove_book_container, text='Remove Book From System', font=FONT, bg=BG)
        remove_book_header.pack(anchor=tk.W, padx=PADX, pady=PADY)

        # BookID Entry Field
        self.remove_container_bookID = tk.Frame(remove_book_container, bg=BG)
        self.remove_container_bookID.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        remove_bookID_label = tk.Label(self.remove_container_bookID, text='ID: ', bg=BG)
        remove_bookID_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.remove_bookID_reg = root.register(self.remove_bookID_validate)
        self.remove_bookID_var = tk.StringVar()

        self.remove_bookID_entry = ttk.Entry(self.remove_container_bookID)
        self.remove_bookID_entry.config(textvariable=self.remove_bookID_var, validate="key",
                            validatecommand=(self.remove_bookID_reg, "%P"))
        self.remove_bookID_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # Filler frame for the autocomplete function
        self.remove_container_canvas = tk.Canvas(remove_book_container, height=50, width=50, bg=BG)
        self.remove_container_canvas.pack(fill=tk.X, expand=True)

        self.remove_container_autocomplete = tk.Frame(self.remove_container_canvas, bg=BG)
        self.remove_container_autocomplete.pack(anchor=tk.W, fill=tk.X, side=tk.TOP)

        # Title Entry Field
        self.remove_container_title = tk.Frame(remove_book_container, bg=BG)
        self.remove_container_title.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        remove_title_label = tk.Label(self.remove_container_title, text='Title: ', bg=BG)
        remove_title_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.remove_title_var = tk.StringVar()

        self.remove_title_entry = ttk.Entry(self.remove_container_title, textvariable=self.remove_title_var)
        self.remove_title_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # Author Entry Field
        self.remove_container_author = tk.Frame(remove_book_container, bg=BG)
        self.remove_container_author.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        remove_author_label = tk.Label(self.remove_container_author, text='Author: ', bg=BG)
        remove_author_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.remove_author_var = tk.StringVar()

        self.remove_author_entry = ttk.Entry(self.remove_container_author, textvariable=self.remove_author_var, state=tk.DISABLED)
        self.remove_author_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # Genre Entry Field
        self.remove_container_genre = tk.Frame(remove_book_container, bg=BG)
        self.remove_container_genre.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        remove_genre_label = tk.Label(self.remove_container_genre, text='Genre: ', bg=BG)
        remove_genre_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.remove_genre_var = tk.StringVar()
        self.remove_genre_var.set("-EMPTY-")

        self.remove_genre_menu = ttk.OptionMenu(self.remove_container_genre, self.remove_genre_var, genre_choice_list[0], *genre_choice_list)
        self.remove_genre_menu.configure(state=tk.DISABLED)
        self.remove_genre_menu.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # Remove Book Button Frame
        remove_book_container = tk.Frame(remove_book_container, bg=BG)
        remove_book_container.pack(anchor=tk.W, fill=tk.X, expand=True)

        remove_book_btn = ttk.Button(remove_book_container)
        remove_book_btn.config(text='    Remove Book    ', command=self.remove_book)
        remove_book_btn.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        #  Send all the required variables to allow the autocomplete function to manipulate the entry data the user is entering and find the closest match, as well as manipulating the window that it displays the autocomplete information in.
        AutoCompleteEntryBD_RemoveBookID(self.remove_container_autocomplete, self.remove_title_entry, self.remove_title_var,self.remove_author_entry, self.remove_author_var, self.remove_bookID_var, self.remove_bookID_entry, self.remove_genre_var, self.remove_genre_menu, self.remove_container_canvas)

        # Add Books UI
        add_book_container = tk.Frame(book_database_page, bg=BG)
        add_book_container.pack(side=tk.RIGHT, anchor=tk.N, padx=PADX, pady=PADY)

        add_book_header = tk.Label(add_book_container, text='Add Book Into System', font=FONT, bg=BG)
        add_book_header.pack(anchor=tk.W, padx=PADX, pady=PADY)

        # BookID Entry Field
        self.add_container_bookID = tk.Frame(add_book_container, bg=BG)
        self.add_container_bookID.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        add_bookID_label = tk.Label(self.add_container_bookID, text='ID: ', bg=BG)
        add_bookID_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.add_bookID_var = tk.StringVar()

        select_highest_val = c.execute('SELECT MAX(bookID) + 1 FROM Books').fetchall()
        highest_val = [x[0] for x in select_highest_val][0]

        self.add_bookID_var.set(highest_val)

        self.add_bookID_entry = ttk.Entry(self.add_container_bookID, textvariable=self.add_bookID_var, state=tk.DISABLED)
        self.add_bookID_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # Title Entry Field
        self.add_container_title = tk.Frame(add_book_container, bg=BG)
        self.add_container_title.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        add_title_label = tk.Label(self.add_container_title, text='Title: ', bg=BG)
        add_title_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.add_title_var = tk.StringVar()

        self.add_title_entry = ttk.Entry(self.add_container_title, textvariable=self.add_title_var)
        self.add_title_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # Author Entry Field
        self.add_container_author = tk.Frame(add_book_container, bg=BG)
        self.add_container_author.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        add_author_label = tk.Label(self.add_container_author, text='Author: ', bg=BG)
        add_author_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.add_author_var = tk.StringVar()

        self.add_author_entry = ttk.Entry(self.add_container_author, textvariable=self.add_author_var)
        self.add_author_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # Genre Entry Field
        self.add_container_genre = tk.Frame(add_book_container, bg=BG)
        self.add_container_genre.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        add_genre_label = tk.Label(self.add_container_genre, text='Genre: ', bg=BG)
        add_genre_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.add_genre_var = tk.StringVar()
        self.add_genre_var.set("-EMPTY-")

        self.add_genre_menu = ttk.OptionMenu(self.add_container_genre, self.add_genre_var,genre_choice_list[0], *genre_choice_list)
        self.add_genre_menu.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # Add Book Button Frame
        add_book_container_button = tk.Frame(add_book_container, bg=BG)
        add_book_container_button.pack(anchor=tk.W, fill=tk.X, expand=True)

        add_book_btn = ttk.Button(add_book_container_button)
        add_book_btn.config(text='    Add Book    ', command=self.add_book)
        add_book_btn.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        # Add New Genre Entry Field
        self.container_newgenre = tk.Frame(add_book_container, bg=BG)
        self.container_newgenre.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        newgenre_main_label = tk.Label(self.container_newgenre, text='Manage Genres', font=FONT, bg=BG)
        newgenre_main_label.pack(anchor=tk.W, padx=PADX, pady=PADY)

        newgenre_label = tk.Label(self.container_newgenre, text='Genre Name: ', bg=BG)
        newgenre_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.newgenre_var = tk.StringVar()

        self.newgenre_entry = ttk.Entry(self.container_newgenre, textvariable=self.newgenre_var)
        self.newgenre_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # Add New Genre Button Frame
        container_newgenre_button = tk.Frame(add_book_container, bg=BG)
        container_newgenre_button.pack(anchor=tk.W, fill=tk.X, expand=True)

        add_newgenre_btn = ttk.Button(container_newgenre_button)
        add_newgenre_btn.config(text='    Add New Genre    ', command=self.add_newgenre)
        add_newgenre_btn.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        remove_newgenre_btn = ttk.Button(container_newgenre_button)
        remove_newgenre_btn.config(text='    Remove Genre    ', command=self.remove_newgenre)
        remove_newgenre_btn.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

    def add_newgenre(self):
        '''
        Called when the staff presses the button for a new genre to be added.
        Sends the information to the database and updates the dropdown genre selection menus.
        '''
        # Requires input validation

        # Fetch entry field values
        newgenre_var = self.newgenre_var.get()

        # Check if the entered genre already exists
        c.execute("SELECT genre FROM Genres")
        genres_list_fetch = c.fetchall()
        genre_choice_list = [x[0] for x in genres_list_fetch]

        if newgenre_var in genre_choice_list:
            ms.showerror('Error', 'This genre is already in the system.')
        else:
            # Add new genre to db
            insert_newgenre = 'INSERT INTO Genres(genre) VALUES(?)'
            c.execute(insert_newgenre, [(newgenre_var)])
            conn.commit()

            # Update genre_choice_list and the related OptionMenus
            # List of genres
            c.execute("SELECT genre FROM Genres")
            genres_list_fetch = c.fetchall()
            genre_choice_list = [x[0] for x in genres_list_fetch]

            # Update Add Book OptionMenu in BookDB Page
            add_menu = self.add_genre_menu["menu"]
            add_menu.delete(0, tk.END)
            for _string in genre_choice_list:
                add_menu.add_command(label=_string,
                                 command=lambda value=_string: self.add_genre_var.set(value))

            # Update Remove Book OptionMenu in BookDB Page
            remove_menu = self.remove_genre_menu["menu"]
            remove_menu.delete(0, tk.END)
            for _string in genre_choice_list:
                remove_menu.add_command(label=_string,
                                 command=lambda value=_string: self.add_genre_var.set(value))

            # Update genre search in bookDB page
            search_genre_menu = self.db_search_genre_menu["menu"]
            search_genre_menu.delete(0, tk.END)
            for _string in genre_choice_list:
                search_genre_menu.add_command(label=_string,
                                 command=lambda value=_string: self.db_search_genre_var.set(value))

            ms.showinfo('Success', 'Genre added to the database successfully')

    def remove_newgenre(self):
        '''
        Called when the staff presses the button for a genre to be removed.
        Sends the information to the database and updates the dropdown genre selection menus.
        '''
        # Requires input validation

        # Fetch entry field values
        newgenre_var = self.newgenre_var.get()

        # Check if the entered genre already exists
        c.execute("SELECT genre FROM Genres")
        genres_list_fetch = c.fetchall()
        genre_choice_list = [x[0] for x in genres_list_fetch]

        if newgenre_var not in genre_choice_list:
            ms.showerror('Error', "This genre isn't in the system.")
        elif newgenre_var == '-EMPTY-':
            ms.showerror("Error", "You cannot remove this genre.")
        else:
            # Find if the genre is being used by any books
            used_genre_fetch = c.execute('SELECT genre FROM Books WHERE genre=?', (newgenre_var,)).fetchall()
            used_genre = [x[0] for x in used_genre_fetch]

            if len(used_genre) > 0:
                ms.showerror('Error','Genre is currently in use by other books')
            else:
                # Remove new genre from db
                c.execute('DELETE FROM Genres WHERE genre=?', (newgenre_var,))
                conn.commit()

                # Update genre_choice_list and the related OptionMenus
                # List of genres
                c.execute("SELECT genre FROM Genres")
                genres_list_fetch = c.fetchall()
                genre_choice_list = [x[0] for x in genres_list_fetch]

                add_menu = self.add_genre_menu["menu"]
                add_menu.delete(0, tk.END)
                for _string in genre_choice_list:
                    add_menu.add_command(label=_string,
                                            command=lambda value=_string: self.remove_genre_var.set(value))

                # Update Remove Book OptionMenu in BookDB Page
                remove_menu = self.remove_genre_menu["menu"]
                remove_menu.delete(0, tk.END)
                for _string in genre_choice_list:
                    remove_menu.add_command(label=_string,
                                     command=lambda value=_string: self.remove_genre_var.set(value))

                # Update genre search in bookDB page
                search_genre_menu = self.db_search_genre_menu["menu"]
                search_genre_menu.delete(0, tk.END)
                for _string in genre_choice_list:
                    search_genre_menu.add_command(label=_string,
                                     command=lambda value=_string: self.db_search_genre_var.set(value))

                ms.showinfo('Success', 'Genre removed from the database successfully')

    def add_book(self):
        '''
        Called when the staff presses the button for a book to be added into the system.
        Sends the information to the database and updates the treeview table.
        '''

        # Fetch entry field values
        add_bookID_var = self.add_bookID_var.get()
        add_title_var = self.add_title_var.get()
        add_author_var = self.add_author_var.get()
        add_genre_var = self.add_genre_var.get()

        # The location of the book within the physical library, will be based on the first letter of its Title.
        # The shelves will be split into 27 different locations (alphabet + an '*' to signify any book whose title doesn't start with an alphabetical character.)
        # Example, Title= 1 step closer. Location=*
        # Example 2, Title=Drowning, Location=D

        # Iterate over the alphabet to find the letter that the first letter of the title matches.
        for letter in string.ascii_uppercase:
            if letter == add_title_var[0]:
                location = letter
            elif add_title_var[0] not in string.ascii_uppercase:
                # If the letter does not match an alphabetical character.
                location = '*'

        # Insert fetched values into database
        insert_book_info = 'INSERT INTO Books(bookID, title, author, genre, issued, location) VALUES(?,?,?,?,0,?)'
        c.execute(insert_book_info,[(add_bookID_var), (add_title_var), (add_author_var), (add_genre_var), (location)])
        conn.commit()

        # Increase the displayed bookID on the Add Book section
        select_highest_val = c.execute('SELECT MAX(bookID) + 1 FROM Books').fetchall()
        highest_val = [x[0] for x in select_highest_val][0]

        self.add_bookID_var.set(highest_val)

        # Set entryfields to empty after addition
        self.add_title_var.set('')
        self.add_author_var.set('')

        # Run database fetch function
        db_fetch = self.database_fetch()

        # Extract return values from function.
        bookID_list = db_fetch[0]
        title_list = db_fetch[1]
        author_list = db_fetch[2]
        genre_list = db_fetch[3]
        location_list = db_fetch[4]
        issued_list = db_fetch[5]

        for k in self.tree.get_children():
            self.tree.delete(k)

        for i in range(len(bookID_list)):
            # Issue Date
            c.execute("SELECT date_issued FROM MyBooks WHERE user_id=(SELECT user_id WHERE bookID=?)", (bookID_list[i],))
            date_issued_fetch = c.fetchall()
            date_issued_list = [x[0] for x in date_issued_fetch]

            # Return Date
            c.execute("SELECT return_date FROM MyBooks WHERE user_id=(SELECT user_id WHERE bookID=?)", (bookID_list[i],))
            return_date_fetch = c.fetchall()
            return_date_list = [x[0] for x in return_date_fetch]

            # creates an entry in the tree for each element of the list
            # then stores the id of the tree in the self.ids list
            if len(date_issued_list)==0 or len(return_date_list)==0:
                self.tree_ids.append(self.tree.insert("", "end", values=(bookID_list[i], title_list[i], author_list[i], genre_list[i], location_list[i], issued_list[i], 'N/A', 'N/A')))
            else:
                self.tree_ids.append(self.tree.insert("", "end", values=(bookID_list[i], title_list[i], author_list[i], genre_list[i], location_list[i], issued_list[i], date_issued_list[0], return_date_list[0])))
        self.tree.pack()

        for self.col in self.columns:
                self.tree.heading(self.col, text=self.col,
                                      command=lambda c=self.col: self.sort_upon_press(c))

        ms.showinfo('Success', 'Book added to the database successfully')

    def remove_book(self):
        '''
        Called when the staff presses the button to remove a book from the system.
        Sends the information to the database and updates the treeview table.
        '''

        # Fetch entry field values
        remove_bookID_var = self.remove_bookID_var.get()

        # Delete the book with said book ID
        c.execute('DELETE FROM Books WHERE bookID=?', (remove_bookID_var,))
        conn.commit()

        # Check if anyone owns said book and remove it from their My Books table
        check_book_owned = c.execute('SELECT user_id FROM MyBooks WHERE bookID=?', (remove_bookID_var,)).fetchall()
        book_owner = [x[0] for x in check_book_owned]

        if len(book_owner) == 1:
            c.execute('DELETE FROM MyBooks WHERE bookID=?',(remove_bookID_var,))
            conn.commit()

        # Set entryfields to empty after removal
        self.remove_bookID_var.set('')
        self.remove_title_var.set('')
        self.remove_author_var.set('')

        # Run database fetch function
        db_fetch = self.database_fetch()

        # Extract return values from function.
        bookID_list = db_fetch[0]
        title_list = db_fetch[1]
        author_list = db_fetch[2]
        genre_list = db_fetch[3]
        location_list = db_fetch[4]
        issued_list = db_fetch[5]

        for k in self.tree.get_children():
            self.tree.delete(k)

        for i in range(len(bookID_list)):
            # Issue Date
            c.execute("SELECT date_issued FROM MyBooks WHERE user_id=(SELECT user_id WHERE bookID=?)", (bookID_list[i],))
            date_issued_fetch = c.fetchall()
            date_issued_list = [x[0] for x in date_issued_fetch]

            # Return Date
            c.execute("SELECT return_date FROM MyBooks WHERE user_id=(SELECT user_id WHERE bookID=?)", (bookID_list[i],))
            return_date_fetch = c.fetchall()
            return_date_list = [x[0] for x in return_date_fetch]

            # creates an entry in the tree for each element of the list
            # then stores the id of the tree in the self.ids list
            if len(date_issued_list)==0 or len(return_date_list)==0:
                self.tree_ids.append(self.tree.insert("", "end", values=(bookID_list[i], title_list[i], author_list[i], genre_list[i], location_list[i], issued_list[i], 'N/A', 'N/A')))
            else:
                self.tree_ids.append(self.tree.insert("", "end", values=(bookID_list[i], title_list[i], author_list[i], genre_list[i], location_list[i], issued_list[i], date_issued_list[0], return_date_list[0])))
        self.tree.pack()

        for self.col in self.columns:
                self.tree.heading(self.col, text=self.col,
                                      command=lambda c=self.col: self.sort_upon_press(c))

        ms.showinfo('Success', 'Book removed from the database successfully')

    def issue_book(self):
        '''
        Called when the staff presses the button to issue a book to a target user.
        Sends the information to the database and updates the treeview table.
        '''

        # Get all relevant entry values.
        bookID_var = self.bookID_var.get()
        title_var = self.title_var.get()
        author_var = self.author_var.get()
        recipient_email = self.recipient_var.get()
        date_issued = self.issue_date_entry.get_date()

        # Convert date object into a string for easier manipulation.
        date_issued_string = str(date_issued.strftime('%Y-%m-%d'))

        # Check if the string date is equal to the date today.
        if str(date_issued_string) == str(datetime.today().strftime('%Y-%m-%d')):

            # Get the excepted, target return date.
            expected_return_date = self.actual_return_date_entry.get_date()

            # Fetch the bookID that matches the title and author
            book_id_search = c.execute('SELECT bookID FROM Books WHERE title=? AND author=? ', (title_var, author_var)).fetchall()
            book_id = [x[0] for x in book_id_search][0]

            # Check if the patron that wants to take the book out has an account, by checking
            # if the staff member leaves the recipient email field empty, then that means to
            # take the book out under no account, but still store the information of the 'transaction'.
            if recipient_email == '':
                # The patron has no account.
                # Check if book is already issued out
                book_already_issued_fetch = c.execute('SELECT issued FROM Books WHERE bookID=?', (bookID_var,)).fetchall()
                book_already_issued = [x[0] for x in book_already_issued_fetch][0]

                if book_already_issued == 0:
                    # No need to insert the book into the MyBooks table.

                    # Check if the user meant to leave this field empty.
                    confirm_action = ms.askquestion("No Account Issuing", "You are about to issue a book to a patron with no account.\nAre you sure you want to continue?")
                    if confirm_action == "yes":
                        # Update that it is currently issued on the Books table.
                        c.execute('UPDATE Books SET issued=1 WHERE bookID=?', (book_id,))
                        conn.commit()

                        ms.showinfo('Success', 'Book Issued Successfully.')

                        # Set entryfields to empty after issue
                        self.bookID_var.set('')
                        self.title_var.set('')
                        self.author_var.set('')
                        self.recipient_var.set('')

                        # update treeview BookDatabase when the book is issued
                        # gather db info to check if book has been issued, so that we only show the books that have NOT been issued.

                        # Run database fetch function
                        db_fetch = self.database_fetch()

                        # Extract return values from function.
                        bookID_list = db_fetch[0]
                        title_list = db_fetch[1]
                        author_list = db_fetch[2]
                        genre_list = db_fetch[3]
                        location_list = db_fetch[4]
                        issued_list = db_fetch[5]

                        # Delete all rows in the tree.
                        for k in self.tree.get_children():
                            self.tree.delete(k)

                        # Iterate over each bookID in the database table and populate the table one row at a time.
                        for i in range(len(bookID_list)):
                            # Issue Date
                            c.execute("SELECT date_issued FROM MyBooks WHERE user_id=(SELECT user_id WHERE bookID=?)", (bookID_list[i],))
                            date_issued_fetch = c.fetchall()
                            date_issued_list = [x[0] for x in date_issued_fetch]

                            # Return Date
                            c.execute("SELECT return_date FROM MyBooks WHERE user_id=(SELECT user_id WHERE bookID=?)", (bookID_list[i],))
                            return_date_fetch = c.fetchall()
                            return_date_list = [x[0] for x in return_date_fetch]

                            if len(date_issued_list) == 0 or len(return_date_list) == 0:
                                self.tree_ids.append(self.tree.insert("", "end", values=(bookID_list[i], title_list[i], author_list[i], genre_list[i], location_list[i], issued_list[i], 'N/A', 'N/A')))
                            else:
                                self.tree_ids.append(self.tree.insert("", "end", values=(bookID_list[i], title_list[i], author_list[i], genre_list[i], location_list[i], issued_list[i], date_issued_list[0], return_date_list[0])))
                        self.tree.pack()

                        for self.col in self.columns:
                            self.tree.heading(self.col, text=self.col,
                                                  command=lambda c=self.col: self.sort_upon_press(c))
                    else:
                        ms.showwarning('Alert', 'Issuing Cancelled')
                else:
                    ms.showerror('Error', 'This book has already been issued.')
            elif recipient_email != '':
                #  Send info to database
                account_info_fetch = c.execute('SELECT * FROM Accounts WHERE email_address=?', (recipient_email,)).fetchall()
                if len(account_info_fetch) != 0:
                    accounts_userid_check = [x[0] for x in account_info_fetch][0]

                    # Check if book is already issued out
                    book_already_issued_fetch = c.execute('SELECT issued FROM Books WHERE bookID=?', (bookID_var,)).fetchall()
                    book_already_issued = [x[0] for x in book_already_issued_fetch][0]

                    if book_already_issued == 0:
                        # Insert the book information into the MyBooks table under the given user id, if the book issued status is 0
                        insert_my_bookID = 'INSERT INTO MyBooks(user_id,bookID) VALUES(?,?)'
                        c.execute(insert_my_bookID, [(accounts_userid_check), (book_id)])
                        conn.commit()

                        # Followed by updating said book to be issued after inserting it above.
                        c.execute('UPDATE Books SET issued=1 WHERE bookID=?', (book_id,))
                        conn.commit()

                        # Update the issue date to the current date.
                        c.execute("""UPDATE MyBooks
                            SET date_issued=?
                            WHERE user_id = (SELECT user_id FROM Accounts WHERE email_address=?)
                            AND bookID=?""" , (date_issued, recipient_email, bookID_var))
                        conn.commit()

                        # Update the return date to the target return date set by the staff.
                        c.execute("""UPDATE MyBooks
                            SET return_date=?
                            WHERE user_id = (SELECT user_id FROM Accounts WHERE email_address=?)
                            AND bookID=?""", (expected_return_date, recipient_email, bookID_var))
                        conn.commit()

                        # Fetch Location
                        book_location_fetch = c.execute("SELECT location FROM Books WHERE bookID=?", (bookID_var,)).fetchall()
                        book_location = [x[0] for x in book_location_fetch][0]

                        # Fetch genre
                        book_genre_fetch = c.execute("SELECT genre FROM Books WHERE bookID=?", (bookID_var,)).fetchall()
                        book_genre = [x[0] for x in book_genre_fetch][0]

                        # Call the email class from the email_sys file.
                        e = Email()
                        # Establish the Google API connection.
                        service = e.get_service()
                        # Create the message along with passing any additional information that must go on the message.
                        message = e.create_issuing_message("from@gmail.com", recipient_email, "Books4All Book Issued", title_var, author_var, book_genre, book_location, date_issued, expected_return_date)
                        # Send the message.
                        e.send_message(service, "from@gmail.com", message)

                        ms.showinfo('Success', 'Book issued out successfully\nAn email has been sent to\n'+recipient_email+'\nregarding the issuing information.')
                    else:
                        ms.showerror('Error', 'This book has already been issued.')

                else:
                    ms.showerror("Error", "Account does not exist")

                # Set entryfields to empty after issue
                self.bookID_var.set('')
                self.title_var.set('')
                self.author_var.set('')
                self.recipient_var.set('')

                # update treeview BookDatabase when the book is issued
                # gather db info to check if book has been issued, so that we only show the books that have NOT been issued.

                # Run database fetch function
                db_fetch = self.database_fetch()

                # Extract return values from function.
                bookID_list = db_fetch[0]
                title_list = db_fetch[1]
                author_list = db_fetch[2]
                genre_list = db_fetch[3]
                location_list = db_fetch[4]
                issued_list = db_fetch[5]

                # Delete all rows in the tree.
                for k in self.tree.get_children():
                    self.tree.delete(k)

                # Iterate over each bookID in the database table and populate the table one row at a time.
                for i in range(len(bookID_list)):
                    # Issue Date
                    c.execute("SELECT date_issued FROM MyBooks WHERE user_id=(SELECT user_id WHERE bookID=?)", (bookID_list[i],))
                    date_issued_fetch = c.fetchall()
                    date_issued_list = [x[0] for x in date_issued_fetch]

                    # Return Date
                    c.execute("SELECT return_date FROM MyBooks WHERE user_id=(SELECT user_id WHERE bookID=?)", (bookID_list[i],))
                    return_date_fetch = c.fetchall()
                    return_date_list = [x[0] for x in return_date_fetch]

                    if len(date_issued_list) == 0 or len(return_date_list) == 0:
                        self.tree_ids.append(self.tree.insert("", "end", values=(bookID_list[i], title_list[i], author_list[i], genre_list[i], location_list[i], issued_list[i], 'N/A', 'N/A')))
                    else:
                        self.tree_ids.append(self.tree.insert("", "end", values=(bookID_list[i], title_list[i], author_list[i], genre_list[i], location_list[i], issued_list[i], date_issued_list[0], return_date_list[0])))
                self.tree.pack()

                for self.col in self.columns:
                    self.tree.heading(self.col, text=self.col,
                                          command=lambda c=self.col: self.sort_upon_press(c))

            else:
                ms.showerror('Error', 'Email was not found.', icon='error')
        else:
            ms.showerror('Error', 'Invalid DOI (Date of Issue)')

    def return_book(self):
        '''
        Called when the staff presses the button to return a book to the system from the ownership of a user.
        Sends the information to the database and updates the treeview table.

        Structuraly the same as the issue book.
        '''
        # Retrieve all entryboxes variables
        title_var = self.ret_title_var.get()
        author_var = self.ret_author_var.get()
        return_email = self.return_email_var.get()
        actual_return_date = self.ret_date_entry.get_date()

        book_id_search = c.execute('SELECT bookID FROM Books WHERE title=? AND author=? ', (title_var, author_var)).fetchall()
        book_id = [x[0] for x in book_id_search][0]

        if return_email == '':
            # Patron has no account.
            # Check if the book is connected to another email address.
            account_linked_book = c.execute("SELECT user_id FROM MyBooks WHERE bookID=?", (book_id,)).fetchall()
            if len(account_linked_book) != 0:
                ms.showerror('Error', 'Email address does not match the address linked to the book.')
            else:
                # Set the book issued status to 0 (meaning its now available).
                c.execute('UPDATE Books SET issued = 0 WHERE bookID=?', (book_id,))
                conn.commit()

                # Set entryfields to empty after return
                self.ret_bookID_var.set('')
                self.ret_title_var.set('')
                self.ret_author_var.set('')
                self.return_email_var.set('')

                # Run database fetch function
                db_fetch = self.database_fetch()

                # Extract return values from function.
                bookID_list = db_fetch[0]
                title_list = db_fetch[1]
                author_list = db_fetch[2]
                genre_list = db_fetch[3]
                location_list = db_fetch[4]
                issued_list = db_fetch[5]

                # Delete all rows in the table.
                for k in self.tree.get_children():
                    self.tree.delete(k)

                # Iterate over each bookID and populate the table row by row.
                for i in range(len(bookID_list)):
                    # Issue Date
                    c.execute("SELECT date_issued FROM MyBooks WHERE user_id=(SELECT user_id WHERE bookID=?)", (bookID_list[i],))
                    date_issued_fetch = c.fetchall()
                    date_issued_list = [x[0] for x in date_issued_fetch]

                    # Return Date
                    c.execute("SELECT return_date FROM MyBooks WHERE user_id=(SELECT user_id WHERE bookID=?)", (bookID_list[i],))
                    return_date_fetch = c.fetchall()
                    return_date_list = [x[0] for x in return_date_fetch]

                    if len(date_issued_list)==0 or len(return_date_list)==0:
                        self.tree_ids.append(self.tree.insert("", "end", values=(bookID_list[i], title_list[i], author_list[i], genre_list[i], location_list[i], issued_list[i], 'N/A', 'N/A')))
                    else:
                        self.tree_ids.append(self.tree.insert("", "end", values=(bookID_list[i], title_list[i], author_list[i], genre_list[i], location_list[i], issued_list[i], date_issued_list[0], return_date_list[0])))
                self.tree.pack()

                for self.col in self.columns:
                        self.tree.heading(self.col, text=self.col,
                                              command=lambda c=self.col: self.sort_upon_press(c))

                ms.showinfo('Success', 'Book returned successfully')
        else:
            try:
                # Check if email matches the owner of the loaned book.
                book_owner_email_fetch = c.execute('SELECT email_address FROM Accounts WHERE user_id=(SELECT user_id FROM MyBooks WHERE bookID=?)', (book_id,)).fetchall()
                book_owner_email = [x[0] for x in book_owner_email_fetch][0]

                if return_email != book_owner_email:
                    ms.showerror('Error', 'Email address does not match its rightful owner.')
                else:
                    # Send info to db
                    account_info_fetch = c.execute('SELECT * FROM Accounts WHERE email_address=?', (return_email,)).fetchall()
                    if len(account_info_fetch) != 0:
                        accounts_userid_check = [x[0] for x in account_info_fetch][0]

                        # Update the MyBooks table to set the actual return date. (the real date the patron returned the book, not the target date).
                        c.execute('UPDATE MyBooks SET actual_return_date=? WHERE bookID = ?', (actual_return_date, book_id,))
                        conn.commit()

                        # Check if the user has returned on time
                        accounts_return_date_fetch = c.execute('SELECT return_date FROM MyBooks WHERE bookID=?', (book_id,)).fetchall()
                        accounts_return_date_check = [x[0] for x in accounts_return_date_fetch][0]

                        accounts_return_date_check_time = datetime.strptime(accounts_return_date_check, '%Y-%m-%d').date()

                        if accounts_return_date_check_time < actual_return_date:
                            # Handed late
                            # Find the number of days the book is late by.
                            days_since_return_date = (accounts_return_date_check_time - actual_return_date)

                            # Format the output to be just an integer days to fetch just the integer
                            days_since_return_date_formatted = str(days_since_return_date).split("d")[0]

                            # Fetch the number in string and convert it into an absolute value integer.
                            days_since_return_date_formatted_integer = int(re.search(r'\d+', days_since_return_date_formatted).group())
                            result = ms.askyesno('Warning', 'This user has returned the book late by %s days\nDo you wish to Continue?' % days_since_return_date_formatted_integer)

                            if result is True:
                                # Delete the user where the bookID is equal to the returned book.
                                remove_user_id = 'DELETE FROM MyBooks WHERE bookID=?'
                                c.execute(remove_user_id, [(book_id)])
                                conn.commit()

                                # Set the book issued status to 0 (meaning its now available).
                                c.execute('UPDATE Books SET issued = 0 WHERE bookID=?', (book_id,))
                                conn.commit()

                                # Set entryfields to empty after return
                                self.ret_bookID_var.set('')
                                self.ret_title_var.set('')
                                self.ret_author_var.set('')
                                self.return_email_var.set('')

                                ms.showinfo('Success', 'Book returned successfully')

                            else:
                                ms.showerror('Cancelled', 'Book return cancelled')

                        elif accounts_return_date_check_time >= actual_return_date:
                            # Handed on time

                            # Fetch Location
                            book_location_fetch = c.execute("SELECT location FROM Books WHERE bookID=?", (book_id,)).fetchall()
                            book_location = [x[0] for x in book_location_fetch][0]

                            # Fetch genre
                            book_genre_fetch = c.execute("SELECT genre FROM Books WHERE bookID=?", (book_id,)).fetchall()
                            book_genre = [x[0] for x in book_genre_fetch][0]

                            # Fetch date issued
                            book_date_issued_fetch = c.execute("SELECT date_issued FROM MyBooks WHERE bookID=?", (book_id,)).fetchall()
                            date_issued = [x[0] for x in book_date_issued_fetch][0]

                            expected_return_date = accounts_return_date_check_time

                            e = Email()
                            service = e.get_service()
                            message = e.create_return_message("from@gmail.com", return_email, "Books4All Book Issued", title_var, author_var, book_genre, book_location, date_issued, expected_return_date, actual_return_date)
                            e.send_message(service, "from@gmail.com", message)

                            # Remove user_id from the ownership of the user and onto the public library.
                            remove_user_id = 'DELETE FROM MyBooks WHERE bookID=?'
                            c.execute(remove_user_id, [(book_id)])
                            conn.commit()

                            c.execute('UPDATE Books SET issued=0 WHERE bookID=?',(book_id,))
                            conn.commit()

                            ms.showinfo('Success', 'Book returned out successfully\nAn email has been sent to\n'+return_email+'\nregarding the return information.')

                        # Set entryfields to empty after return
                        self.ret_bookID_var.set('')
                        self.ret_title_var.set('')
                        self.ret_author_var.set('')
                        self.return_email_var.set('')

                        # Run database fetch function
                        db_fetch = self.database_fetch()

                        # Extract return values from function.
                        bookID_list = db_fetch[0]
                        title_list = db_fetch[1]
                        author_list = db_fetch[2]
                        genre_list = db_fetch[3]
                        location_list = db_fetch[4]
                        issued_list = db_fetch[5]

                        # Delete all rows in the table.
                        for k in self.tree.get_children():
                            self.tree.delete(k)

                        # Iterate over each bookID and populate the table row by row.
                        for i in range(len(bookID_list)):
                            # Issue Date
                            c.execute("SELECT date_issued FROM MyBooks WHERE user_id=(SELECT user_id WHERE bookID=?)",(bookID_list[i],))
                            date_issued_fetch = c.fetchall()
                            date_issued_list = [x[0] for x in date_issued_fetch]

                            # Return Date
                            c.execute("SELECT return_date FROM MyBooks WHERE user_id=(SELECT user_id WHERE bookID=?)",(bookID_list[i],))
                            return_date_fetch = c.fetchall()
                            return_date_list = [x[0] for x in return_date_fetch]

                            if len(date_issued_list)==0 or len(return_date_list)==0:
                                self.tree_ids.append(self.tree.insert("", "end", values=(bookID_list[i], title_list[i], author_list[i], genre_list[i], location_list[i], issued_list[i], 'N/A', 'N/A')))
                            else:
                                self.tree_ids.append(self.tree.insert("", "end", values=(bookID_list[i], title_list[i], author_list[i], genre_list[i], location_list[i], issued_list[i], date_issued_list[0], return_date_list[0])))
                        self.tree.pack()

                        for self.col in self.columns:
                                self.tree.heading(self.col, text=self.col,
                                                      command=lambda c=self.col: self.sort_upon_press(c))

                    else:
                        ms.showerror('Error', 'Email was not found.', icon='error')
            except IndexError:
                ms.showerror('Error', 'Email address does not match its rightful owner.')

    def bookID_validate(self, bookID_input):
        '''
        Validation to avoid invalid inputs in real-time.
        '''
        if bookID_input.isdigit():
            return True
        elif bookID_input == "":
            return True
        else:
            return False

    def ret_bookID_validate(self, ret_bookID_input):
        '''
        Validation to avoid invalid inputs in real-time.
        '''
        if ret_bookID_input.isdigit():
            return True
        elif ret_bookID_input == "":
            return True
        else:
            return False

    def remove_bookID_validate(self, remove_bookID_input):
        '''
        Validation to avoid invalid inputs in real-time.
        '''
        if remove_bookID_input.isdigit():
            return True
        elif remove_bookID_input == "":
            return True
        else:
            return False

    def _columns_searcher(self, *args):
        '''
        Passes in the values entered in the search fields below the table.
        Evaluates the state of the tree and what values are currently displayed.
        Passes this information onto the tree searching function(s).
        '''

        # Gets the empty self._detached list that will store all the rows of the table that are not to be shown, based on the search fields that the user entered.
        # Adds the self._detached empty list to a list of currently displayed rows in the table, 
        # thereby creating one list called children, which stores both the hidden and visible rows of the table.
        children = list(self._detached) + list(self.tree.get_children())

        # self._detached is made into a set, which is a data structure that stores values in an unordered fashion.
        self._detached = set()

        # Get all search entry fields and convert them into strings for easier manipulation later on.
        query_bookID = str(self.db_search_bookID_var.get())
        query_title = str(self.db_search_title_var.get())
        query_author = str(self.db_search_author_var.get())
        query_genre = str(self.db_search_genre_var.get())
        query_location = str(self.db_search_location_var.get())

        # Call the function that will re-order the tree according to the search parameters entered by the user.
        self.search_tv(children, query_bookID, query_title, query_author, query_genre, query_location)

    def search_tv(self, children, query_bookID, query_title, query_author, query_genre, query_location):
        '''
        Returns a tree that is ordered according to the search parameters entered by the user.
        '''

        # Iterable variable that will iterate from row 0 on the tree.
        i_r = -1

        # Iterate over each item_id (which is the row id) in the whole tree, both the hidden and currently displayed rows.
        for item_id in children:
            # Get the string values of each column value of the current row.
            bookID_text = str(self.tree.item(item_id)['values'][0])
            title_text = str(self.tree.item(item_id)['values'][1])
            author_text = str(self.tree.item(item_id)['values'][2])
            genre_text = str(self.tree.item(item_id)['values'][3])
            location_text = str(self.tree.item(item_id)['values'][4])

            # If the current search parameter is empty, the tree will display all the rows on the table.
            # E.g. If all the search fields are empty, meaning nothing has been searched for, then the table will display all the values as a default.
            if query_bookID != '':
                if query_bookID in bookID_text:
                    # If any of the characters in the user search query are in the column string value (in this case the bookID_text string value);
                    # The iterable will increase to find the next row (if this is the start of the search, then the iterable will increment to 0, which is the top row of the table.)
                    i_r += 1
                    # The tree will reattach the correct row (item_id) onto the top of the table, as well as any other searches which contain the same characters so far.
                    # E.g. searching bookID=1 in a database with bookIDs= 1, 11, 133. This will prompt the table to show all those rows on the table, because they all begin with the 1
                    # that the user searched for.
                    # This process repeats for the rest of the function.
                    self.tree.reattach(item_id, '', i_r)
                else:
                    self._detached.add(item_id)
                    self.tree.detach(item_id)

            elif query_title != '':
                if query_title in title_text:
                    i_r += 1
                    self.tree.reattach(item_id, '', i_r)
                else:
                    self._detached.add(item_id)
                    self.tree.detach(item_id)

            elif query_author != '':
                if query_author in author_text:
                    i_r += 1
                    self.tree.reattach(item_id, '', i_r)
                else:
                    self._detached.add(item_id)
                    self.tree.detach(item_id)

            elif query_genre != '-EMPTY-':
                if query_genre in genre_text:
                    i_r += 1
                    self.tree.reattach(item_id, '', i_r)
                else:
                    self._detached.add(item_id)
                    self.tree.detach(item_id)

            elif query_location != '-EMPTY-':
                if query_location in location_text:
                    i_r += 1
                    self.tree.reattach(item_id, '', i_r)
                else:
                    self._detached.add(item_id)
                    self.tree.detach(item_id)
            else:
                # If all the fields are empty or in their default state, display the default table.
                self.tree.reattach(item_id, '', i_r)

    def _columns_searcher_issued(self, *args):
        '''
        Passes in the values entered in the search fields below the table.
        Evaluates the state of the tree and what values are currently displayed.
        Passes this information onto the tree searching function(s).

        Seperate from the rest of the query searches, because the trace() feature
        does not allow more than one variable to be traced onto the same function callback.

        Structuraly the same as the above function of _columns_searcher
        '''
        children = list(self._detached) + list(self.tree.get_children())
        self._detached = set()
        query_issued = self.db_search_issued_var.get()

        self.search_issued_tv(children, query_issued)

    def search_issued_tv(self, children, query_issued):
        '''
        Returns a tree that is ordered according to the search parameters entered by the user.

        Seperate from the rest of the query searches, because the trace() feature
        does not allow more than one variable to be traced onto the same function callback.

        Structuraly the same as the above function of search_tv
        '''
        i_r = -1

        for item_id in children:
            issued_text = self.tree.item(item_id)['values'][5]

            if query_issued in str(issued_text):
                i_r += 1
                self.tree.reattach(item_id, '', i_r)

            elif query_issued == '-EMPTY-':
                self.tree.reattach(item_id, '', i_r)

            else:
                self._detached.add(item_id)
                self.tree.detach(item_id)

    def sort_upon_press(self, c):
        '''
        Passes in a column value c
        Passes an array for the quicksort algorithm to sort into the correct alphanumerical order.
        '''

        # Try statement here, because the column heading that is pressed may require that the
        # sort is done based on integers, therefore the array values would need to be converted into integers.
        # whereas if the column that is attempted to be sorted is alphabetical, all the values of the array must
        # be converted into strings when read from the tree.
        try:
            # Iterates over each row of the tree (tuple data structure) and places it into an array that the quicksort can use.
            self.arr = [(int(self.tree.set(k, c)), k) for k in self.tree.get_children('')]
        except ValueError:
            # In case the column requires a string sort, the same happens here as above.
            self.arr = [(self.tree.set(k, c), k) for k in self.tree.get_children('')]

        # Store the length of the array.
        self.n = len(self.arr)
        # Call the quicksort function and pass in:
        #        - The tree object to allow the sort algorithm to re-order the tree upon each partition.
        #        - The column value that the tree is currently being sorted by.
        #        - The array that was established above for the sorting algorithm to sort.
        #        - The low variable for the sort algorithm is set to 0.
        #        - The length of the array -1 set as the high
        #        - Reverse is set to False, as this is the assumed First press of the heading, on the second press, this would be True.

        self.quickSort(self.tree, c, self.arr, 0, self.n-1, False)

    def partition(self, arr,low, high):
        '''
        Create the partition for the sort algorithm
        The partition will be sorted until its completed that section and returns the left bound pointer i, upon it reaching a value >= the pivot
        '''

        # Lower bound pointer i
        i = (low-1)
        # Pivot is chosen as the value of the length of the array -1
        pivot = arr[high]

        # Iterate j over the elements between the beginning of the array (low) and the pivot (high).
        for j in range(low, high):
            # If the current iteration of j is an element that is less than or equal to the pivot.
            if arr[j] <= pivot:
                # Increment the lower bound pointer i
                i = i+1
                # Swap the lower bound pointer i's element for the element at position j in the array.
                # and element at position j swaps with element at position i.
                arr[i], arr[j] = arr[j], arr[i]

        # swap the element above the current position of the left bound pointer i, to the position of the pivot.
        # swap the element at the pivot to the position above the current position of the left bound pointer i.
        arr[i+1], arr[high] = arr[high], arr[i+1]

        # return the left bound pointer i value upon completion of the first partition.
        return (i+1)

    def quickSort(self, tv, col, arr, low, high, reverse):
        '''
        Quicksort is called to keep the partitions going until the tree is considered sorted, where no partitions can be made.
        Returns a sorted tree.
        '''
        # Need to update arr if a new value is added to the treeview
        if len(arr) == 1:
            # If the array has only one element, it is already inherently sorted.
            return arr
        if low < high:
            #  pt is partitioning index
            pt = self.partition(arr, low, high)

            #  Separately sort elements before
            #  partition and after partition
            self.quickSort(tv, col, arr, low, pt-1, reverse=reverse)
            self.quickSort(tv, col, arr, pt+1, high, reverse=reverse)

        # Iterate over the tuple values in the array and move each row to the correct index position determined by the array that has been sorted.
        for index, (val, k) in enumerate(arr):
            # Moves the correct row id to the correct index.
            tv.move(k, '', index)

        # For each time that the column heading is pressed, the opposite of the reverse variable will occur.
        # Meaning if the reverse variable is currently False, because it has already been ran as a False and sorted the tree in ascending order,
        # then the next press will invert the array to be sorted in descending order.
        tv.heading(col, command=lambda: \
            self.quickSort(tv, col, arr, low, high, not reverse))

        if reverse is True:
            # To save time and avoid having to sort the list again when it has already been sorted,
            # when the reverse sort is triggered, the array simply inverts itself, rather than go
            # through the whole partitioning sort process again.
            arr_reverse = arr[::-1]
            # The tree is re-ordered as this function is described above.
            for index, (val, k) in enumerate(arr_reverse):
                tv.move(k, '', index)

    def database_fetch(self):
        '''
        Commonly used database fetch
        Returns the lists of bookIDs, titles, authors, genres, locations and issued books.
        '''
        # Book IDs
        c.execute("SELECT bookID FROM Books")
        bookIDs_fetch = c.fetchall()
        bookID_list = [x[0] for x in bookIDs_fetch]

        # Titles
        c.execute("SELECT title FROM Books")
        title_fetch = c.fetchall()
        title_list = [x[0] for x in title_fetch]

        # Authors
        c.execute("SELECT author FROM Books")
        author_fetch = c.fetchall()
        author_list = [x[0] for x in author_fetch]

        # Genres
        c.execute("SELECT genre FROM Books")
        genre_fetch = c.fetchall()
        genre_list = [x[0] for x in genre_fetch]

        # location
        c.execute("SELECT location FROM Books")
        location_fetch = c.fetchall()
        location_list = [x[0] for x in location_fetch]

        # Issued/Not Issued
        c.execute("SELECT issued FROM Books")
        issued_fetch = c.fetchall()
        issued_list = [x[0] for x in issued_fetch]

        return (bookID_list, title_list, author_list, genre_list, location_list, issued_list)


class AutoCompleteEntryBD_ReturnBookID(ttk.Entry):
    '''
    Autocomplete function to display all the possible values that could go into the field, based on what is currently being typed into the entry field.
    '''
    def __init__(self, ret_search_container_autocomplete, ret_title_entry, ret_title_var, ret_author_entry, ret_author_var, ret_bookID_var, ret_bookID_entry, ret_date_entry, ret_search_container_canvas, *args, **kwargs):
        '''
        Fetch all the necessary values and setup the variables required for the upcoming functions.
        '''

        # Add self to variables to make them class instance variables and be accessed across the class.
        self.ret_search_container_autocomplete = ret_search_container_autocomplete
        self.ret_bookID_entry = ret_bookID_entry
        self.ret_title_entry = ret_title_entry
        self.ret_author_entry = ret_author_entry
        self.ret_date_entry = ret_date_entry
        self.ret_search_container_canvas = ret_search_container_canvas

        #  Listbox length
        if 'listboxLength' in kwargs:
            self.listboxLength = kwargs['listboxLength']
            del kwargs['listboxLength']
        else:
            self.listboxLength = 8

        # Initiate the entry box for the autocomplete search field.
        ttk.Entry.__init__(self, *args, **kwargs)
        # Focus the user keyboard on the this field.
        self.focus()

        # Fetch database books that have been issued (issued=1)
        # Titles
        c.execute("SELECT bookID FROM Books WHERE issued=1")
        issued_bookIDs_fetch = c.fetchall()
        issued_bookIDs_list = [x[0] for x in issued_bookIDs_fetch]

        # Establish more class instance variables.
        self.listb = issued_bookIDs_list

        self.ret_bookID_var = ret_bookID_var
        self.ret_title_var = ret_title_var
        self.ret_author_var = ret_author_var

        self.ret_bookID_entry = self["textvariable"]
        if self.ret_bookID_entry == '':
            self.ret_bookID_entry = self["textvariable"] = tk.StringVar()

        # Trace the user input in the entry field.
        # Calls self.changed function upon any user changes in the field.
        self.ret_bookID_var.trace('w', self.changed)

        # Bind the user's arrow keys to different functions in the autocomplete box.
        # <Right> arrow key allows for the user to select the currently highlighted autocomplete value.
        self.bind("<Right>", self.selection)
        # <Up> and <Down> arrow keys allow the user to navigate the autocomplete box.
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)

        # lb_up determines whether the autocomplete frame should be currently showing or not.
        # Set to False by default, to avoid having the box showing the entire time, despite any user input or not.
        self.lb_up = False

    def changed(self, name, index, mode):
        '''
        Passes in the name, index and mode of the search.
        Name: Holds the event trigger that is automatically passed by tkinter when the .trace() function is called
        Index: Holds the index position of the user when searching through the autocomplete box using the arrow keys.
        Mode: Holds the mode which is currently being used to search through the box.
        '''
        # Fetch database books that have been issued (issued=1)
        # Titles
        c.execute("SELECT bookID FROM Books WHERE issued=1")
        issued_bookIDs_fetch = c.fetchall()
        issued_bookIDs = [x[0] for x in issued_bookIDs_fetch]

        self.listb = issued_bookIDs

        # Check if the autocomplete container is currently on the screen.
        if self.ret_search_container_autocomplete.winfo_ismapped() == False:
            # If the autocomplete container is not on the screen, display it on there.
            self.ret_search_container_autocomplete.pack(anchor=tk.W, fill=tk.X, side=tk.TOP)

        if self.ret_bookID_var.get() == '':
            # If the user input is empty, destroy the autocomplete box.
            if self.lb_up:
                self.lb.destroy()
                self.lb_up = False
        else:
            # If the user input is not empty, populate the autocomplete container with the correct values that match the input.
            # Call the comparison function that checks if any of the bookIDs in the database match any of the characters entered by the user.
            # Returns a list each character entered by the user. Example: input=(Yes), then words=['Y','e','s']
            words = self.comparison()
            if words:
                # Since there are no operators to evaluate the variable 'words',
                # the if statement evaluates it as a boolean, therefore if there is any kind of data in words, it will be considered a truthy statement
                # and return True, if there is no data in the variable at all, it is considered a False.
                if not self.lb_up:
                    # If the opposite of the autocomplete container status is True, then the container is currently not showing, therefore it must be shown, hence the widget is packed below.
                    self.lb = tk.Listbox(self.ret_search_container_canvas, width=self["width"], height=self.listboxLength)

                    # Bind double clicking the mouse button 1 as a selection event.
                    self.lb.bind("<Double-Button-1>", self.selection)

                    # Also allow the user to use the <Right> arrow key to select the currently highlighted autocomplete value.
                    self.lb.bind("<Right>", self.selection)
                    self.lb.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

                    # The autocomplete container is now showing, therefore lb_up is True.
                    self.lb_up = True

                # Delete any values that may have lingered on from the previous call of this function.
                # Clears any possible values from the box to have an empty box to then populate.
                self.lb.delete(0, tk.END)

                # For each character in the user input list that we created earlier, insert the character back into the options in the autocomplete box.
                for w in words:
                    self.lb.insert(tk.END, w)
            else:
                # If the list of words is empty, then destroy the autocomplete box.
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False

                    # Hide the box from view, not destroy.
                    self.ret_search_container_autocomplete.pack_forget()
                    self.ret_search_container_canvas["height"] = 0
                    self.ret_search_container_canvas["width"] = 0

    def selection(self, event):
        '''
        Upon triggering this function, the selected autocomplete option will be copied over to the entry field.
        '''
        if self.lb_up:
            # If the autocomplete container is currently showing, then set the entry field where the user was entering their search, to be the value that they selected.
            self.ret_bookID_var.set(self.lb.get(tk.ACTIVE))

            # Fetch the book's title, author and return date based on the bookID that was selected above.
            book_title_fetch = c.execute('SELECT title FROM Books WHERE bookID=?', (self.ret_bookID_var.get(),)).fetchall()
            book_title = [x[0] for x in book_title_fetch][0]

            book_author_fetch = c.execute('SELECT author FROM Books WHERE bookID=?', (self.ret_bookID_var.get(),)).fetchall()
            book_author = [x[0] for x in book_author_fetch][0]

            try:
                # Fetch return date from table
                return_date_fetch = c.execute('SELECT return_date FROM MyBooks WHERE bookID=?', (self.ret_bookID_var.get(),)).fetchall()
                return_date = [x[0] for x in return_date_fetch][0]
            except IndexError:
                return_date = str(datetime.today().strftime('%Y-%m-%d'))

            # Set the entry fields to be the fetched values.
            self.ret_title_var.set(book_title)
            self.ret_author_var.set(book_author)
            self.ret_date_entry.set_date(datetime.strptime(return_date, '%Y-%m-%d'))

            # Hide the autocomplete box upon setting the other entry field values.
            self.ret_search_container_autocomplete.pack_forget()
            self.ret_search_container_canvas["height"] = 0
            self.ret_search_container_canvas["width"] = 0

            # Destroy the container of the autocomplete box.
            self.lb.destroy()

            # The container is no longer showing, therefore lb_up should be False.
            self.lb_up = False

            # Set the cursor (flashing line when you type) to be at the end of the string in the entry field.
            self.icursor(tk.END)

    def up(self, event):
        '''
        Allow the user to move up the autocomplete box using the <Up> arrow key.
        '''

        if self.lb_up:
            # only allow the user to move this way, if the autocomplete box is currently on the screen.
            if self.lb.curselection() == ():
                # lb.curselection() returns a tuple with the number of elements in the listbox that is the autocomplete box.
                # If this tuple is empty, then set the index to 0 (the first element in the listbox will be highlighted)
                index = '0'
            else:
                # If it is not empty, then the index will be equal to the position of the currently selected element in the listbox.
                index = self.lb.curselection()[0]

            if index != '0':
                # If the index is not 0, then the element in the index position will be cleared
                self.lb.selection_clear(first=index)
                # The index will decrement by one
                index = str(int(index)-1)

                # Allow the element in the listbox at the index position to be in view.
                self.lb.see(index)
                self.lb.selection_set(first=index)

                # Select the element specified by the index.
                self.lb.activate(index)

    def down(self, event):
        '''
        The same as the up function, but downward.
        '''
        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != tk.END:
                self.lb.selection_clear(first=index)
                index = str(int(index)+1)

                self.lb.see(index)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def comparison(self):
        '''
        Convert the user input into a segmented list, where each character from the input is a seperate element.
        Compares the database issued book values to the user input, and checks if any of the characters match any characters in the other and vice versa.
        Returns a list of elements that make up the user input.
        '''
        pattern = re.compile('.*' + self.ret_bookID_var.get() + '.*')
        return [w for w in self.listb if re.match(pattern, str(w))]


class AutoCompleteEntryBD_IssueBookID(ttk.Entry):
    '''
    Autocomplete function to display all the possible values that could go into the field, based on what is currently being typed into the entry field.

    Structuraly the same as all the other Autocomplete classes, however this applies to the issuing of books.
    Already described above.
    '''
    def __init__(self, search_container_autocomplete, title_entry, title_var, author_entry, author_var, bookID_var, bookID_entry, search_container_canvas, *args, **kwargs):

        self.search_container_autocomplete = search_container_autocomplete
        self.search_container_canvas = search_container_canvas

        self.title_entry = title_entry
        self.author_entry = author_entry

        #  Listbox length
        if 'listboxLength' in kwargs:
            self.listboxLength = kwargs['listboxLength']
            del kwargs['listboxLength']
        else:
            self.listboxLength = 8

        ttk.Entry.__init__(self, *args, **kwargs)
        self.focus()

        # Titles
        c.execute("SELECT bookID FROM Books WHERE issued=0")
        books_bookIDs_fetch = c.fetchall()
        book_bookIDs_list = [x[0] for x in books_bookIDs_fetch]

        self.lista = book_bookIDs_list

        self.bookID_var = bookID_var
        self.title_var = title_var
        self.author_var = author_var

        self.bookID_entry = self["textvariable"]
        if self.bookID_entry == '':
            self.bookID_entry = self["textvariable"] = tk.StringVar()

        self.bookID_var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)

        self.lb_up = False

    def changed(self, name, index, mode):
        # Titles
        c.execute("SELECT bookID FROM Books WHERE issued=0")
        books_bookID_fetch = c.fetchall()
        book_bookID_list = [x[0] for x in books_bookID_fetch]

        self.lista = book_bookID_list

        if self.search_container_autocomplete.winfo_ismapped() is False:
            self.search_container_autocomplete.pack(anchor=tk.W, fill=tk.X, side=tk.TOP)

        if self.bookID_var.get() == '':
            if self.lb_up:
                self.lb.destroy()
                self.lb_up = False

        else:
            words = self.comparison()
            if words:
                if not self.lb_up:
                    self.lb = tk.Listbox(self.search_container_canvas, width=self["width"], height=self.listboxLength)
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)
                    self.lb_up = True

                self.lb.delete(0, tk.END)

                for w in words:
                    self.lb.insert(tk.END,w)

            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False

                    self.search_container_autocomplete.pack_forget()
                    self.search_container_canvas["height"]=0
                    self.search_container_canvas["width"]=0

    def selection(self, event):
        if self.lb_up:
            self.bookID_var.set(self.lb.get(tk.ACTIVE))

            book_title_fetch = c.execute('SELECT title FROM Books WHERE bookID=?', (self.bookID_var.get(),)).fetchall()
            book_title = [x[0] for x in book_title_fetch][0]

            book_author_fetch = c.execute('SELECT author FROM Books WHERE bookID=?', (self.bookID_var.get(),)).fetchall()
            book_author = [x[0] for x in book_author_fetch][0]

            self.title_var.set(book_title)
            self.author_var.set(book_author)

            self.search_container_autocomplete.pack_forget()
            self.search_container_canvas["height"] = 0
            self.search_container_canvas["width"] = 0

            self.lb.destroy()
            self.lb_up = False
            self.icursor(tk.END)

    def up(self, event):
        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]

            if index != '0':
                self.lb.selection_clear(first=index)
                index = str(int(index)-1)

                self.lb.see(index)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def down(self, event):
        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != tk.END:
                self.lb.selection_clear(first=index)
                index = str(int(index)+1)

                self.lb.see(index)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def comparison(self):
        pattern = re.compile('.*' + self.bookID_var.get() + '.*')
        return [w for w in self.lista if re.match(pattern, str(w))]


class AutoCompleteEntryBD_RemoveBookID(ttk.Entry):
    '''
    Autocomplete function to display all the possible values that could go into the field, based on what is currently being typed into the entry field.

    Structuraly the same as all the other Autocomplete classes, however this applies to the removal of books.
    Already described above.
    '''
    def __init__(self, remove_container_autocomplete, remove_title_entry, remove_title_var, remove_author_entry, remove_author_var, remove_bookID_var, remove_bookID_entry, remove_genre_var, remove_genre_menu, remove_container_canvas, *args, **kwargs):

        self.remove_container_autocomplete = remove_container_autocomplete
        self.remove_container_canvas = remove_container_canvas
        self.remove_title_entry = remove_title_entry
        self.remove_author_entry = remove_author_entry
        self.remove_genre_menu = remove_genre_menu

        #  Listbox length
        if 'listboxLength' in kwargs:
            self.listboxLength = kwargs['listboxLength']
            del kwargs['listboxLength']
        else:
            self.listboxLength = 8

        ttk.Entry.__init__(self, *args, **kwargs)
        self.focus()

        # Titles
        c.execute("SELECT bookID FROM Books")
        remove_books_bookIDs_fetch = c.fetchall()
        remove_book_bookID_list = [x[0] for x in remove_books_bookIDs_fetch]

        self.lista = remove_book_bookID_list

        self.remove_bookID_var = remove_bookID_var
        self.remove_title_var = remove_title_var
        self.remove_author_var = remove_author_var
        self.remove_genre_var = remove_genre_var

        self.remove_bookID_entry = self["textvariable"]
        if self.remove_bookID_entry == '':
            self.remove_bookID_entry = self["textvariable"] = tk.StringVar()

        self.remove_bookID_var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)

        self.lb_up = False

    def changed(self, name, index, mode):
        # Titles
        c.execute("SELECT bookID FROM Books")
        books_bookID_fetch = c.fetchall()
        remove_book_bookID_list = [x[0] for x in books_bookID_fetch]

        self.lista = remove_book_bookID_list

        if self.remove_container_autocomplete.winfo_ismapped() is False:
            self.remove_container_autocomplete.pack(anchor=tk.W, fill=tk.X, side=tk.TOP)

        if self.remove_bookID_var.get() == '':
            if self.lb_up:
                self.lb.destroy()
                self.lb_up = False
        else:
            words = self.comparison()
            if words:
                if not self.lb_up:
                    self.lb = tk.Listbox(self.remove_container_canvas, width=self["width"], height=self.listboxLength)
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)
                    self.lb_up = True

                self.lb.delete(0, tk.END)
                for w in words:
                    self.lb.insert(tk.END, w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False

                    self.remove_container_autocomplete.pack_forget()
                    self.remove_container_canvas["height"] = 0
                    self.remove_container_canvas["width"] = 0

    def selection(self, event):
        if self.lb_up:
            self.remove_bookID_var.set(self.lb.get(tk.ACTIVE))

            remove_book_title_fetch = c.execute('SELECT title FROM Books WHERE bookID=?', (self.remove_bookID_var.get(),)).fetchall()
            remove_book_title = [x[0] for x in remove_book_title_fetch][0]

            remove_book_author_fetch = c.execute('SELECT author FROM Books WHERE bookID=?', (self.remove_bookID_var.get(),)).fetchall()
            remove_book_author = [x[0] for x in remove_book_author_fetch][0]

            remove_book_genre_fetch = c.execute('SELECT genre FROM Books WHERE bookID=?', (self.remove_bookID_var.get(),)).fetchall()
            remove_book_genre = [x[0] for x in remove_book_genre_fetch][0]

            self.remove_title_var.set(remove_book_title)
            self.remove_author_var.set(remove_book_author)
            self.remove_genre_var.set(remove_book_genre)

            self.remove_container_autocomplete.pack_forget()
            self.remove_container_canvas["height"] = 0
            self.remove_container_canvas["width"] = 0

            self.lb.destroy()
            self.lb_up = False
            self.icursor(tk.END)

    def up(self, event):
        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]

            if index != '0':
                self.lb.selection_clear(first=index)
                index = str(int(index)-1)

                self.lb.see(index)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def down(self, event):
        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != tk.END:
                self.lb.selection_clear(first=index)
                index = str(int(index)+1)

                self.lb.see(index)
                self.lb.selection_set(first=index)
                self.lb.activate(index) 

    def comparison(self):
        pattern = re.compile('.*' + self.remove_bookID_var.get() + '.*')
        return [w for w in self.lista if re.match(pattern, str(w))]

