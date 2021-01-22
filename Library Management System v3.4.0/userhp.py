# User Help

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as ms
import re
import linecache

HEADER_FONT = re.sub('^.*?=', '', linecache.getline('config.txt',11)).strip()
FG = re.sub('^.*?=', '', linecache.getline('config.txt', 13)).strip()
BD = re.sub('^.*?=', '', linecache.getline('config.txt', 14)).strip()
RELIEF = re.sub('^.*?=', '', linecache.getline('config.txt', 15)).strip()


class UserHelp():
    def __init__(self, root, notebook, user_email):
        self.root = root
        self.notebook = notebook

        admin_help_page = tk.Frame(self.notebook, relief=RELIEF, bd=BD)
        notebook.add(admin_help_page, text="User Help Page")

        header_frame = tk.Frame(admin_help_page)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        header = tk.Label(header_frame, text="User Help Page", font=HEADER_FONT)
        header.pack(side=tk.TOP)

        large_frame = tk.Frame(admin_help_page)
        large_frame.pack(fill=tk.BOTH, expand=True)

        _help = tk.Label(large_frame, text="""The library page allows you
to view and filter through all available books in the library.

Use key fields such as Title, Author or Genre to view what kinds of books we 
have in stock.

Additionaly, we display which bookshelf a particular book is on, therefore 
the code that can be filtered and seen on the table matches the code on the 
bookshelf in the physical library.

Account Information
Your Account Details can be accessed in the Accounts tab on the notebook bar 
at the top. There, you are able to change the password of your account or 
optionally delete your account permanently.

The My Books tab is responsible for displaying all your currently issued books.
You can search through it as you would with the Library page described above,
however you can also see the return dates of your books.""", justify=tk.CENTER)
        _help.pack()