#BookDatabase page

import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox as ms
import bcrypt
import sys
import string
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import re

from email_sys import Email
conn = sqlite3.connect('LibrarySystem.db')
c = conn.cursor()

width=225
padx=8
pady=5

geometry = '1500x1500'
bg='gray90'
font='System 18'

#List of genres
c.execute("SELECT genre FROM Genres")
genres_list_fetch = c.fetchall()
genre_choice_list = [x[0] for x in genres_list_fetch]

#Fetch database values
#Titles that have not been issued (issued=0) 
c.execute("SELECT title FROM Books WHERE issued=0")
books_title_fetch = c.fetchall()
book_title_list = [x[0] for x in books_title_fetch]

#Fetch database books that have been issued (issued=1)
#Titles
c.execute("SELECT title FROM Books WHERE issued=1")
issued_titles_fetch = c.fetchall()
issued_titles = [x[0] for x in issued_titles_fetch]

#List of locations
location_choice_list = list(string.ascii_uppercase)
location_alphabet_symbol = location_choice_list.append('*')
location_empty_insert = location_choice_list.insert(0, '-EMPTY-')

#List of issued
issued_choice_list = ['-EMPTY-', '0', '1']



class BookDatabase():
    #STAFF ONLY ACCESS
    #Update book database when books are taken in/out.
    def __init__(self, root, notebook, current_user_email):
        self.tree_ids = [] 
        self.lista = []
        self.root = root
        self.notebook = notebook
        user_email = current_user_email

        book_database_page = tk.Frame(self.notebook)
        notebook.add(book_database_page, text='Book Database')

        header_frame = tk.Frame(book_database_page)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        header = tk.Label(header_frame, text='Book Database', font='System 30')
        header.pack(side=tk.TOP)

        # Library TreeView Book Database Frame
        tree_container = tk.Frame(book_database_page, bg=bg)
        tree_container.pack(side=tk.BOTTOM, anchor=tk.N, padx=padx, pady=pady)

        tree_header = tk.Label(tree_container, text='Database', font='System 18', bg=bg)
        tree_header.pack(padx=padx, pady=pady)

        #Set up TreeView table
        self.columns = ('Book ID','Title', 'Author', 'Genre','Location', 'Issued', 'Issue Date', 'Return Date')
        self.tree = ttk.Treeview(tree_container, columns=self.columns, show='headings') #create tree
        self.tree.heading("Book ID", text='Book ID')
        self.tree.heading("Title", text='Title')
        self.tree.heading("Author", text='Author')
        self.tree.heading("Genre", text='Genre')
        self.tree.heading("Location", text='Location')
        self.tree.heading("Issued", text='Issued')
        self.tree.heading("Issue Date", text='Issued Date')
        self.tree.heading("Return Date", text='Return Date')

        self.tree.column("Book ID", width=width, anchor=tk.CENTER)
        self.tree.column("Title", width=width, anchor=tk.CENTER)
        self.tree.column("Author", width=width, anchor=tk.CENTER)
        self.tree.column("Genre", width=width, anchor=tk.CENTER)
        self.tree.column("Location", width=width, anchor=tk.CENTER)
        self.tree.column("Issued", width=width, anchor=tk.CENTER)
        self.tree.column("Issue Date", width=width, anchor=tk.CENTER)
        self.tree.column("Return Date", width=width, anchor=tk.CENTER)

        #Book IDs
        c.execute("SELECT bookID FROM Books")
        bookIDs_fetch = c.fetchall()
        bookID_list = [x[0] for x in bookIDs_fetch]

        #Titles
        c.execute("SELECT title FROM Books")
        title_fetch = c.fetchall()
        title_list = [x[0] for x in title_fetch]

        #Authors
        c.execute("SELECT author FROM Books")
        author_fetch = c.fetchall()
        author_list = [x[0] for x in author_fetch]

        #Genres
        c.execute("SELECT genre FROM Books")
        genre_fetch = c.fetchall()
        genre_list = [x[0] for x in genre_fetch]

        #location
        c.execute("SELECT location FROM Books")
        location_fetch = c.fetchall()
        location_list = [x[0] for x in location_fetch]

        #Issued/Not Issued
        c.execute("SELECT issued FROM Books")
        issued_fetch = c.fetchall()
        issued_list = [x[0] for x in issued_fetch]

        for k in self.tree.get_children():
            self.tree.delete(k)

        for i in range(len(bookID_list)):
            #Issue Date
            c.execute("SELECT date_issued FROM MyBooks WHERE user_id=(SELECT user_id WHERE bookID=?)",(bookID_list[i],))
            date_issued_fetch = c.fetchall()
            date_issued_list = [x[0] for x in date_issued_fetch]

            #Return Date
            c.execute("SELECT return_date FROM MyBooks WHERE user_id=(SELECT user_id WHERE bookID=?)",(bookID_list[i],))
            return_date_fetch = c.fetchall()
            return_date_list = [x[0] for x in return_date_fetch]
            #creates an entry in the tree for each element of the list
            #then stores the id of the tree in the self.ids list
            if len(date_issued_list)==0 or len(return_date_list)==0:
                self.tree_ids.append(self.tree.insert("", "end", values=(bookID_list[i], title_list[i], author_list[i], genre_list[i], location_list[i], issued_list[i], 'N/A', 'N/A')))
            else:
                self.tree_ids.append(self.tree.insert("", "end", values=(bookID_list[i], title_list[i], author_list[i], genre_list[i], location_list[i], issued_list[i], date_issued_list[0], return_date_list[0])))
        self.tree.pack()


        #Search the Treeview Container
        self.db_search_container = tk.Frame(tree_container)
        self.db_search_container.pack(side=tk.BOTTOM, anchor=tk.N, padx=padx, pady=pady)


        #BookID Search DB
        db_search_label_bookID = tk.Label(self.db_search_container, text='ID: ', bg=bg)
        db_search_label_bookID.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self._detached = set()
        self.db_search_bookID_var = tk.StringVar()
        self.db_search_bookID_var.trace("w", self._columns_searcher_bookID_BD)

        self.db_search_bookID_entry = ttk.Entry(self.db_search_container, textvariable=self.db_search_bookID_var)
        self.db_search_bookID_entry.pack(side=tk.LEFT, anchor=tk.E, padx=padx, pady=pady)


        #Title Search DB
        db_search_label_title = tk.Label(self.db_search_container, text='Title: ', bg=bg)
        db_search_label_title.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self._detached = set()
        self.db_search_title_var = tk.StringVar()
        self.db_search_title_var.trace("w", self._columns_searcher_title_BD)

        self.db_search_title_entry = ttk.Entry(self.db_search_container, textvariable=self.db_search_title_var)
        self.db_search_title_entry.pack(side=tk.LEFT, anchor=tk.E, padx=padx, pady=pady)


        #Author Search DB
        db_search_label_author = tk.Label(self.db_search_container, text='Author: ', bg=bg)
        db_search_label_author.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self._detached = set()
        self.db_search_author_var = tk.StringVar()
        self.db_search_author_var.trace("w", self._columns_searcher_author_BD)

        self.db_search_author_entry = ttk.Entry(self.db_search_container, textvariable=self.db_search_author_var)
        self.db_search_author_entry.pack(side=tk.LEFT, anchor=tk.E, padx=padx, pady=pady)


        #Genre Search DB
        db_search_label_genre = tk.Label(self.db_search_container, text='Genre: ', bg=bg)
        db_search_label_genre.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self._detached = set()
        self.db_search_genre_var = tk.StringVar()
        self.db_search_genre_var.set("-EMPTY-")
        self.db_search_genre_var.trace("w", self._columns_searcher_genre_BD)


        self.db_search_genre_menu = ttk.OptionMenu(self.db_search_container, self.db_search_genre_var, genre_choice_list[0], *genre_choice_list)
        self.db_search_genre_menu.pack(side=tk.LEFT, anchor=tk.E, padx=padx, pady=pady)



        #Location Search DB
        db_search_label_location = tk.Label(self.db_search_container, text='Location: ', bg=bg)
        db_search_label_location.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self._detached = set()
        self.db_search_location_var = tk.StringVar()
        self.db_search_location_var.set("-EMPTY-")
        self.db_search_location_var.trace("w", self._columns_searcher_location_BD)


        self.db_search_location_menu = ttk.OptionMenu(self.db_search_container, self.db_search_location_var, location_choice_list[0], *location_choice_list)
        self.db_search_location_menu.pack(side=tk.LEFT, anchor=tk.E, padx=padx, pady=pady)


        #Issued Search DB
        db_search_label_issued = tk.Label(self.db_search_container, text='Issued(1/0): ', bg=bg)
        db_search_label_issued.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self._detached = set()
        self.db_search_issued_var = tk.StringVar()
        self.db_search_issued_var.set("-EMPTY-")
        self.db_search_issued_var.trace("w", self._columns_searcher_issued_BD)

        self.db_search_issued_menu = ttk.OptionMenu(self.db_search_container, self.db_search_issued_var, issued_choice_list[0], *issued_choice_list)
        self.db_search_issued_menu.pack(side=tk.LEFT, anchor=tk.E, padx=padx, pady=pady)


        for self.col in self.columns:
                self.tree.heading(self.col, text=self.col,
                                      command=lambda c=self.col: self.sort_upon_press(c))


        #Issue/Return Books UI
        filter_container = tk.Frame(book_database_page, bg=bg)
        filter_container.pack(side=tk.LEFT, anchor=tk.N, padx=padx, pady=pady)

        filter_header = tk.Label(filter_container, text='Issue Book', font='System 18', bg=bg)
        filter_header.pack(anchor=tk.W, padx=padx, pady=pady)

        #BookID Entry Field
        self.search_container_bookID = tk.Frame(filter_container, bg=bg)
        self.search_container_bookID.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        bookID_label = tk.Label(self.search_container_bookID, text='ID: ', bg=bg)
        bookID_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.bookID_reg = root.register(self.bookID_validate)
        self.bookID_var = tk.StringVar()

        self.bookID_entry = ttk.Entry(self.search_container_bookID)
        self.bookID_entry.config(textvariable=self.bookID_var, validate="key",
                            validatecommand=(self.bookID_reg, "%P"))
        self.bookID_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        # Filler frame for the autocomplete function
        self.search_container_canvas = tk.Canvas(filter_container, height=50, width=50, bg=bg)
        self.search_container_canvas.pack(fill=tk.X, expand=True)

        self.search_container_autocomplete = tk.Frame(self.search_container_canvas, bg=bg)
        self.search_container_autocomplete.pack(anchor=tk.W, fill=tk.X, side=tk.TOP)


        #Title Entry Field
        self.search_container_title = tk.Frame(filter_container, bg=bg)
        self.search_container_title.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        title_label = tk.Label(self.search_container_title, text='Title: ', bg=bg)
        title_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.title_var = tk.StringVar()

        self.title_entry = ttk.Entry(self.search_container_title, textvariable=self.title_var, state=tk.DISABLED)
        self.title_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)

        #Author Entry Field
        self.search_container_author = tk.Frame(filter_container, bg=bg)
        self.search_container_author.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        author_label = tk.Label(self.search_container_author, text='Author: ', bg=bg)
        author_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.author_var = tk.StringVar()

        self.author_entry = ttk.Entry(self.search_container_author, textvariable=self.author_var, state=tk.DISABLED)
        self.author_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Book recipient frame
        recipient_container = tk.Frame(filter_container, bg=bg)
        recipient_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        recipient_label = tk.Label(recipient_container, text='Recipient Email: ', bg=bg)
        recipient_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.recipient_var = tk.StringVar()

        recipient_entry = ttk.Entry(recipient_container, textvariable=self.recipient_var)
        recipient_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Date entry frame
        issue_date_container = tk.Frame(filter_container, bg=bg)
        issue_date_container.pack(anchor=tk.W, fill=tk.X, expand=True)

        recipient_label = tk.Label(issue_date_container, text='Date of Issuing: ', bg=bg)
        recipient_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.issue_date_entry = DateEntry(issue_date_container, width=12, background='darkblue',
                    foreground='white', borderwidth=2, mindate=datetime.now(), maxdate=datetime.now(), locale='en_UK')
        self.issue_date_entry.pack(padx=padx, pady=pady)



        #Return date frame
        return_date_container = tk.Frame(filter_container, bg=bg)
        return_date_container.pack(anchor=tk.W, fill=tk.X, expand=True)

        return_date_label = tk.Label(return_date_container, text='Expected Return Date: ', bg=bg)
        return_date_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        three_months_from_now = relativedelta(months=3)
        return_date_calc = self.issue_date_entry.get_date() + three_months_from_now

        self.actual_return_date_entry = DateEntry(return_date_container, width=12, background='darkblue',
                    foreground='white', borderwidth=2, mindate=datetime.now(), maxdate=return_date_calc, locale='en_UK')
        self.actual_return_date_entry.pack(padx=padx, pady=pady)


        #Issue Book Button Frame
        issue_book_container = tk.Frame(filter_container, bg=bg)
        issue_book_container.pack(anchor=tk.W, fill=tk.X, expand=True)


        issue_book_btn = ttk.Button(issue_book_container)
        issue_book_btn.config(text='    Issue Book    ', command=self.issue_book)
        issue_book_btn.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        # Gather an updated list of books to be displayed correctly on the autocomplete box.


        autocomplete_issue_bookID = AutoCompleteEntryBD_IssueBookID(self.search_container_autocomplete, self.title_entry, self.title_var, self.author_entry, self.author_var, self.bookID_var, self.bookID_entry, self.search_container_canvas)






        ### Book Return ('ret' following the variable name is short for 'return' to differentiate between the variables above and below)
        #Return Books UI
        ret_filter_container = tk.Frame(book_database_page, bg=bg)
        ret_filter_container.pack(side=tk.LEFT, anchor=tk.N, padx=padx, pady=pady)

        ret_filter_header = tk.Label(ret_filter_container, text='Return Book', font='System 18', bg=bg)
        ret_filter_header.pack(anchor=tk.W, padx=padx, pady=pady)

        #BookID Entry Field
        self.ret_search_container_bookID = tk.Frame(ret_filter_container, bg=bg)
        self.ret_search_container_bookID.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        ret_bookID_label = tk.Label(self.ret_search_container_bookID, text='ID: ', bg=bg)
        ret_bookID_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.ret_bookID_reg = root.register(self.ret_bookID_validate)
        self.ret_bookID_var = tk.StringVar()

        self.ret_bookID_entry = ttk.Entry(self.ret_search_container_bookID)
        self.ret_bookID_entry.config(textvariable=self.ret_bookID_var, validate="key",
                            validatecommand=(self.ret_bookID_reg, "%P"))
        self.ret_bookID_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Filler frame for the autocomplete function
        self.ret_search_container_canvas = tk.Canvas(ret_filter_container, height=50, width=50, bg=bg)
        self.ret_search_container_canvas.pack(fill=tk.X, expand=True)

        self.ret_search_container_autocomplete = tk.Frame(self.ret_search_container_canvas, bg=bg)
        self.ret_search_container_autocomplete.pack(anchor=tk.W, fill=tk.X, side=tk.TOP)


        #Title Entry Field
        self.ret_search_container_title = tk.Frame(ret_filter_container, bg=bg)
        self.ret_search_container_title.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        ret_title_label = tk.Label(self.ret_search_container_title, text='Title: ', bg=bg)
        ret_title_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.ret_title_var = tk.StringVar()

        self.ret_title_entry = ttk.Entry(self.ret_search_container_title, textvariable=self.ret_title_var, state=tk.DISABLED)
        self.ret_title_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)

        #Author Entry Field
        self.ret_search_container_author = tk.Frame(ret_filter_container, bg=bg)
        self.ret_search_container_author.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        ret_author_label = tk.Label(self.ret_search_container_author, text='Author: ', bg=bg)
        ret_author_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.ret_author_var = tk.StringVar()

        self.ret_author_entry = ttk.Entry(self.ret_search_container_author, textvariable=self.ret_author_var, state=tk.DISABLED)
        self.ret_author_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Book recipient frame
        ret_recipient_container = tk.Frame(ret_filter_container, bg=bg)
        ret_recipient_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        ret_recipient_label = tk.Label(ret_recipient_container, text='Return Email: ', bg=bg)
        ret_recipient_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.return_email_var = tk.StringVar()

        ret_recipient_entry = ttk.Entry(ret_recipient_container, textvariable=self.return_email_var)
        ret_recipient_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Date entry frame
        ret_date_container = tk.Frame(ret_filter_container, bg=bg)
        ret_date_container.pack(anchor=tk.W, fill=tk.X, expand=True)

        ret_recipient_label = tk.Label(ret_date_container, text='Date of Return: ', bg=bg)
        ret_recipient_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.ret_date_entry = DateEntry(ret_date_container, width=12, background='darkblue',
                    foreground='white', borderwidth=2, mindate=datetime.now(), maxdate=datetime.now(), locale='en_UK')
        self.ret_date_entry.pack(padx=padx, pady=pady)



        #Return Book Button Frame
        return_book_container = tk.Frame(ret_filter_container, bg=bg)
        return_book_container.pack(anchor=tk.W, fill=tk.X, expand=True)


        return_book_btn = ttk.Button(return_book_container)
        return_book_btn.config(text='    Return Book    ', command=self.return_book)
        return_book_btn.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)


        autocomplete_return_bookID = AutoCompleteEntryBD_ReturnBookID(self.ret_search_container_autocomplete, self.ret_title_entry, self.ret_title_var, self.ret_author_entry, self.ret_author_var, self.ret_bookID_var, self.ret_bookID_entry, self.ret_date_entry, self.ret_search_container_canvas)





        #Remove Books UI
        remove_book_container = tk.Frame(book_database_page, bg=bg)
        remove_book_container.pack(side=tk.RIGHT, anchor=tk.N, padx=padx, pady=pady)

        remove_book_header = tk.Label(remove_book_container, text='Remove Book From System', font='System 18', bg=bg)
        remove_book_header.pack(anchor=tk.W, padx=padx, pady=pady)

        #BookID Entry Field
        self.remove_container_bookID = tk.Frame(remove_book_container, bg=bg)
        self.remove_container_bookID.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        remove_bookID_label = tk.Label(self.remove_container_bookID, text='ID: ', bg=bg)
        remove_bookID_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.remove_bookID_reg = root.register(self.remove_bookID_validate)
        self.remove_bookID_var = tk.StringVar()

        self.remove_bookID_entry = ttk.Entry(self.remove_container_bookID)
        self.remove_bookID_entry.config(textvariable=self.remove_bookID_var, validate="key",
                            validatecommand=(self.remove_bookID_reg, "%P"))
        self.remove_bookID_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)

        #Filler frame for the autocomplete function
        self.remove_container_canvas = tk.Canvas(remove_book_container, height=50, width=50, bg=bg)
        self.remove_container_canvas.pack(fill=tk.X, expand=True)

        self.remove_container_autocomplete = tk.Frame(self.remove_container_canvas, bg=bg)
        self.remove_container_autocomplete.pack(anchor=tk.W, fill=tk.X, side=tk.TOP)


        #Title Entry Field
        self.remove_container_title = tk.Frame(remove_book_container, bg=bg)
        self.remove_container_title.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        remove_title_label = tk.Label(self.remove_container_title, text='Title: ', bg=bg)
        remove_title_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.remove_title_var = tk.StringVar()

        self.remove_title_entry = ttk.Entry(self.remove_container_title, textvariable=self.remove_title_var, state=tk.DISABLED)
        self.remove_title_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Author Entry Field
        self.remove_container_author = tk.Frame(remove_book_container, bg=bg)
        self.remove_container_author.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        remove_author_label = tk.Label(self.remove_container_author, text='Author: ', bg=bg)
        remove_author_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.remove_author_var = tk.StringVar()

        self.remove_author_entry = ttk.Entry(self.remove_container_author, textvariable=self.remove_author_var, state=tk.DISABLED)
        self.remove_author_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Genre Entry Field
        self.remove_container_genre = tk.Frame(remove_book_container, bg=bg)
        self.remove_container_genre.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        remove_genre_label = tk.Label(self.remove_container_genre, text='Genre: ', bg=bg)
        remove_genre_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.remove_genre_var = tk.StringVar()
        self.remove_genre_var.set("-EMPTY-")

        self.remove_genre_menu = ttk.OptionMenu(self.remove_container_genre, self.remove_genre_var,genre_choice_list[0], *genre_choice_list)
        self.remove_genre_menu.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Remove Book Button Frame
        remove_book_container = tk.Frame(remove_book_container, bg=bg)
        remove_book_container.pack(anchor=tk.W, fill=tk.X, expand=True)


        remove_book_btn = ttk.Button(remove_book_container)
        remove_book_btn.config(text='    Remove Book    ', command=self.remove_book)
        remove_book_btn.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        autocomplete_remove_bookID = AutoCompleteEntryBD_RemoveBookID(self.remove_container_autocomplete, self.remove_title_entry, self.remove_title_var,self.remove_author_entry, self.remove_author_var, self.remove_bookID_var, self.remove_bookID_entry, self.remove_genre_var, self.remove_genre_menu, self.remove_container_canvas)


        #Add Books UI
        add_book_container = tk.Frame(book_database_page, bg=bg)
        add_book_container.pack(side=tk.RIGHT, anchor=tk.N, padx=padx, pady=pady)

        add_book_header = tk.Label(add_book_container, text='Add Book Into System', font='System 18', bg=bg)
        add_book_header.pack(anchor=tk.W, padx=padx, pady=pady)

        #BookID Entry Field
        self.add_container_bookID = tk.Frame(add_book_container, bg=bg)
        self.add_container_bookID.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        add_bookID_label = tk.Label(self.add_container_bookID, text='ID: ', bg=bg)
        add_bookID_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.add_bookID_var = tk.StringVar()

        select_highest_val = c.execute('SELECT MAX(bookID) + 1 FROM Books').fetchall()
        highest_val = [x[0] for x in select_highest_val][0]

        self.add_bookID_var.set(highest_val)

        self.add_bookID_entry = ttk.Entry(self.add_container_bookID, textvariable=self.add_bookID_var, state=tk.DISABLED)
        self.add_bookID_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Title Entry Field
        self.add_container_title = tk.Frame(add_book_container, bg=bg)
        self.add_container_title.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        add_title_label = tk.Label(self.add_container_title, text='Title: ', bg=bg)
        add_title_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.add_title_var = tk.StringVar()

        self.add_title_entry = ttk.Entry(self.add_container_title, textvariable=self.add_title_var)
        self.add_title_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Author Entry Field
        self.add_container_author = tk.Frame(add_book_container, bg=bg)
        self.add_container_author.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        add_author_label = tk.Label(self.add_container_author, text='Author: ', bg=bg)
        add_author_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.add_author_var = tk.StringVar()

        self.add_author_entry = ttk.Entry(self.add_container_author, textvariable=self.add_author_var)
        self.add_author_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Genre Entry Field
        self.add_container_genre = tk.Frame(add_book_container, bg=bg)
        self.add_container_genre.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        add_genre_label = tk.Label(self.add_container_genre, text='Genre: ', bg=bg)
        add_genre_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.add_genre_var = tk.StringVar()
        self.add_genre_var.set("-EMPTY-")

        self.add_genre_menu = ttk.OptionMenu(self.add_container_genre, self.add_genre_var,genre_choice_list[0], *genre_choice_list)
        self.add_genre_menu.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)

        #Add Book Button Frame
        add_book_container_button = tk.Frame(add_book_container, bg=bg)
        add_book_container_button.pack(anchor=tk.W, fill=tk.X, expand=True)


        add_book_btn = ttk.Button(add_book_container_button)
        add_book_btn.config(text='    Add Book    ', command=self.add_book)
        add_book_btn.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)


        #Add New Genre Entry Field
        self.container_newgenre = tk.Frame(add_book_container, bg=bg)
        self.container_newgenre.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)


        newgenre_main_label = tk.Label(self.container_newgenre, text='Add Genre Into the System', font='System 18', bg=bg)
        newgenre_main_label.pack(anchor=tk.W, padx=padx, pady=pady)


        newgenre_label = tk.Label(self.container_newgenre, text='Genre Name: ', bg=bg)
        newgenre_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.newgenre_var = tk.StringVar()

        self.newgenre_entry = ttk.Entry(self.container_newgenre, textvariable=self.newgenre_var)
        self.newgenre_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)

        #Add New Genre Button Frame
        container_newgenre_button = tk.Frame(add_book_container, bg=bg)
        container_newgenre_button.pack(anchor=tk.W, fill=tk.X, expand=True)


        add_newgenre_btn = ttk.Button(container_newgenre_button)
        add_newgenre_btn.config(text='    Add New Genre    ', command=self.add_newgenre)
        add_newgenre_btn.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        remove_newgenre_btn = ttk.Button(container_newgenre_button)
        remove_newgenre_btn.config(text='    Remove Genre    ', command=self.remove_newgenre)
        remove_newgenre_btn.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

    def add_newgenre(self):
        #Requires input validation

        #Fetch entry field values
        newgenre_var = self.newgenre_var.get()
        
        #Check if the entered genre already exists
        c.execute("SELECT genre FROM Genres")
        genres_list_fetch = c.fetchall()
        genre_choice_list = [x[0] for x in genres_list_fetch]

        if newgenre_var in genre_choice_list:
            ms.showerror('Error','This genre is already in the system.')
        else:
            #Add new genre to db
            insert_newgenre = 'INSERT INTO Genres(genre) VALUES(?)'
            c.execute(insert_newgenre,[(newgenre_var)])
            conn.commit()

            #Update genre_choice_list and the related OptionMenus
            #List of genres
            c.execute("SELECT genre FROM Genres")
            genres_list_fetch = c.fetchall()
            genre_choice_list = [x[0] for x in genres_list_fetch]

            #Update Add Book OptionMenu in BookDB Page
            add_menu = self.add_genre_menu["menu"]
            add_menu.delete(0, tk.END)
            for string in genre_choice_list:
                add_menu.add_command(label=string,
                                 command=lambda value=string: self.add_genre_var.set(value))

            #Update Remove Book OptionMenu in BookDB Page
            remove_menu = self.remove_genre_menu["menu"]
            remove_menu.delete(0, tk.END)
            for string in genre_choice_list:
                remove_menu.add_command(label=string,
                                 command=lambda value=string: self.add_genre_var.set(value))

            #Update genre search in bookDB page
            search_genre_menu = self.db_search_genre_menu["menu"]
            search_genre_menu.delete(0, tk.END)
            for string in genre_choice_list:
                search_genre_menu.add_command(label=string,
                                 command=lambda value=string: self.db_search_genre_var.set(value))

            ms.showinfo('Success', 'Genre added to the database successfully')



    def remove_newgenre(self):
        #Requires input validation

        #Fetch entry field values
        newgenre_var = self.newgenre_var.get()
        
        #Check if the entered genre already exists
        c.execute("SELECT genre FROM Genres")
        genres_list_fetch = c.fetchall()
        genre_choice_list = [x[0] for x in genres_list_fetch]

        if newgenre_var not in genre_choice_list:
            ms.showerror('Error',"This genre isn't in the system.")
        elif newgenre_var == '-EMPTY-':
            ms.showerror("Error","You cannot remove this genre.")
        else:
            #Find if the genre is being used by any books
            used_genre_fetch = c.execute('SELECT genre FROM Books WHERE genre=?',(newgenre_var,)).fetchall()
            used_genre = [x[0] for x in used_genre_fetch]

            if len(used_genre) > 0:
                ms.showerror('Error','Genre is currently in use by other books')
            else:
                #Remove new genre from db
                remove_genre = c.execute('DELETE FROM Genres WHERE genre=?',(newgenre_var,))
                conn.commit()

                #Update genre_choice_list and the related OptionMenus
                #List of genres
                c.execute("SELECT genre FROM Genres")
                genres_list_fetch = c.fetchall()
                genre_choice_list = [x[0] for x in genres_list_fetch]

                add_menu = self.add_genre_menu["menu"]
                add_menu.delete(0, tk.END)
                for string in genre_choice_list:
                    add_menu.add_command(label=string,
                                            command=lambda value=string: self.remove_genre_var.set(value))

                #Update Remove Book OptionMenu in BookDB Page
                remove_menu = self.remove_genre_menu["menu"]
                remove_menu.delete(0, tk.END)
                for string in genre_choice_list:
                    remove_menu.add_command(label=string,
                                     command=lambda value=string: self.remove_genre_var.set(value))

                #Update genre search in bookDB page
                search_genre_menu = self.db_search_genre_menu["menu"]
                search_genre_menu.delete(0, tk.END)
                for string in genre_choice_list:
                    search_genre_menu.add_command(label=string,
                                     command=lambda value=string: self.db_search_genre_var.set(value))

                ms.showinfo('Success', 'Genre removed from the database successfully')



    def add_book(self):

        #Fetch entry field values
        add_bookID_var = self.add_bookID_var.get()
        add_title_var = self.add_title_var.get()
        add_author_var =  self.add_author_var.get()
        add_genre_var = self.add_genre_var.get()

        #The location of the book within the physical library, will be based on the first letter of its Title.
        #The shelves will be split into 27 different locations (alphabet + an '*' to signify any book whose title doesn't start with an alphabetical character.)
        #Example, Title= 1 step closer. Location=*
        #Example 2, Title=Drowning, Location=D

        for letter in string.ascii_uppercase:
            if letter == add_title_var[0]:
                location=letter
            elif add_title_var[0] not in string.ascii_uppercase:
                location='*'

        #Insert fetched values into database
        insert_book_info = 'INSERT INTO Books(bookID, title, author, genre, issued, location) VALUES(?,?,?,?,0,?)'
        c.execute(insert_book_info,[(add_bookID_var), (add_title_var), (add_author_var), (add_genre_var),(location)])
        conn.commit()

        #Increase the displayed bookID on the Add Book section
        select_highest_val = c.execute('SELECT MAX(bookID) + 1 FROM Books').fetchall()
        highest_val = [x[0] for x in select_highest_val][0]

        self.add_bookID_var.set(highest_val)

        #Set entryfields to empty after addition
        self.add_title_var.set('')
        self.add_author_var.set('')


        #Update TreeView
        #Book IDs
        c.execute("SELECT bookID FROM Books")
        bookIDs_fetch = c.fetchall()
        bookID_list = [x[0] for x in bookIDs_fetch]

        #Titles
        c.execute("SELECT title FROM Books")
        title_fetch = c.fetchall()
        title_list = [x[0] for x in title_fetch]

        #Authors
        c.execute("SELECT author FROM Books")
        author_fetch = c.fetchall()
        author_list = [x[0] for x in author_fetch]

        #Genres
        c.execute("SELECT genre FROM Books")
        genre_fetch = c.fetchall()
        genre_list = [x[0] for x in genre_fetch]

        #location
        c.execute("SELECT location FROM Books")
        location_fetch = c.fetchall()
        location_list = [x[0] for x in location_fetch]

        #Issued/Not Issued
        c.execute("SELECT issued FROM Books")
        issued_fetch = c.fetchall()
        issued_list = [x[0] for x in issued_fetch]

        for k in self.tree.get_children():
            self.tree.delete(k)

        for i in range(len(bookID_list)):
            #Issue Date
            c.execute("SELECT date_issued FROM MyBooks WHERE user_id=(SELECT user_id WHERE bookID=?)",(bookID_list[i],))
            date_issued_fetch = c.fetchall()
            date_issued_list = [x[0] for x in date_issued_fetch]

            #Return Date
            c.execute("SELECT return_date FROM MyBooks WHERE user_id=(SELECT user_id WHERE bookID=?)",(bookID_list[i],))
            return_date_fetch = c.fetchall()
            return_date_list = [x[0] for x in return_date_fetch]

            #creates an entry in the tree for each element of the list
            #then stores the id of the tree in the self.ids list
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
        
        #Fetch entry field values
        remove_bookID_var = self.remove_bookID_var.get()

        remove_bookID_search = c.execute('DELETE FROM Books WHERE bookID=?',(remove_bookID_var,))
        conn.commit()

        #Check if anyone owns said book and remove it from their My Books table
        check_book_owned = c.execute('SELECT user_id FROM MyBooks WHERE bookID=?',(remove_bookID_var,)).fetchall()
        book_owner = [x[0] for x in check_book_owned]

        if len(book_owner)==1:
            remove_bookID_search = c.execute('DELETE FROM MyBooks WHERE bookID=?',(remove_bookID_var,))
            conn.commit()

        #Set entryfields to empty after removal
        self.remove_bookID_var.set('')
        self.remove_title_var.set('')
        self.remove_author_var.set('')

        #Update TreeView
        #Book IDs
        c.execute("SELECT bookID FROM Books")
        bookIDs_fetch = c.fetchall()
        bookID_list = [x[0] for x in bookIDs_fetch]

        #Titles
        c.execute("SELECT title FROM Books")
        title_fetch = c.fetchall()
        title_list = [x[0] for x in title_fetch]

        #Authors
        c.execute("SELECT author FROM Books")
        author_fetch = c.fetchall()
        author_list = [x[0] for x in author_fetch]

        #Genres
        c.execute("SELECT genre FROM Books")
        genre_fetch = c.fetchall()
        genre_list = [x[0] for x in genre_fetch]

        #location
        c.execute("SELECT location FROM Books")
        location_fetch = c.fetchall()
        location_list = [x[0] for x in location_fetch]

        #Issued/Not Issued
        c.execute("SELECT issued FROM Books")
        issued_fetch = c.fetchall()
        issued_list = [x[0] for x in issued_fetch]

        for k in self.tree.get_children():
            self.tree.delete(k)

        for i in range(len(bookID_list)):
            #Issue Date
            c.execute("SELECT date_issued FROM MyBooks WHERE user_id=(SELECT user_id WHERE bookID=?)",(bookID_list[i],))
            date_issued_fetch = c.fetchall()
            date_issued_list = [x[0] for x in date_issued_fetch]

            #Return Date
            c.execute("SELECT return_date FROM MyBooks WHERE user_id=(SELECT user_id WHERE bookID=?)",(bookID_list[i],))
            return_date_fetch = c.fetchall()
            return_date_list = [x[0] for x in return_date_fetch]

            #creates an entry in the tree for each element of the list
            #then stores the id of the tree in the self.ids list
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
        #Send entered information to the database.
        #May need try/except block here
        bookID_var = self.bookID_var.get()
        title_var = self.title_var.get()
        author_var = self.author_var.get()
        recipient_email = self.recipient_var.get()
        date_issued = self.issue_date_entry.get_date()

        date_issued_string = str(date_issued.strftime('%d-%m-%Y'))

        if str(date_issued_string) == str(datetime.today().strftime('%d-%m-%Y')):
            expected_return_date = self.actual_return_date_entry.get_date()

            book_id_search = c.execute('SELECT bookID FROM Books WHERE title=? AND author=? ',(title_var, author_var)).fetchall()
            book_id = [x[0] for x in book_id_search][0]

            # Send info to db
            account_info_fetch = c.execute('SELECT * FROM Accounts WHERE email_address=?',(recipient_email,)).fetchall()
            if len(account_info_fetch) != 0:
                accounts_userid_check = [x[0] for x in account_info_fetch][0]

                #Check if book is already issued out
                book_already_issued_fetch = c.execute('SELECT issued FROM Books WHERE bookID=?',(bookID_var,)).fetchall()
                book_already_issued = [x[0] for x in book_already_issued_fetch][0]

                if book_already_issued == 0:
                    insert_my_bookID = 'INSERT INTO MyBooks(user_id,bookID) VALUES(?,?)'
                    c.execute(insert_my_bookID,[(accounts_userid_check),(book_id)])
                    conn.commit()

                    update_issued_val = c.execute('UPDATE Books SET issued=1 WHERE bookID=?',(book_id,))
                    conn.commit()

                    update_date_issued_val = c.execute("""UPDATE MyBooks
                        SET date_issued=?
                        WHERE user_id = (SELECT user_id FROM Accounts WHERE email_address=?)
                        AND bookID=?""",(date_issued, recipient_email, bookID_var))
                    conn.commit()

                    update_return_date_val = c.execute("""UPDATE MyBooks
                        SET return_date=?
                        WHERE user_id = (SELECT user_id FROM Accounts WHERE email_address=?)
                        AND bookID=?""",(expected_return_date, recipient_email, bookID_var))
                    conn.commit()

                    #Fetch Location
                    book_location_fetch = c.execute("SELECT location FROM Books WHERE bookID=?",(bookID_var,)).fetchall()
                    book_location = [x[0] for x in book_location_fetch][0]

                    #Fetch genre
                    book_genre_fetch = c.execute("SELECT genre FROM Books WHERE bookID=?",(bookID_var,)).fetchall()
                    book_genre = [x[0] for x in book_genre_fetch][0]


                    e = Email()
                    service = e.get_service()
                    message = e.create_issuing_message("from@gmail.com",recipient_email,"Books4All Book Issued", title_var, author_var, book_genre, book_location, date_issued, expected_return_date)
                    e.send_message(service,"from@gmail.com",message)

                    ms.showinfo('Success', 'Book issued out successfully\nAn email has been sent to\n'+recipient_email+'\nregarding the issuing information.')
                else:
                    ms.showerror('Error','This book has already been issued.')

                #Set entryfields to empty after issue
                self.bookID_var.set('')
                self.title_var.set('')
                self.author_var.set('')
                self.recipient_var.set('')

                #update treeview BookDatabase when the book is issued
                #gather db info to check if book has been issued, so that we only show the books that have NOT been issued.

                #Book IDs
                c.execute("SELECT bookID FROM Books")
                bookIDs_fetch = c.fetchall()
                bookID_list = [x[0] for x in bookIDs_fetch]

                #Titles
                c.execute("SELECT title FROM Books")
                title_fetch = c.fetchall()
                title_list = [x[0] for x in title_fetch]

                #Authors
                c.execute("SELECT author FROM Books")
                author_fetch = c.fetchall()
                author_list = [x[0] for x in author_fetch]

                #Genres
                c.execute("SELECT genre FROM Books")
                genre_fetch = c.fetchall()
                genre_list = [x[0] for x in genre_fetch]

                #location
                c.execute("SELECT location FROM Books")
                location_fetch = c.fetchall()
                location_list = [x[0] for x in location_fetch]

                #Issued/Not Issued
                c.execute("SELECT issued FROM Books")
                issued_fetch = c.fetchall()
                issued_list = [x[0] for x in issued_fetch]

                for k in self.tree.get_children():
                    self.tree.delete(k)

                for i in range(len(bookID_list)):
                    #Issue Date
                    c.execute("SELECT date_issued FROM MyBooks WHERE user_id=(SELECT user_id WHERE bookID=?)",(bookID_list[i],))
                    date_issued_fetch = c.fetchall()
                    date_issued_list = [x[0] for x in date_issued_fetch]

                    #Return Date
                    c.execute("SELECT return_date FROM MyBooks WHERE user_id=(SELECT user_id WHERE bookID=?)",(bookID_list[i],))
                    return_date_fetch = c.fetchall()
                    return_date_list = [x[0] for x in return_date_fetch]

                    #creates an entry in the tree for each element of the list
                    #then stores the id of the tree in the self.ids list
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
        else:
            ms.showerror('Error','Invalid DOI (Date of Issue)')



    def return_book(self):
        #Send entered information to the database.
        #Retrieve all entryboxes variables

        #May need try/except block here
        title_var = self.ret_title_var.get()
        author_var = self.ret_author_var.get()
        return_email = self.return_email_var.get()
        actual_return_date = self.ret_date_entry.get_date()

        book_id_search = c.execute('SELECT bookID FROM Books WHERE title=? AND author=? ',(title_var, author_var)).fetchall()
        book_id = [x[0] for x in book_id_search][0]

        # Send info to db
        #could be shortened a bit.
        account_info_fetch = c.execute('SELECT * FROM Accounts WHERE email_address=?',(return_email,)).fetchall()

        #Check if email matches the owner of the loaned book.
        book_owner_email_fetch = c.execute('SELECT email_address FROM Accounts WHERE user_id=(SELECT user_id FROM MyBooks WHERE bookID=?)',(book_id,)).fetchall()
        book_owner_email = [x[0] for x in book_owner_email_fetch][0]

        print(return_email, book_owner_email)
        if return_email != book_owner_email:
            ms.showerror('Error','Email address does not match its rightful owner.')
        else:
            if len(account_info_fetch) != 0:
                accounts_userid_check = [x[0] for x in account_info_fetch][0]

                update_issued_val = c.execute('UPDATE MyBooks SET actual_return_date=? WHERE bookID=?',(actual_return_date, book_id,))
                conn.commit()

                #Check if the user has returned on time
                accounts_return_date_fetch = c.execute('SELECT return_date FROM MyBooks WHERE user_id=?',(accounts_userid_check,)).fetchall()
                accounts_return_date_check = [x[0] for x in accounts_return_date_fetch][0]

                accounts_return_date_check_time = datetime.strptime(accounts_return_date_check, '%Y-%m-%d').date()

                if accounts_return_date_check_time > actual_return_date:
                    #Handed late
                    #Find the number of days the book is late by.
                    days_since_return_date = (accounts_return_date_check_time - actual_return_date)
                    #Format the output to be just an integer days to fetch just the integer
                    days_since_return_date_formatted = str(days_since_return_date).split("d")[0]
                    #Fetch the number in string and convert it into an absolute value integer.
                    days_since_return_date_formatted_integer = int(re.search(r'\d+', days_since_return_date_formatted).group())
                    result = ms.askyesno('Warning','This user has returned the book late by %s days\nDo you wish to Continue?' % days_since_return_date_formatted_integer)

                    if result == True:
                        remove_user_id = 'DELETE FROM MyBooks WHERE bookID=?'
                        c.execute(remove_user_id,[(book_id)])
                        conn.commit()

                        update_issued_val = c.execute('UPDATE Books SET issued=0 WHERE bookID=?',(book_id,))
                        conn.commit()

                        #Set entryfields to empty after return
                        self.ret_bookID_var.set('')
                        self.ret_title_var.set('')
                        self.ret_author_var.set('')
                        self.return_email_var.set('')

                        ms.showinfo('Success', 'Book returned successfully')

                    else:
                        ms.showerror('Cancelled','Book return cancelled')

                elif accounts_return_date_check_time <= actual_return_date:
                    #Handed on time

                    #Fetch Location
                    book_location_fetch = c.execute("SELECT location FROM Books WHERE bookID=?",(book_id,)).fetchall()
                    book_location = [x[0] for x in book_location_fetch][0]

                    #Fetch genre
                    book_genre_fetch = c.execute("SELECT genre FROM Books WHERE bookID=?",(book_id,)).fetchall()
                    book_genre = [x[0] for x in book_genre_fetch][0]

                    #Fetch date issued
                    book_date_issued_fetch = c.execute("SELECT date_issued FROM MyBooks WHERE bookID=?",(book_id,)).fetchall()
                    date_issued = [x[0] for x in book_date_issued_fetch][0]

                    expected_return_date = accounts_return_date_check_time

                    e = Email()
                    service = e.get_service()
                    message = e.create_return_message("from@gmail.com",return_email,"Books4All Book Issued", title_var, author_var, book_genre, book_location, date_issued, expected_return_date, actual_return_date)
                    e.send_message(service,"from@gmail.com",message)

                    #Remove user_id from the ownership of the user and onto the public library.
                    remove_user_id = 'DELETE FROM MyBooks WHERE bookID=?'
                    c.execute(remove_user_id,[(book_id)])
                    conn.commit()

                    update_issued_val = c.execute('UPDATE Books SET issued=0 WHERE bookID=?',(book_id,))
                    conn.commit()

                    ms.showinfo('Success', 'Book returned out successfully\nAn email has been sent to\n'+return_email+'\nregarding the return information.')



                #Set entryfields to empty after return
                self.ret_bookID_var.set('')
                self.ret_title_var.set('')
                self.ret_author_var.set('')
                self.return_email_var.set('')

                #Update Treeview table in BookDatabase Page
                #Maybe pack into a function?
                #Book IDs
                #compress
                c.execute("SELECT bookID FROM Books")
                bookIDs_fetch = c.fetchall()
                bookID_list = [x[0] for x in bookIDs_fetch]

                #Titles
                c.execute("SELECT title FROM Books")
                title_fetch = c.fetchall()
                title_list = [x[0] for x in title_fetch]

                #Authors
                c.execute("SELECT author FROM Books")
                author_fetch = c.fetchall()
                author_list = [x[0] for x in author_fetch]

                #Genres
                c.execute("SELECT genre FROM Books")
                genre_fetch = c.fetchall()
                genre_list = [x[0] for x in genre_fetch]

                #location
                c.execute("SELECT location FROM Books")
                location_fetch = c.fetchall()
                location_list = [x[0] for x in location_fetch]

                #Issued/Not Issued
                c.execute("SELECT issued FROM Books")
                issued_fetch = c.fetchall()
                issued_list = [x[0] for x in issued_fetch]

                for k in self.tree.get_children():
                    self.tree.delete(k)

                for i in range(len(bookID_list)):
                    #Issue Date
                    c.execute("SELECT date_issued FROM MyBooks WHERE user_id=(SELECT user_id WHERE bookID=?)",(bookID_list[i],))
                    date_issued_fetch = c.fetchall()
                    date_issued_list = [x[0] for x in date_issued_fetch]

                    #Return Date
                    c.execute("SELECT return_date FROM MyBooks WHERE user_id=(SELECT user_id WHERE bookID=?)",(bookID_list[i],))
                    return_date_fetch = c.fetchall()
                    return_date_list = [x[0] for x in return_date_fetch]

                    #creates an entry in the tree for each element of the list
                    #then stores the id of the tree in the self.ids list
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

    def bookID_validate(self, bookID_input):
        if bookID_input.isdigit():
            return True
        elif bookID_input is "":
            return True
        else:
            return False

    def ret_bookID_validate(self, ret_bookID_input):
        if ret_bookID_input.isdigit():
            return True
        elif ret_bookID_input is "":
            return True
        else:
            return False

    def remove_bookID_validate(self, remove_bookID_input):
        if remove_bookID_input.isdigit():
            return True
        elif remove_bookID_input is "":
            return True
        else:
            return False



    def _columns_searcher_bookID_BD(self, *args):
        children = list(self._detached) + list(self.tree.get_children())
        self._detached = set()
        query_bookID = self.db_search_bookID_var.get()

        self.search_bookID_tv_BD(children, query_bookID)

    def _columns_searcher_title_BD(self, *args):
        children = list(self._detached) + list(self.tree.get_children())
        self._detached = set()
        query_title = self.db_search_title_var.get()

        self.search_title_tv_BD(children, query_title)

    def _columns_searcher_author_BD(self, *args):
        children = list(self._detached) + list(self.tree.get_children())
        self._detached = set()
        query_author = self.db_search_author_var.get()

        self.search_author_tv_BD(children, query_author)

    def _columns_searcher_genre_BD(self, *args):
        children = list(self._detached) + list(self.tree.get_children())
        self._detached = set()
        query_genre = self.db_search_genre_var.get()

        self.search_genre_tv_BD(children, query_genre)

    def _columns_searcher_location_BD(self, *args):
        children = list(self._detached) + list(self.tree.get_children())
        self._detached = set()
        query_location = self.db_search_location_var.get()

        self.search_location_tv_BD(children, query_location)

    def _columns_searcher_issued_BD(self, *args):
        children = list(self._detached) + list(self.tree.get_children())
        self._detached = set()
        query_issued = self.db_search_issued_var.get()

        self.search_issued_tv_BD(children, query_issued)

    def search_bookID_tv_BD(self, children, query_bookID):
        i_r = -1

        for item_id in children:
            bookID_text = str(self.tree.item(item_id)['values'][0])

            if query_bookID in bookID_text:
                i_r += 1
                self.tree.reattach(item_id, '', i_r)

            else:
                self._detached.add(item_id)
                self.tree.detach(item_id)

    def search_title_tv_BD(self, children, query_title):
        i_r = -1

        for item_id in children:
            title_text = self.tree.item(item_id)['values'][1]

            if query_title in title_text:
                i_r += 1
                self.tree.reattach(item_id, '', i_r)

            else:
                self._detached.add(item_id)
                self.tree.detach(item_id)

    def search_author_tv_BD(self, children, query_author):
        i_r = -1

        for item_id in children:
            author_text = self.tree.item(item_id)['values'][2]

            if query_author in author_text:
                i_r += 1
                self.tree.reattach(item_id, '', i_r)

            else:
                self._detached.add(item_id)
                self.tree.detach(item_id)

    def search_genre_tv_BD(self, children, query_genre):
        i_r = -1

        for item_id in children:
            genre_text = self.tree.item(item_id)['values'][3]

            if query_genre in genre_text:
                i_r += 1
                self.tree.reattach(item_id, '', i_r)

            elif query_genre == '-EMPTY-':
                self.tree.reattach(item_id, '', i_r)

            else:
                self._detached.add(item_id)
                self.tree.detach(item_id)

    def search_location_tv_BD(self, children, query_location):
        i_r = -1

        for item_id in children:
            location_text = self.tree.item(item_id)['values'][4]

            if query_location in location_text:
                i_r += 1
                self.tree.reattach(item_id, '', i_r)

            elif query_location == '-EMPTY-':
                self.tree.reattach(item_id, '', i_r)

            else:
                self._detached.add(item_id)
                self.tree.detach(item_id)

    def search_issued_tv_BD(self, children, query_issued):
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
        try:
            self.arr = [(int(self.tree.set(k, c)), k) for k in self.tree.get_children('')]
        except ValueError:
            self.arr = [(self.tree.set(k, c), k) for k in self.tree.get_children('')]
        self.n = len(self.arr)
        self.quickSort(self.tree, c, self.arr, 0, self.n-1, False)

    def partition(self, arr,low, high):
        i = (low-1)
        pivot = arr[high]
     
        for j in range(low, high):
            if arr[j] <= pivot:
                i = i+1
                arr[i], arr[j] = arr[j], arr[i]
     
        arr[i+1], arr[high] = arr[high], arr[i+1]

        return (i+1)
     
    def quickSort(self, tv, col, arr, low, high, reverse):
        #Need to update arr if a new value is added to the treeview
        if len(arr) == 1:
            return arr
        if low < high:
            # pi is partitioning index, arr[p] is now
            # at right place
            pi = self.partition(arr, low, high)
     
            # Separately sort elements before
            # partition and after partition
            self.quickSort(tv, col, arr, low, pi-1, reverse=reverse)
            self.quickSort(tv, col, arr, pi+1, high, reverse=reverse)

        for index, (val, k) in enumerate(arr):
            tv.move(k, '', index)

        tv.heading(col, command=lambda: \
            self.quickSort(tv, col, arr, low, high, not reverse))
        if reverse == True:
            arr_reverse = arr[::-1]
            for index, (val, k) in enumerate(arr_reverse):
                tv.move(k, '', index)



