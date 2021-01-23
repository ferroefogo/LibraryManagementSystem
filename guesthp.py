#Guest Help

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as ms
import re
import linecache

HEADER_FONT = re.sub('^.*?=', '', linecache.getline('config.txt',11)).strip()
FG = re.sub('^.*?=', '', linecache.getline('config.txt', 13)).strip()
BD = re.sub('^.*?=', '', linecache.getline('config.txt', 14)).strip()
RELIEF = re.sub('^.*?=', '', linecache.getline('config.txt', 15)).strip()


class GuestHelp():
    def __init__(self, root, notebook):
        self.root = root
        self.notebook = notebook

        guest_help_page = tk.Frame(self.notebook, relief=RELIEF, bd=BD)
        notebook.add(guest_help_page, text="Guest Help Page")

        header_frame = tk.Frame(guest_help_page)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        header = tk.Label(header_frame, text="Guest Help Page", font=HEADER_FONT)
        header.pack(side=tk.TOP)

        large_frame = tk.Frame(guest_help_page)
        large_frame.pack(fill=tk.BOTH, expand=True)

        _help = tk.Label(large_frame, text="""The guest login is designed for those who do no want to create an account but
still want to use the system to search for books.The library page allows you
to view and filter through all available books in the library.

Use key fields such as Title, Author or Genre to view what kinds of books we 
have in stock. 

Additionaly, we display which bookshelf a particular book is on, therefore 
the code that can be filtered and seen on the table matches the code on the 
bookshelf in the physical library.""", justify=tk.CENTER)
        _help.pack()