#Home Page
import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox as ms

width=225
padx=8
pady=5

geometry = '1500x1500'
bg='gray90'
font='System 18'

class Home():
    #USER ACCESS
    #Describe Software Information.
    def __init__(self, root, notebook):
        home_page = tk.Frame(notebook)
        notebook.add(home_page, text='Home')

        home_header = tk.Label(home_page, text='Welcome to the Library System!', font='System 30')
        home_header.pack(fill=tk.X, expand=True, side=tk.TOP, anchor=tk.N)



        '''
        sidebarframe = tk.Frame(root)
        self.sometext = tk.Text(sidebarframe)
        button= tk.Button(sidebarframe, text="do something",
                          command = self.do_something)

        sidebarframe.pack(row = 3, column = 5)
        self.sometext.pack(row = 3, column = 6)
        button.pack(row = 3, column = 7)

        self.sometext.focus_set()

    def do_something(self):
        self.sometext.delete(1.0, "end")
        print ("do something")
        '''