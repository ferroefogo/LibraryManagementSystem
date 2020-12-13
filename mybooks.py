#MyBooks Page
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

#List of locations
location_choice_list = list(string.ascii_uppercase)
location_alphabet_symbol = location_choice_list.append('*')
location_empty_insert = location_choice_list.insert(0, '-EMPTY-')

class MyBooks():
    #USER ACCESS
    #Display logged in user's books taken out.
    def __init__(self, root, notebook, current_user_email):
        self.user_email = current_user_email
        self.tree_ids = [] 

        my_books_page = tk.Frame(notebook)
        notebook.add(my_books_page, text='My Books')

        header_frame = tk.Frame(my_books_page)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        header = tk.Label(header_frame, text='My Books', font='System 30')
        header.pack(side=tk.TOP)

        current_books_header = ttk.Label(header_frame, text='Current Books', font='System 25')
        current_books_header.pack(side=tk.TOP)

        current_books_frame = tk.Frame(my_books_page)
        current_books_frame.pack(side=tk.TOP, anchor=tk.N)

        # Library TreeView Book Database Frame
        tree_container = tk.Frame(current_books_frame)
        tree_container.pack(side=tk.RIGHT, anchor=tk.N, padx=padx)

        #Set up TreeView table
        self.columns = ('Book ID','Title', 'Author', 'Genre','Location','Issue Date','Return Date')
        self.tree = ttk.Treeview(tree_container, columns=self.columns, show='headings') #create tree
        self.tree.heading("Book ID", text='Book ID')
        self.tree.heading("Title", text='Title')
        self.tree.heading("Author", text='Author')
        self.tree.heading("Genre", text='Genre')
        self.tree.heading("Location", text='Location')
        self.tree.heading("Issue Date", text='Issue Date')
        self.tree.heading("Return Date", text="Return Date")

        self.tree.column("Book ID", width=width, anchor=tk.CENTER)
        self.tree.column("Title", width=width, anchor=tk.CENTER)
        self.tree.column("Author", width=width, anchor=tk.CENTER)
        self.tree.column("Genre", width=width, anchor=tk.CENTER)
        self.tree.column("Location", width=width, anchor=tk.CENTER)
        self.tree.column("Issue Date", width=width, anchor=tk.CENTER)
        self.tree.column("Return Date", width=width, anchor=tk.CENTER)

        #BookIDs
        c.execute("""SELECT Books.bookID
            FROM MyBooks
            INNER JOIN Books
            ON MyBooks.bookID = Books.bookID
            INNER JOIN Accounts
            ON MyBooks.user_id = Accounts.user_id
            WHERE Accounts.user_id = (SELECT user_id FROM Accounts WHERE email_address=?)""",(self.user_email,))
        user_books_bookIDs_fetch = c.fetchall()
        user_book_bookID_list = [x[0] for x in user_books_bookIDs_fetch]


        #Titles
        c.execute("""SELECT Books.title
            FROM MyBooks
            INNER JOIN Books
            ON MyBooks.bookID = Books.bookID
            INNER JOIN Accounts
            ON MyBooks.user_id = Accounts.user_id
            WHERE Accounts.user_id = (SELECT user_id FROM Accounts WHERE email_address=?)""",(self.user_email,))
        user_books_title_fetch = c.fetchall()
        user_book_title_list = [x[0] for x in user_books_title_fetch]


        #Authors
        c.execute("""SELECT Books.author
            FROM MyBooks
            INNER JOIN Books
            ON MyBooks.bookID = Books.bookID
            INNER JOIN Accounts
            ON MyBooks.user_id = Accounts.user_id
            WHERE Accounts.user_id = (SELECT user_id FROM Accounts WHERE email_address=?)""",(self.user_email,))
        user_books_author_fetch = c.fetchall()
        user_book_author_list = [x[0] for x in user_books_author_fetch]


        #Genres
        c.execute("""SELECT Books.genre
            FROM MyBooks
            INNER JOIN Books
            ON MyBooks.bookID = Books.bookID
            INNER JOIN Accounts
            ON MyBooks.user_id = Accounts.user_id
            WHERE Accounts.user_id = (SELECT user_id FROM Accounts WHERE email_address=?)""",(self.user_email,))
        user_books_genre_fetch = c.fetchall()
        user_book_genre_list = [x[0] for x in user_books_genre_fetch]

        #Location
        c.execute("""SELECT Books.location
            FROM MyBooks
            INNER JOIN Books
            ON MyBooks.bookID = Books.bookID
            INNER JOIN Accounts
            ON MyBooks.user_id = Accounts.user_id
            WHERE Accounts.user_id = (SELECT user_id FROM Accounts WHERE email_address=?)""",(self.user_email,))
        user_books_location_fetch = c.fetchall()
        user_book_location_list = [x[0] for x in user_books_location_fetch]


        #Issue Date
        c.execute("""SELECT date_issued
            FROM MyBooks
            WHERE user_id = (SELECT user_id FROM Accounts WHERE email_address=?)""",(self.user_email,))
        user_books_issue_date_fetch = c.fetchall()
        user_book_issue_date_list = [x[0] for x in user_books_issue_date_fetch]


        #Return Date
        c.execute("""SELECT return_date
            FROM MyBooks
            WHERE user_id = (SELECT user_id FROM Accounts WHERE email_address=?)""",(self.user_email,))
        user_books_return_date_fetch = c.fetchall()
        user_book_return_date_list = [x[0] for x in user_books_return_date_fetch]

        for i in range(len(user_book_bookID_list)):
            #creates an entry in the tree for each element of the list
            #then stores the id of the tree in the self.ids list
            self.tree_ids.append(self.tree.insert("", "end", values=(user_book_bookID_list[i], user_book_title_list[i], user_book_author_list[i], user_book_genre_list[i], user_book_location_list[i],user_book_issue_date_list[i], user_book_return_date_list[i])))
        self.tree.pack()

        #Search Books UI
        filter_container = tk.Frame(current_books_frame, bg=bg)
        filter_container.pack(side=tk.LEFT, anchor=tk.N, padx=padx, pady=pady)

        filter_header = tk.Label(filter_container, text='Filters', font='System 18', bg=bg)
        filter_header.pack(anchor=tk.W, padx=padx, pady=pady)


        #BookIDs Filter
        search_container_bookID = tk.Frame(filter_container, bg=bg)
        search_container_bookID.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        bookID_label = tk.Label(search_container_bookID, text='Book ID: ', bg=bg)
        bookID_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.bookID_reg = root.register(self.bookID_validate)

        self._detached = set()
        self.bookID_var = tk.StringVar() #create stringvar for entry widget
        self.bookID_var.trace("w", self._columns_searcher) #callback if stringvar is updated

        self.bookID_entry = ttk.Entry(search_container_bookID)
        self.bookID_entry.config(textvariable=self.bookID_var, validate="key",
                            validatecommand=(self.bookID_reg, "%P"))
        self.bookID_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Titles Filter
        search_container_title = tk.Frame(filter_container, bg=bg)
        search_container_title.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        title_label = tk.Label(search_container_title, text='Title: ', bg=bg)
        title_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.title_var = tk.StringVar() #create stringvar for entry widget
        self.title_var.trace("w", self._columns_searcher) #callback if stringvar is updated

        self.title_entry = ttk.Entry(search_container_title, textvariable=self.title_var)
        self.title_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Author Filter
        search_container_author = tk.Frame(filter_container, bg=bg)
        search_container_author.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        author_label = tk.Label(search_container_author, text='Author: ', bg=bg)
        author_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.author_var = tk.StringVar() #create stringvar for entry widget
        self.author_var.trace("w", self._columns_searcher) #callback if stringvar is updated

        self.author_entry = ttk.Entry(search_container_author, textvariable=self.author_var)
        self.author_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Genre Filter
        search_container_genre = tk.Frame(filter_container, bg=bg)
        search_container_genre.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        genre_label = tk.Label(search_container_genre, text='Genre:', bg=bg)
        genre_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.genre_var = tk.StringVar()
        self.genre_var.set("-EMPTY-")

        from functools import partial
        self.genre_menu = ttk.OptionMenu(search_container_genre, self.genre_var,genre_choice_list[0], *genre_choice_list, command=partial(self._columns_searcher))
        self.genre_menu.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)

        #Location Filter
        search_container_location = tk.Frame(filter_container, bg=bg)
        search_container_location.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        location_label = tk.Label(search_container_location, text='Location:', bg=bg)
        location_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.location_var = tk.StringVar()
        self.location_var.set("-EMPTY-")
        self.location_var.trace("w", self._columns_searcher)

        self.location_menu = ttk.OptionMenu(search_container_location, self.location_var,location_choice_list[0], *location_choice_list)
        self.location_menu.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)



        refresh_container = tk.Frame(filter_container, bg=bg)
        refresh_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        refresh_label = tk.Label(refresh_container, text='Update Page Values: ', bg=bg)
        refresh_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        refresh_button = ttk.Button(refresh_container, text='Refresh', command=self.refresh_page)
        refresh_button.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        for self.col in self.columns:
                    self.tree.heading(self.col, text=self.col,
                                          command=lambda c=self.col: self.sort_upon_press(c))

        root.bind("<F5>", self.refresh_page)


    def refresh_page(self, *args):
        for k in self.tree.get_children():
            self.tree.delete(k)

        #BookIDs
        c.execute("""SELECT Books.bookID
            FROM MyBooks
            INNER JOIN Books
            ON MyBooks.bookID = Books.bookID
            INNER JOIN Accounts
            ON MyBooks.user_id = Accounts.user_id
            WHERE Accounts.user_id = (SELECT user_id FROM Accounts WHERE email_address=?)""",(self.user_email,))
        user_books_bookIDs_fetch = c.fetchall()
        user_book_bookID_list = [x[0] for x in user_books_bookIDs_fetch]


        #Titles
        c.execute("""SELECT Books.title
            FROM MyBooks
            INNER JOIN Books
            ON MyBooks.bookID = Books.bookID
            INNER JOIN Accounts
            ON MyBooks.user_id = Accounts.user_id
            WHERE Accounts.user_id = (SELECT user_id FROM Accounts WHERE email_address=?)""",(self.user_email,))
        user_books_title_fetch = c.fetchall()
        user_book_title_list = [x[0] for x in user_books_title_fetch]


        #Authors
        c.execute("""SELECT Books.author
            FROM MyBooks
            INNER JOIN Books
            ON MyBooks.bookID = Books.bookID
            INNER JOIN Accounts
            ON MyBooks.user_id = Accounts.user_id
            WHERE Accounts.user_id = (SELECT user_id FROM Accounts WHERE email_address=?)""",(self.user_email,))
        user_books_author_fetch = c.fetchall()
        user_book_author_list = [x[0] for x in user_books_author_fetch]


        #Genres
        c.execute("""SELECT Books.genre
            FROM MyBooks
            INNER JOIN Books
            ON MyBooks.bookID = Books.bookID
            INNER JOIN Accounts
            ON MyBooks.user_id = Accounts.user_id
            WHERE Accounts.user_id = (SELECT user_id FROM Accounts WHERE email_address=?)""",(self.user_email,))
        user_books_genre_fetch = c.fetchall()
        user_book_genre_list = [x[0] for x in user_books_genre_fetch]

        #Location
        c.execute("""SELECT Books.location
            FROM MyBooks
            INNER JOIN Books
            ON MyBooks.bookID = Books.bookID
            INNER JOIN Accounts
            ON MyBooks.user_id = Accounts.user_id
            WHERE Accounts.user_id = (SELECT user_id FROM Accounts WHERE email_address=?)""",(self.user_email,))
        user_books_location_fetch = c.fetchall()
        user_book_location_list = [x[0] for x in user_books_location_fetch]

        for i in range(len(user_book_bookID_list)):
            #creates an entry in the tree for each element of the list
            #then stores the id of the tree in the self.ids list
            self.tree_ids.append(self.tree.insert("", "end", values=(user_book_bookID_list[i], user_book_title_list[i], user_book_author_list[i], user_book_genre_list[i], user_book_location_list[i])))
        self.tree.pack()

        #Update Genre List for OptionMenu
        c.execute("SELECT genre FROM Genres")
        genres_list_fetch = c.fetchall()
        genre_choice_list = [x[0] for x in genres_list_fetch]

        genre_menu = self.genre_menu["menu"]
        genre_menu.delete(0, tk.END)
        for string in genre_choice_list:
            genre_menu.add_command(label=string,
                             command=lambda value=string: self.genre_var.set(value))

        #Update location List for OptionMenu
        c.execute("SELECT location FROM Books")
        locations_list_fetch = c.fetchall()
        location_choice_list = [x[0] for x in locations_list_fetch]

        location_menu = self.location_menu["menu"]
        location_menu.delete(0, tk.END)
        for string in location_choice_list:
            location_menu.add_command(label=string,
                             command=lambda value=string: self.location_var.set(value))



        ms.showinfo('Success','You have refreshed the My Books Page!')

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
class AutoCompleteEntryMB():
    def __init__(self, search_container_title, current_user_email, *args, **kwargs):

        self.search_container_title = search_container_title
        self.user_email = current_user_email
        #Titles
        c.execute("""SELECT Books.title
            FROM MyBooks
            INNER JOIN Books
            ON MyBooks.bookID = Books.bookID
            INNER JOIN Accounts
            ON MyBooks.user_id = Accounts.user_id
            WHERE Accounts.user_id = (SELECT user_id FROM Accounts WHERE email_address=?)""",(self.user_email,))
        user_books_title_fetch = c.fetchall()
        user_book_title_list = [x[0] for x in user_books_title_fetch]

        self.lista = user_book_title_list   
        self.var_mb = self.title_entry["textvariable"]
        if self.var_mb == '':
            self.var_mb = self.title_entry["textvariable"] = tk.StringVar()

        self.var_mb.trace('w', self.changed)
        self.title_entry.bind("<Right>", self.selection)
        self.title_entry.bind("<Up>", self.up)
        self.title_entry.bind("<Down>", self.down)
        
        self.lb_up = False

    def changed(self, name, index, mode):
        #Titles
        c.execute("""SELECT Books.title
            FROM MyBooks
            INNER JOIN Books
            ON MyBooks.bookID = Books.bookID
            INNER JOIN Accounts
            ON MyBooks.user_id = Accounts.user_id
            WHERE Accounts.user_id = (SELECT user_id FROM Accounts WHERE email_address=?)""",(self.user_email,))
        user_books_title_fetch = c.fetchall()
        user_book_title_list = [x[0] for x in user_books_title_fetch]

        self.lista = user_book_title_list  

        if self.var_mb.get() == '':
            self.lb.destroy()
            self.lb_up = False
        else:
            words = self.comparison()
            if words:            
                if not self.lb_up:
                    self.lb = tk.Listbox(self.search_container_title)
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)
                    self.lb_up = True
                
                self.lb.delete(0, tk.END)
                for w in words:
                    self.lb.insert(tk.END,w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False
        
    def selection(self, event):

        if self.lb_up:
            self.var_mb.set(self.lb.get(tk.ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.title_entry.icursor(tk.END)

    def up(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':                
                self.lb.selection_clear(first=index)
                index = str(int(index)-1)                
                self.lb.selection_set(first=index)
                self.lb.activate(index) 

    def down(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != tk.tk.END:                        
                self.lb.selection_clear(first=index)
                index = str(int(index)+1)        
                self.lb.selection_set(first=index)
                self.lb.activate(index) 

    def comparison(self):
        pattern = re.compile('.*' + self.var_mb.get() + '.*')
        return [w for w in self.lista if re.match(pattern, w)]