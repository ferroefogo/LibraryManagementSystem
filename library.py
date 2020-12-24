#Library Page
#Treeview not showing, because <<NotebookTabChanged>> is not being called on when i log inm though it works when i use a guest login

import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox as ms
import string


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





class Library():
    #USER ACCESS
    #Look for more books in the database (VIEW ONLY).
    def __init__(self, root, notebook):
        self.tree_ids = [] #creates a list to store the ids of each entry in the tree

        library_page = tk.Frame(notebook)
        notebook.add(library_page, text='Library')

        notebook.bind("<<NotebookTabChanged>>", self.notebook_tab_change)
        root.bind("<F5>", self.refresh_page)

        header_frame = tk.Frame(library_page)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        header = tk.Label(header_frame, text='Library', font='System 30')
        header.pack(side=tk.TOP)

        # Library TreeView Book Database Frame
        tree_container = tk.Frame(library_page, bg=bg)
        tree_container.pack(side=tk.RIGHT, anchor=tk.N, padx=padx)

        tree_header = tk.Label(tree_container, text='Database', font='System 18', bg=bg)
        tree_header.pack(padx=padx, pady=pady)

        #Set up TreeView table
        self.columns = ('Book ID','Title', 'Author', 'Genre','Location')
        self.tree = ttk.Treeview(tree_container, columns=self.columns, show='headings') #create tree
        self.tree.heading("Book ID", text='Book ID')
        self.tree.heading("Title", text='Title')
        self.tree.heading("Author", text='Author')
        self.tree.heading("Genre", text='Genre')
        self.tree.heading("Location", text='Location')

        self.tree.column("Book ID", width=width, anchor=tk.CENTER)
        self.tree.column("Title", width=width, anchor=tk.CENTER)
        self.tree.column("Author", width=width, anchor=tk.CENTER)
        self.tree.column("Genre", width=width, anchor=tk.CENTER)
        self.tree.column("Location", width=width, anchor=tk.CENTER)

        #Library Book Database Filters Frame
        filter_container = tk.Frame(library_page, bg=bg)
        filter_container.pack(side=tk.LEFT, anchor=tk.N, padx=padx, pady=pady)

        filter_header = tk.Label(filter_container, text='Filters', font='System 18', bg=bg)
        filter_header.pack(anchor=tk.W, padx=padx, pady=pady)


        #BookID Filter
        search_container_bookID = tk.Frame(filter_container, bg=bg)
        search_container_bookID.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        bookID_label = tk.Label(search_container_bookID, text='Book ID: ', bg=bg)
        bookID_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.bookID_reg = root.register(self.bookID_validate)

        self._detached = set()
        self.bookID_var = tk.StringVar() #create stringvar for entry widget
        self.bookID_var.trace("w", self._columns_searcher) #callback if stringvar is updated

        self.bookID_entry = ttk.Entry(search_container_bookID) #create entry
        self.bookID_entry.config(textvariable=self.bookID_var, validate="key",
                            validatecommand=(self.bookID_reg, "%P"))

        self.bookID_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Title Filter
        search_container_title = tk.Frame(filter_container, bg=bg)
        search_container_title.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        title_label = tk.Label(search_container_title, text='Title: ', bg=bg)
        title_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self._detached = set()
        self.title_var = tk.StringVar() #create stringvar for entry widget
        self.title_var.trace("w", self._columns_searcher) #callback if stringvar is updated

        self.title_entry = ttk.Entry(search_container_title, textvariable=self.title_var) #create entry

        self.title_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Author Filter
        search_author_container = tk.Frame(filter_container, bg=bg)
        search_author_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        author_filter_label = tk.Label(search_author_container, text='Author:', bg=bg)
        author_filter_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.author_var = tk.StringVar()
        self.author_var.trace("w", self._columns_searcher)

        self.author_entry = ttk.Entry(search_author_container, textvariable=self.author_var, font='System 6')
        self.author_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Genre Filter
        search_genre_container = tk.Frame(filter_container, bg=bg)
        search_genre_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        genre_filter_label = tk.Label(search_genre_container, text='Genre:', bg=bg)
        genre_filter_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.genre_var = tk.StringVar()
        self.genre_var.set("-EMPTY-")
        #self.genre_var.trace("w", self._columns_searcher_genre)

        self.genre_menu = ttk.OptionMenu(search_genre_container, self.genre_var,genre_choice_list[0], *genre_choice_list)
        self.genre_menu.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)

        #location Filter
        search_location_container = tk.Frame(filter_container, bg=bg)
        search_location_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        location_filter_label = tk.Label(search_location_container, text='Location:', bg=bg)
        location_filter_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.location_var = tk.StringVar()
        self.location_var.set("-EMPTY-")
        #self.location_var.trace("w", self._columns_searcher_location)

        self.location_menu = ttk.OptionMenu(search_location_container, self.location_var,location_choice_list[0], *location_choice_list)
        self.location_menu.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)




    def notebook_tab_change(self, *args):
        #gather db info to check if book has been issued, so that we only show the books that have NOT been issued.

        #BookIDs
        c.execute("SELECT bookID FROM Books WHERE issued=0")
        non_issued_bookIDs_fetch = c.fetchall()
        non_issued_bookID_list = [x[0] for x in non_issued_bookIDs_fetch]

        c.execute("SELECT title FROM Books WHERE issued=0")
        non_issued_title_fetch = c.fetchall()
        non_issued_title_list = [x[0] for x in non_issued_title_fetch]

        #Authors
        c.execute("SELECT author FROM Books WHERE issued=0")
        non_issued_author_fetch = c.fetchall()
        non_issued_author_list = [x[0] for x in non_issued_author_fetch]

        #Genres
        c.execute("SELECT genre FROM Books WHERE issued=0")
        non_issued_genre_fetch = c.fetchall()
        non_issued_genre_list = [x[0] for x in non_issued_genre_fetch]

        #Locations
        c.execute('SELECT location FROM Books WHERE issued=0')
        non_issued_location_fetch = c.fetchall()
        non_issued_location_list = [x[0] for x in non_issued_location_fetch]


        for k in self.tree.get_children():
            self.tree.delete(k)

        for i in range(len(non_issued_bookID_list)):
            #creates an entry in the tree for each element of the list
            #then stores the id of the tree in the self.ids list
            self.tree_ids.append(self.tree.insert("", "end", values=(non_issued_bookID_list[i], non_issued_title_list[i], non_issued_author_list[i], non_issued_genre_list[i], non_issued_location_list[i])))
        self.tree.pack()

        #Update Genre List for OptionMenu
        # c.execute("SELECT genre FROM Genres")
        # genres_list_fetch = c.fetchall()
        # genre_choice_list = [x[0] for x in genres_list_fetch]

        # genre_menu = self.genre_menu["menu"]
        # genre_menu.delete(0, tk.END)
        # for string in genre_choice_list:
        #     genre_menu.add_command(label=string,
        #                      command=lambda value=string: self.genre_var.set(value))

    def refresh_page(self, *args):
        #BookIDs
        c.execute("SELECT bookID FROM Books WHERE issued=0")
        non_issued_bookIDs_fetch = c.fetchall()
        non_issued_bookID_list = [x[0] for x in non_issued_bookIDs_fetch]

        c.execute("SELECT title FROM Books WHERE issued=0")
        non_issued_title_fetch = c.fetchall()
        non_issued_title_list = [x[0] for x in non_issued_title_fetch]

        #Authors
        c.execute("SELECT author FROM Books WHERE issued=0")
        non_issued_author_fetch = c.fetchall()
        non_issued_author_list = [x[0] for x in non_issued_author_fetch]

        #Genres
        c.execute("SELECT genre FROM Books WHERE issued=0")
        non_issued_genre_fetch = c.fetchall()
        non_issued_genre_list = [x[0] for x in non_issued_genre_fetch]

        #Locations
        c.execute('SELECT location FROM Books WHERE issued=0')
        non_issued_location_fetch = c.fetchall()
        non_issued_location_list = [x[0] for x in non_issued_location_fetch]


        for k in self.tree.get_children():
            self.tree.delete(k)

        for i in range(len(non_issued_bookID_list)):
            #creates an entry in the tree for each element of the list
            #then stores the id of the tree in the self.ids list
            self.tree_ids.append(self.tree.insert("", "end", values=(non_issued_bookID_list[i], non_issued_title_list[i], non_issued_author_list[i], non_issued_genre_list[i], non_issued_location_list[i])))
        self.tree.pack()

    def bookID_validate(self, bookID_input):
        if bookID_input.isdigit():
            return True
        elif bookID_input is "":
            return True
        else:
            return False




    def _columns_searcher(self,*args):
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
                    i_r +=1
                    self.tree.reattach(item_id, '', i_r)
                else:
                    self._detached.add(item_id)
                    self.tree.detach(item_id)

            elif query_author != '':
                if query_author in author_text:
                    i_r +=1
                    self.tree.reattach(item_id, '', i_r)
                else:
                    self._detached.add(item_id)
                    self.tree.detach(item_id)

            elif query_genre != '-EMPTY-':
                if query_genre in genre_text:
                    i_r +=1
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