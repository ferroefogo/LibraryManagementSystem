#Options Page

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as ms

width=225
padx=8
pady=5

geometry = '1500x1500'
bg='gray90'
font='System 18'

class Options():
    #USER ACCESS
    #Display program options (Theme, Font, etc...)
    #Optionally do this. Leave for now.
    def __init__(self, root, notebook):
        option_page = tk.Frame(notebook)
        notebook.add(option_page, text='Options')

        options_header = tk.Label(option_page, text='Options', font='System 30')
        options_header.pack(side=tk.TOP)

        #Options Main Container
        options_container = tk.Frame(option_page, bg=bg)
        options_container.pack(side=tk.LEFT, anchor=tk.N, padx=padx)

        #Font Choice
        self.options_container_font = tk.Frame(options_container, bg=bg)
        self.options_container_font.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        font_label = tk.Label(self.options_container_font, text='Choose a Font: ', bg=bg)
        font_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.font_list = ["System", "Helvetica", "Arial", "Times", "Courier", "Palatino", "Garamond", "Bookman", "Avant"]

        self.font_list_var = tk.StringVar()
        self.font_list_var.set(self.font_list[0])
        self.font_list_var.trace("w", self.font_global_change)

        self.font_listbox = ttk.OptionMenu(self.options_container_font, self.font_list_var, *self.font_list)
        self.font_listbox.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)

    def font_global_change(self, *args):
        global global_font
        global_font = self.font_list_var.get()
