# Library Page

# Imports
import tkinter as tk
from tkinter import ttk
import sqlite3
import string
import re
import linecache


# Connect to the database
with sqlite3.connect('LibrarySystem.db') as db:
    c = db.cursor()

# File Configurations
WIDTH = re.sub('^.*?=', '', linecache.getline('config.txt', 1))
PADX = re.sub('^.*?=', '', linecache.getline('config.txt', 2))
PADY = re.sub('^.*?=', '', linecache.getline('config.txt', 3))
BG = re.sub('^.*?=', '', linecache.getline('config.txt', 6)).strip()
FONT = re.sub('^.*?=', '', linecache.getline('config.txt', 10)).strip()
HEADER_FONT = re.sub('^.*?=', '', linecache.getline('config.txt', 11)).strip()

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


class Library():
    '''
    Access Level: USER
    Functions: Allow the user to look at all available books in the database.
    '''
    def __init__(self, root, notebook):
        '''
        Initialise the visual layout of the system.
        '''

        # creates a list to store the ids of each entry in the tree
        self.tree_ids = []

        library_page = tk.Frame(notebook)
        notebook.add(library_page, text='Library')

        header_frame = tk.Frame(library_page)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        header = tk.Label(header_frame, text='Library', font=HEADER_FONT)
        header.pack(side=tk.TOP)

        # Library TreeView Book Database Frame
        tree_container = tk.Frame(library_page, bg=BG)
        tree_container.pack(side=tk.RIGHT, anchor=tk.N, padx=PADX)

        tree_header = tk.Label(tree_container, text='Database', font=FONT, bg=BG)
        tree_header.pack(padx=PADX, pady=PADY)

        # Set up TreeView table
        self.columns = ('Book ID', 'Title', 'Author', 'Genre', 'Location')
        self.tree = ttk.Treeview(tree_container, columns=self.columns, show='headings')
        self.tree.heading("Book ID", text='Book ID')
        self.tree.heading("Title", text='Title')
        self.tree.heading("Author", text='Author')
        self.tree.heading("Genre", text='Genre')
        self.tree.heading("Location", text='Location')

        self.tree.column("Book ID", width=WIDTH, anchor=tk.CENTER)
        self.tree.column("Title", width=WIDTH, anchor=tk.CENTER)
        self.tree.column("Author", width=WIDTH, anchor=tk.CENTER)
        self.tree.column("Genre", width=WIDTH, anchor=tk.CENTER)
        self.tree.column("Location", width=WIDTH, anchor=tk.CENTER)

        # Library Book Database Filters Frame
        filter_container = tk.Frame(library_page, bg=BG)
        filter_container.pack(side=tk.LEFT, anchor=tk.N, padx=PADX, pady=PADY)

        filter_header = tk.Label(filter_container, text='Filters', font=FONT, bg=BG)
        filter_header.pack(anchor=tk.W, padx=PADX, pady=PADY)

        # BookID Filter
        search_container_bookID = tk.Frame(filter_container, bg=BG)
        search_container_bookID.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        bookID_label = tk.Label(search_container_bookID, text='Book ID: ', bg=BG)
        bookID_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.bookID_reg = root.register(self.bookID_validate)

        self._detached = set()
        self.bookID_var = tk.StringVar()
        self.bookID_var.trace("w", self._columns_searcher)

        self.bookID_entry = ttk.Entry(search_container_bookID)
        self.bookID_entry.config(textvariable=self.bookID_var, validate="key",
                            validatecommand=(self.bookID_reg, "%P"))

        self.bookID_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # Title Filter
        search_container_title = tk.Frame(filter_container, bg=BG)
        search_container_title.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        title_label = tk.Label(search_container_title, text='Title: ', bg=BG)
        title_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.title_var = tk.StringVar()
        self.title_var.trace("w", self._columns_searcher)

        self.title_entry = ttk.Entry(search_container_title, textvariable=self.title_var)

        self.title_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # Author Filter
        search_author_container = tk.Frame(filter_container, bg=BG)
        search_author_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        author_filter_label = tk.Label(search_author_container, text='Author:', bg=BG)
        author_filter_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.author_var = tk.StringVar()
        self.author_var.trace("w", self._columns_searcher)

        self.author_entry = ttk.Entry(search_author_container, textvariable=self.author_var, font='System 6')
        self.author_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # Genre Filter
        search_genre_container = tk.Frame(filter_container, bg=BG)
        search_genre_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        genre_filter_label = tk.Label(search_genre_container, text='Genre:', bg=BG)
        genre_filter_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.genre_var = tk.StringVar()
        self.genre_var.set("-EMPTY-")

        from functools import partial
        self.genre_menu = ttk.OptionMenu(search_genre_container, self.genre_var, genre_choice_list[0], *genre_choice_list, command=partial(self._columns_searcher))
        self.genre_menu.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # location Filter
        search_location_container = tk.Frame(filter_container, bg=BG)
        search_location_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        location_filter_label = tk.Label(search_location_container, text='Location:', bg=BG)
        location_filter_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.location_var = tk.StringVar()
        self.location_var.set("-EMPTY-")
        self.location_var.trace("w", self._columns_searcher)

        self.location_menu = ttk.OptionMenu(search_location_container, self.location_var,location_choice_list[0], *location_choice_list)
        self.location_menu.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        for self.col in self.columns:
                    self.tree.heading(self.col, text=self.col,
                                          command=lambda c=self.col: self.sort_upon_press(c))

        # This line will be called everytime the user changes tabs to update the library page.
        # All the filter entry fields are passed into the function, so that they can be set to an empty string upon switching tabs. Also to update the treeview to match the database.
        # The lambda shows that this will happen upon each event trigger and not all at once.
        notebook.bind("<<NotebookTabChanged>>", self.notebook_tab_change)

    def notebook_tab_change(self, event):
        # gather db info to check if book has been issued, so that we only show the books that have NOT been issued.
        # Call database fetch function to fetch latest values from database.
        db_fetch = self.database_fetch()
        # Extract the return values of the database fetch function.
        non_issued_bookID_list = db_fetch[0]
        non_issued_title_list = db_fetch[1]
        non_issued_author_list = db_fetch[2]
        non_issued_genre_list = db_fetch[3]
        non_issued_location_list = db_fetch[4]

        # Set all fields to be -EMPTY-
        self.bookID_var.set('')
        self.title_var.set('')
        self.author_var.set('')
        self.genre_var.set('-EMPTY-')
        self.location_var.set('-EMPTY-')

        for k in self.tree.get_children():
            self.tree.delete(k)

        for i in range(len(non_issued_bookID_list)):
            # creates an entry in the tree for each element of the list
            # then stores the id of the tree in the self.ids list
            self.tree_ids.append(self.tree.insert("", "end", values=(non_issued_bookID_list[i], non_issued_title_list[i], non_issued_author_list[i], non_issued_genre_list[i], non_issued_location_list[i])))
        self.tree.pack()

        for self.col in self.columns:
                    self.tree.heading(self.col, text=self.col,
                                          command=lambda c=self.col: self.sort_upon_press(c))

    def bookID_validate(self, bookID_input):
        if bookID_input.isdigit():
            return True
        elif bookID_input is "":
            return True
        else:
            return False

    def _columns_searcher(self, *args):
        children = list(self._detached) + list(self.tree.get_children())
        self._detached = set()
        query_bookID = str(self.bookID_var.get())
        query_title = str(self.title_var.get())
        query_author = str(self.author_var.get())
        query_genre = str(self.genre_var.get())

        query_location = str(self.location_var.get())

        self.search_tv(children, query_bookID, query_title, query_author, query_genre, query_location)

    def search_tv(self, children, query_bookID, query_title, query_author, query_genre, query_location):
        i_r = -1

        for item_id in children:
            bookID_text = str(self.tree.item(item_id)['values'][0])
            title_text = str(self.tree.item(item_id)['values'][1])
            author_text = str(self.tree.item(item_id)['values'][2])
            genre_text = str(self.tree.item(item_id)['values'][3])
            location_text = str(self.tree.item(item_id)['values'][4])

            if query_bookID != '':
                if query_bookID in bookID_text:
                    i_r += 1
                    self.tree.reattach(item_id, '', i_r)
                    query_location = str(self.location_var.get())
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
                    i_r +=1
                    self.tree.reattach(item_id, '', i_r)
                else:
                    self._detached.add(item_id)
                    self.tree.detach(item_id)

            else:
                self.tree.reattach(item_id, '', i_r)

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
        # Need to update arr if a new value is added to the treeview
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

    def database_fetch(self):
        # BookIDs
        c.execute("SELECT bookID FROM Books WHERE issued=0")
        non_issued_bookIDs_fetch = c.fetchall()
        non_issued_bookID_list = [x[0] for x in non_issued_bookIDs_fetch]

        c.execute("SELECT title FROM Books WHERE issued=0")
        non_issued_title_fetch = c.fetchall()
        non_issued_title_list = [x[0] for x in non_issued_title_fetch]

        # Authors
        c.execute("SELECT author FROM Books WHERE issued=0")
        non_issued_author_fetch = c.fetchall()
        non_issued_author_list = [x[0] for x in non_issued_author_fetch]

        # Genres
        c.execute("SELECT genre FROM Books WHERE issued=0")
        non_issued_genre_fetch = c.fetchall()
        non_issued_genre_list = [x[0] for x in non_issued_genre_fetch]

        # Locations
        c.execute('SELECT location FROM Books WHERE issued=0')
        non_issued_location_fetch = c.fetchall()
        non_issued_location_list = [x[0] for x in non_issued_location_fetch]

        return (non_issued_bookID_list, non_issued_title_list, non_issued_author_list, non_issued_genre_list, non_issued_location_list)