class AutoCompleteEntryBD_ReturnBookID(ttk.Entry):
    def __init__(self, ret_search_container_autocomplete, ret_title_entry, ret_title_var, ret_author_entry, ret_author_var, ret_bookID_var, ret_bookID_entry, ret_date_entry, ret_search_container_canvas, *args, **kwargs):

        self.ret_search_container_autocomplete = ret_search_container_autocomplete
        self.ret_bookID_entry = ret_bookID_entry
        self.ret_title_entry = ret_title_entry
        self.ret_author_entry = ret_author_entry
        self.ret_date_entry = ret_date_entry
        self.ret_search_container_canvas = ret_search_container_canvas

        # Listbox length
        if 'listboxLength' in kwargs:
            self.listboxLength = kwargs['listboxLength']
            del kwargs['listboxLength']
        else:
            self.listboxLength = 8


        ttk.Entry.__init__(self, *args, **kwargs)
        self.focus()

        #Fetch database books that have been issued (issued=1)
        #Titles
        c.execute("SELECT bookID FROM Books WHERE issued=1")
        issued_bookIDs_fetch = c.fetchall()
        issued_bookIDs_list = [x[0] for x in issued_bookIDs_fetch]

        self.listb = issued_bookIDs_list

        self.ret_bookID_var = ret_bookID_var
        self.ret_title_var = ret_title_var
        self.ret_author_var = ret_author_var

        self.ret_bookID_entry = self["textvariable"]
        if self.ret_bookID_entry == '':
            self.ret_bookID_entry = self["textvariable"] = tk.StringVar()

        self.ret_bookID_var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)
        
        self.lb_up = False

    def changed(self, name, index, mode):
        #Fetch database books that have been issued (issued=1)
        #Titles
        c.execute("SELECT bookID FROM Books WHERE issued=1")
        issued_bookIDs_fetch = c.fetchall()
        issued_bookIDs = [x[0] for x in issued_bookIDs_fetch]

        self.listb = issued_bookIDs

        if self.ret_search_container_autocomplete.winfo_ismapped() == False:
            self.ret_search_container_autocomplete.pack(anchor=tk.W, fill=tk.X, side=tk.TOP)


        if self.ret_bookID_var.get() == '':
            if self.lb_up:
                self.lb.destroy()
                self.lb_up = False
        else:
            words = self.comparison()
            if words:            
                if not self.lb_up:
                    self.lb = tk.Listbox(self.ret_search_container_canvas, width=self["width"], height=self.listboxLength)
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)
                    self.lb_up = True

                self.lb.delete(0, tk.END)


                for w in words:
                    self.lb.insert(tk.END,w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False

                    self.ret_search_container_autocomplete.pack_forget()
                    self.ret_search_container_canvas["height"]=0
                    self.ret_search_container_canvas["width"]=0
        
    def selection(self, event):
        if self.lb_up:
            self.ret_bookID_var.set(self.lb.get(tk.ACTIVE))

            book_title_fetch = c.execute('SELECT title FROM Books WHERE bookID=?',(self.ret_bookID_var.get(),)).fetchall()
            book_title = [x[0] for x in book_title_fetch][0]

            book_author_fetch = c.execute('SELECT author FROM Books WHERE bookID=?',(self.ret_bookID_var.get(),)).fetchall()
            book_author = [x[0] for x in book_author_fetch][0]

            #Fetch return date from table
            return_date_fetch = c.execute('SELECT return_date FROM MyBooks WHERE bookID=?',(self.ret_bookID_var.get(),)).fetchall()
            return_date = [x[0] for x in return_date_fetch][0]

            self.ret_title_var.set(book_title)
            self.ret_author_var.set(book_author)
            self.ret_date_entry.set_date(datetime.strptime(return_date, '%Y-%m-%d'))

            self.ret_search_container_autocomplete.pack_forget()
            self.ret_search_container_canvas["height"]=0
            self.ret_search_container_canvas["width"]=0

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
        pattern = re.compile('.*' + self.ret_bookID_var.get() + '.*')
        return [w for w in self.listb if re.match(pattern, str(w))]




class AutoCompleteEntryBD_IssueBookID(ttk.Entry):
    def __init__(self, search_container_autocomplete, title_entry, title_var, author_entry, author_var, bookID_var, bookID_entry, search_container_canvas, *args, **kwargs):

        self.search_container_autocomplete = search_container_autocomplete
        self.search_container_canvas = search_container_canvas

        self.title_entry = title_entry
        self.author_entry = author_entry

        # Listbox length
        if 'listboxLength' in kwargs:
            self.listboxLength = kwargs['listboxLength']
            del kwargs['listboxLength']
        else:
            self.listboxLength = 8

        ttk.Entry.__init__(self, *args, **kwargs)
        self.focus()

        #Titles
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
        #Titles
        c.execute("SELECT bookID FROM Books WHERE issued=0")
        books_bookID_fetch = c.fetchall()
        book_bookID_list = [x[0] for x in books_bookID_fetch]

        self.lista = book_bookID_list

        if self.search_container_autocomplete.winfo_ismapped() == False:
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
                    self.lb.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)
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

            book_title_fetch = c.execute('SELECT title FROM Books WHERE bookID=?',(self.bookID_var.get(),)).fetchall()
            book_title = [x[0] for x in book_title_fetch][0]

            book_author_fetch = c.execute('SELECT author FROM Books WHERE bookID=?',(self.bookID_var.get(),)).fetchall()
            book_author = [x[0] for x in book_author_fetch][0]

            self.title_var.set(book_title)
            self.author_var.set(book_author)

            self.search_container_autocomplete.pack_forget()
            self.search_container_canvas["height"]=0
            self.search_container_canvas["width"]=0


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
    def __init__(self, remove_container_autocomplete, remove_title_entry, remove_title_var, remove_author_entry, remove_author_var, remove_bookID_var, remove_bookID_entry, remove_genre_var, remove_genre_menu, remove_container_canvas, *args, **kwargs):

        self.remove_container_autocomplete = remove_container_autocomplete
        self.remove_container_canvas = remove_container_canvas
        self.remove_title_entry = remove_title_entry
        self.remove_author_entry = remove_author_entry
        self.remove_genre_menu = remove_genre_menu

        # Listbox length
        if 'listboxLength' in kwargs:
            self.listboxLength = kwargs['listboxLength']
            del kwargs['listboxLength']
        else:
            self.listboxLength = 8

        ttk.Entry.__init__(self, *args, **kwargs)
        self.focus()

        #Titles
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
        #Titles
        c.execute("SELECT bookID FROM Books")
        books_bookID_fetch = c.fetchall()
        remove_book_bookID_list = [x[0] for x in books_bookID_fetch]

        self.lista = remove_book_bookID_list

        if self.remove_container_autocomplete.winfo_ismapped() == False:
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
                    self.lb.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)
                    self.lb_up = True

                self.lb.delete(0, tk.END)
                for w in words:
                    self.lb.insert(tk.END,w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False

                    self.remove_container_autocomplete.pack_forget()
                    self.remove_container_canvas["height"]=0
                    self.remove_container_canvas["width"]=0
        
    def selection(self, event):
        if self.lb_up:
            self.remove_bookID_var.set(self.lb.get(tk.ACTIVE))

            remove_book_title_fetch = c.execute('SELECT title FROM Books WHERE bookID=?',(self.remove_bookID_var.get(),)).fetchall()
            remove_book_title = [x[0] for x in remove_book_title_fetch][0]

            remove_book_author_fetch = c.execute('SELECT author FROM Books WHERE bookID=?',(self.remove_bookID_var.get(),)).fetchall()
            remove_book_author = [x[0] for x in remove_book_author_fetch][0]

            remove_book_genre_fetch = c.execute('SELECT genre FROM Books WHERE bookID=?',(self.remove_bookID_var.get(),)).fetchall()
            remove_book_genre = [x[0] for x in remove_book_genre_fetch][0]

            self.remove_title_var.set(remove_book_title)
            self.remove_author_var.set(remove_book_author)
            self.remove_genre_var.set(remove_book_genre)

            self.remove_container_autocomplete.pack_forget()
            self.remove_container_canvas["height"]=0
            self.remove_container_canvas["width"]=0


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