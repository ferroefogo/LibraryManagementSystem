# Admin Page

# Imports
import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox as ms
import bcrypt
from datetime import datetime, timedelta
import re
import linecache
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import random

# File Imports
from email_sys import Email


# Connect to database
with sqlite3.connect('LibrarySystem.db') as db:
    c = db.cursor()

# File Configurations
WIDTH = re.sub('^.*?=', '', linecache.getline('config.txt', 1))
PADX = re.sub('^.*?=', '', linecache.getline('config.txt', 2))
PADY = re.sub('^.*?=', '', linecache.getline('config.txt', 3))
SMALL_GEOMETRY = re.sub('^.*?=', '',linecache.getline('config.txt', 5)).strip()
BG = re.sub('^.*?=', '', linecache.getline('config.txt', 6)).strip()
DANGER_FG = re.sub('^.*?=', '', linecache.getline('config.txt',7)).strip()
MAIN_APP_BG = re.sub('^.*?=', '', linecache.getline('config.txt', 9)).strip()
FONT = re.sub('^.*?=', '', linecache.getline('config.txt', 10)).strip()
HEADER_FONT = re.sub('^.*?=', '', linecache.getline('config.txt', 11)).strip()
VERSION = re.sub('^.*?=', '', linecache.getline('config.txt', 12)).strip()
FG = re.sub('^.*?=', '', linecache.getline('config.txt', 13)).strip()
BD = re.sub('^.*?=', '', linecache.getline('config.txt', 14)).strip()
RELIEF = re.sub('^.*?=', '', linecache.getline('config.txt', 15)).strip()


mode_choice_list = ['-EMPTY-', '0', '1']


class Admin():
    '''
    Access Level: ADMIN ONLY
    Functions: Allows library admin(s) to create accounts of any access level, including admin.
               Display Analytical data for the admin users to read from.
    '''
    def __init__(self, root, notebook, user_email):
        '''
        Used for the initialisation of the visual aspect of the system.
        '''
        # Class variables
        self.root = root
        self.notebook = notebook
        self.user_email = user_email

        admin_page = tk.Frame(self.notebook)
        notebook.add(admin_page, text="Admin")

        # Page Header
        header_frame = tk.Frame(admin_page)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header = tk.Label(header_frame, text="Admin", font=HEADER_FONT)
        header.pack(side=tk.TOP)

        # Will store the tree ID values of each row of the TreeView table.
        self.tree_ids = []
        #  Admin TreeView
        tree_container = tk.Frame(admin_page, bg=BG, relief=RELIEF, bd=BD)
        tree_container.pack(side=tk.BOTTOM, anchor=tk.N, padx=PADX, pady=PADY)

        tree_header = tk.Label(tree_container, text='Database', font=FONT, bg=BG)
        tree_header.pack(padx=PADX, pady=PADY)

        # Set up TreeView table
        self.columns = ('User ID', 'Email Address', 'Staff Mode', 'Admin Mode', 'Issued BookIDs', 'Earliest Return Date')
        self.tree = ttk.Treeview(tree_container, columns=self.columns, show='headings')
        self.tree.heading("User ID", text='User ID')
        self.tree.heading("Email Address", text='Email Address')
        self.tree.heading("Staff Mode", text='Staff Mode')
        self.tree.heading("Admin Mode", text='Admin Mode')
        self.tree.heading("Issued BookIDs", text='Issued BookIDs')
        self.tree.heading("Earliest Return Date", text='Earliest Return Date')

        self.tree.column("User ID", width=50, anchor=tk.CENTER)
        self.tree.column("Email Address", width=WIDTH, anchor=tk.CENTER)
        self.tree.column("Staff Mode", width=80, anchor=tk.CENTER)
        self.tree.column("Admin Mode", width=80, anchor=tk.CENTER)
        self.tree.column("Issued BookIDs", width=WIDTH, anchor=tk.CENTER)
        self.tree.column("Earliest Return Date", width=115, anchor=tk.CENTER)

        # Call the database fetch function to get all the most recent values
        db_fetch = self.database_fetch()

        # Extract return values from database fetch function.
        userID_list = db_fetch[0]
        email_list = db_fetch[1]
        staff_list = db_fetch[2]
        admin_list = db_fetch[3]

        # Delete all rows in the tree to start with a fresh, empty tree that will be populated.
        for k in self.tree.get_children():
            self.tree.delete(k)

        # Iterate over each user in the Accounts table and add their relevant information on the table under a single row.
        for i in range(len(userID_list)):

            # Fetch the bookIDs of all the books under this specific user.
            c.execute("SELECT bookID FROM MyBooks WHERE user_id=?", (userID_list[i],))
            issued_bookIDs_fetch = c.fetchall()
            issued_bookIDs_list = [x[0] for x in issued_bookIDs_fetch]

            # Iterate over each book and present all the books in the table as a string with a comma seperating each book.
            for x in range(len(issued_bookIDs_list)):
                issued_book_list_string = ','.join(map(str, issued_bookIDs_list))

            # Fetch all the return dates under this specific user.
            c.execute("SELECT return_date FROM MyBooks WHERE user_id=?", (userID_list[i],))
            return_date_fetch = c.fetchall()
            return_date_list = [x[0] for x in return_date_fetch]

            # convert the return_date_list from a list of strings to a list of dates
            dates_list = [datetime.strptime(date, '%Y-%m-%d').date() for date in return_date_list]

            try:
                # Try to store the earliest return date this user has.
                earliest_date = str(min(dates_list))
            except ValueError:
                # If the user does not have any return dates tied to their account, display N/A.
                earliest_date = 'N/A'

            # Check if there were any issued books and hence return dates to be placed on the table under this user's row.
            if len(issued_bookIDs_list)==0 or len(return_date_list)==0:
                # If there were no issued books and therefore no return dates under this user's account, display N/A in the corresponding columns to show such.
                self.tree_ids.append(self.tree.insert("", "end", values=(userID_list[i], email_list[i], staff_list[i], admin_list[i], 'N/A', 'N/A')))
            else:
                # If there was issued books and therefore return dates under this user's account, show them on the row this user is in.
                self.tree_ids.append(self.tree.insert("", "end", values=(userID_list[i], email_list[i], staff_list[i], admin_list[i], issued_book_list_string, earliest_date)))

        # Only now we pack the tree onto the page.
        self.tree.pack()

        # Search the Treeview Container
        self.db_search_container = tk.Frame(tree_container)
        self.db_search_container.pack(side=tk.BOTTOM, anchor=tk.N, padx=PADX, pady=PADY)

        # UserID Search DB
        db_search_label_userID = tk.Label(self.db_search_container, text='ID: ', bg=BG)
        db_search_label_userID.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self._detached = set()
        self.db_search_userID_var = tk.StringVar()
        self.db_search_userID_var.trace("w", self._columns_searcher)

        self.db_search_userID_entry = ttk.Entry(self.db_search_container, textvariable=self.db_search_userID_var)
        self.db_search_userID_entry.pack(side=tk.LEFT, anchor=tk.E, padx=PADX, pady=PADY)

        # Email Search DB
        db_search_label_email = tk.Label(self.db_search_container, text='Email: ', bg=BG)
        db_search_label_email.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.db_search_email_var = tk.StringVar()
        self.db_search_email_var.trace("w", self._columns_searcher)

        self.db_search_email_entry = ttk.Entry(self.db_search_container, textvariable=self.db_search_email_var)
        self.db_search_email_entry.pack(side=tk.LEFT, anchor=tk.E, padx=PADX, pady=PADY)

        # Staff Mode Search DB
        db_search_label_staff_mode = tk.Label(self.db_search_container, text='Staff Mode: ', bg=BG)
        db_search_label_staff_mode.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.db_search_staff_mode_var = tk.StringVar()
        self.db_search_staff_mode_var.set("-EMPTY-")

        from functools import partial
        self.db_search_staff_mode_menu = ttk.OptionMenu(self.db_search_container, self.db_search_staff_mode_var, mode_choice_list[0], *mode_choice_list, command=partial(self._columns_searcher))
        self.db_search_staff_mode_menu.pack(side=tk.LEFT, anchor=tk.E, padx=PADX, pady=PADY)

        # Admin Mode Search DB
        db_search_label_admin_mode = tk.Label(self.db_search_container, text='Admin Mode: ', bg=BG)
        db_search_label_admin_mode.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.db_search_admin_mode_var = tk.StringVar()
        self.db_search_admin_mode_var.set("-EMPTY-")

        self.db_search_admin_mode_menu = ttk.OptionMenu(self.db_search_container, self.db_search_admin_mode_var, mode_choice_list[0], *mode_choice_list, command=self._columns_searcher)
        self.db_search_admin_mode_menu.pack(side=tk.LEFT, anchor=tk.E, padx=PADX, pady=PADY)

        # Issued IDs Search DB
        db_search_label_issuedIDs = tk.Label(self.db_search_container, text='Issued IDs: ', bg=BG)
        db_search_label_issuedIDs.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.db_search_issuedIDs_var = tk.StringVar()
        self.db_search_issuedIDs_var.trace("w", self._columns_searcher)

        self.db_search_issuedIDs_entry = ttk.Entry(self.db_search_container, textvariable=self.db_search_issuedIDs_var)
        self.db_search_issuedIDs_entry.pack(side=tk.LEFT, anchor=tk.E, padx=PADX, pady=PADY)

        # For each column in the list of columns, call the function that sorts each column.
        # Each column will be sorted according to its inherent data type. (integers sorted numerically, strings sorted alphabetically)
        # Sort function described in more detail in the function.
        for self.col in self.columns:
                self.tree.heading(self.col, text=self.col,
                                      command=lambda c=self.col: self.sort_upon_press(c))

        # Add Staff Account
        add_account_container = tk.Frame(admin_page, bg=BG, relief=RELIEF, bd=BD)
        add_account_container.pack(side=tk.LEFT, anchor=tk.N, padx=PADX, pady=PADY)

        add_account_header = tk.Label(add_account_container, text='Add Account', font=FONT, bg=BG)
        add_account_header.pack(anchor=tk.W, padx=PADX, pady=PADY)

        # User ID Field
        self.userID_container = tk.Frame(add_account_container, bg=BG)
        self.userID_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        userID_label = tk.Label(self.userID_container, text='User ID: ', bg=BG)
        userID_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.userID_var = tk.StringVar()

        # Fetch the next highest user_id so that a new, fresh and empty field can be guarenteed.
        select_highest_userID = c.execute("SELECT MAX(user_id)+1 FROM Accounts").fetchall()
        highest_userID = [x[0] for x in select_highest_userID][0]

        self.userID_var.set(highest_userID)

        self.userID_entry = ttk.Entry(self.userID_container)
        self.userID_entry.config(textvariable=self.userID_var, state=tk.DISABLED)
        self.userID_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # Email Address Entry Field
        self.email_container = tk.Frame(add_account_container, bg=BG)
        self.email_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        email_label = tk.Label(self.email_container, text='Email Address: ', bg=BG)
        email_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.email_var = tk.StringVar()

        self.email_entry = ttk.Entry(self.email_container, textvariable=self.email_var)
        self.email_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # Password Entry Field
        self.password_container = tk.Frame(add_account_container, bg=BG)
        self.password_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        password_label = tk.Label(self.password_container, text='Password: ', bg=BG)
        password_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.password_var = tk.StringVar()
        self.password_var.trace('w', self.password_strength)

        self.password_entry = ttk.Entry(self.password_container, textvariable=self.password_var, show='*')
        self.password_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # Confirm Password Entry Field
        self.confirm_password_container = tk.Frame(add_account_container, bg=BG)
        self.confirm_password_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        confirm_password_label = tk.Label(self.confirm_password_container, text='Confirm Password: ', bg=BG)
        confirm_password_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.confirm_password_var = tk.StringVar()

        self.confirm_password_entry = ttk.Entry(self.confirm_password_container, textvariable=self.confirm_password_var, show='*')
        self.confirm_password_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # Password Strength measure container
        self.password_strength_master_container = tk.Frame(add_account_container, bg=BG)
        self.password_strength_master_container.pack(expand=True)

        self.password_strength_container_1 = tk.Frame(self.password_strength_master_container, bg=BG)
        self.password_strength_container_1.pack(expand=True)

        self.password_strength_label_1 = tk.Label(self.password_strength_container_1, text='Password must be a minimum of 8 characters.', bg=BG, fg=DANGER_FG)
        self.password_strength_label_1.pack(anchor=tk.E, side=tk.RIGHT, padx=PADX, pady=PADY)

        self.password_strength_container_2 = tk.Frame(self.password_strength_master_container, bg=BG)
        self.password_strength_container_2.pack(expand=True)

        self.password_strength_label_2 = tk.Label(self.password_strength_container_2, text="""Besides letters, include at least a number or symbol)\n([!@#$%^*-_+=|\\\{\}\[\]`¬;:@"'<>,./?]""", bg=BG, fg=DANGER_FG)
        self.password_strength_label_2.pack(anchor=tk.E, side=tk.RIGHT, padx=PADX, pady=PADY)

        # Staff Mode Box
        add_mode_container = tk.Frame(add_account_container, bg=BG)
        add_mode_container.pack(anchor=tk.W, fill=tk.X, side=tk.TOP)

        add_mode_label = tk.Label(add_mode_container, text='Staff Mode: ', bg=BG)
        add_mode_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.add_staff_mode_var = tk.IntVar()

        self.add_staff_mode_checkbtn = ttk.Checkbutton(add_mode_container, variable=self.add_staff_mode_var)
        self.add_staff_mode_checkbtn.pack(side=tk.LEFT, anchor=tk.E, padx=PADX, pady=PADY)

        # Admin Mode Box
        add_admin_mode_label = tk.Label(add_mode_container, text='Admin Mode: ', bg=BG)
        add_admin_mode_label.pack(side=tk.LEFT, anchor=tk.E, padx=PADX, pady=PADY)

        self.add_admin_mode_var = tk.IntVar()

        self.add_admin_mode_checkbtn = ttk.Checkbutton(add_mode_container, variable=self.add_admin_mode_var)
        self.add_admin_mode_checkbtn.pack(side=tk.LEFT, anchor=tk.E, padx=PADX, pady=PADY)

        # Add Account
        add_account_button_container = tk.Frame(add_account_container, bg=BG)
        add_account_button_container.pack(anchor=tk.W, fill=tk.X, expand=True)

        add_account_btn = ttk.Button(add_account_button_container)
        add_account_btn.config(text='    Add Account    ', command=self.add_account)
        add_account_btn.pack(side=tk.RIGHT, anchor=tk.W, padx=PADX, pady=PADY)

        # Show password button
        self.show_password_button = ttk.Button(add_account_button_container, text='Show Password', command=lambda: self.show_password())
        self.show_password_button.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        # Update Existing Account
        # Allows an admin to update the permissions of a staff/user account.
        update_account_header = tk.Label(add_account_container, text='Update Account', font=FONT, bg=BG)
        update_account_header.pack(anchor=tk.W, padx=PADX, pady=PADY)

        # UserID Entry Field
        self.update_account_userID_container = tk.Frame(add_account_container, bg=BG)
        self.update_account_userID_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        update_userID_label = tk.Label(self.update_account_userID_container, text='User ID: ', bg=BG)
        update_userID_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.update_userID_var = tk.StringVar()

        self.update_userID_entry = ttk.Entry(self.update_account_userID_container)
        self.update_userID_entry.config(textvariable=self.update_userID_var)
        self.update_userID_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # Filler frame for the autocomplete function
        self.update_container_canvas = tk.Canvas(self.update_account_userID_container, height=50, width=50, bg=BG)
        self.update_container_canvas.pack(fill=tk.X, expand=True)

        self.update_container_autocomplete = tk.Frame(self.update_container_canvas, bg=BG)
        self.update_container_autocomplete.pack(anchor=tk.W, fill=tk.X, side=tk.TOP)

        # Update staff mode frame
        update_mode_container = tk.Frame(add_account_container, bg=BG)
        update_mode_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        update_staff_mode_label = tk.Label(update_mode_container, text='Staff Mode: ', bg=BG)
        update_staff_mode_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.update_staff_mode_var = tk.IntVar()

        update_staff_mode_checkbtn = ttk.Checkbutton(update_mode_container, variable=self.update_staff_mode_var)
        update_staff_mode_checkbtn.pack(side=tk.LEFT, anchor=tk.E, padx=PADX, pady=PADY)

        # Admin Mode Box
        update_admin_mode_label = tk.Label(update_mode_container, text='Admin Mode: ', bg=BG)
        update_admin_mode_label.pack(side=tk.LEFT, anchor=tk.E, padx=PADX, pady=PADY)

        self.update_admin_mode_var = tk.IntVar()

        update_admin_mode_checkbtn = ttk.Checkbutton(update_mode_container, variable=self.update_admin_mode_var)
        update_admin_mode_checkbtn.pack(side=tk.LEFT, anchor=tk.E, padx=PADX, pady=PADY)

        # Update Account Button
        update_account_button_container = tk.Frame(add_account_container, bg=BG)
        update_account_button_container.pack(anchor=tk.W, fill=tk.X, expand=True)

        update_account_btn = ttk.Button(update_account_button_container)
        update_account_btn.config(text='    Update Account    ', command=self.update_account)
        update_account_btn.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        AutoCompleteEntryAP_UpdateAccountID(self.update_container_autocomplete, self.update_userID_entry, self.update_userID_var, self.update_container_canvas)

        # Remove Account
        remove_account_container = tk.Frame(admin_page, bg=BG, relief=RELIEF, bd=BD)
        remove_account_container.pack(side=tk.LEFT, anchor=tk.N, padx=PADX, pady=PADY)

        remove_account_header = tk.Label(remove_account_container, text='Remove Account', font=FONT, bg=BG)
        remove_account_header.pack(anchor=tk.W, padx=PADX, pady=PADY)

        # User ID Field
        self.remove_userID_container = tk.Frame(remove_account_container, bg=BG)
        self.remove_userID_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        remove_userID_label = tk.Label(self.remove_userID_container, text='User ID: ', bg=BG)
        remove_userID_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.remove_userID_var = tk.StringVar()
        self.remove_userID_var.set('')

        self.remove_userID_entry = ttk.Entry(self.remove_userID_container)
        self.remove_userID_entry.config(textvariable=self.remove_userID_var)
        self.remove_userID_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # Filler frame for the autocomplete function
        self.remove_container_canvas = tk.Canvas(self.remove_userID_container, height=50, width=50, bg=BG)
        self.remove_container_canvas.pack(fill=tk.X, expand=True)

        self.remove_container_autocomplete = tk.Frame(self.remove_container_canvas, bg=BG)
        self.remove_container_autocomplete.pack(anchor=tk.W, fill=tk.X, side=tk.TOP)

        # Remove Account
        remove_account_button_container = tk.Frame(remove_account_container, bg=BG)
        remove_account_button_container.pack(anchor=tk.W, fill=tk.X, expand=True)

        remove_account_btn = ttk.Button(remove_account_button_container)
        remove_account_btn.config(text='    Remove Account    ', command=self.remove_account)
        remove_account_btn.pack(side=tk.RIGHT, anchor=tk.W, padx=PADX, pady=PADY)

        AutoCompleteEntryAP_RemoveAccountID(self.remove_container_autocomplete, self.remove_userID_entry, self.remove_userID_var, self.remove_container_canvas)

        # Send Email Alert
        # Allows an admin to send email alerts to those whose return date is nearby (within 3 days of return).
        alert_container = tk.Frame(admin_page, bg=BG, relief=RELIEF, bd=BD)
        alert_container.pack(side=tk.LEFT, anchor=tk.N, padx=PADX, pady=PADY)

        alert_header = tk.Label(alert_container, text='Returns Reminder Manual Email', font=FONT, bg=BG)
        alert_header.pack(anchor=tk.W, padx=PADX, pady=PADY)

        alert_desc = tk.Label(alert_container, text='Sends an email alert to all users whose book is\n within three days of needing to be returned.', font='System 10', bg=BG)
        alert_desc.pack(anchor=tk.W, padx=PADX, pady=PADY)

        # Send Email Alert Container
        alert_email_button_container = tk.Frame(alert_container, bg=BG)
        alert_email_button_container.pack(anchor=tk.W, fill=tk.X, expand=True)

        alert_btn = ttk.Button(alert_email_button_container)
        alert_btn.config(text='    Alert    ', command=self.send_alert)
        alert_btn.pack(side=tk.RIGHT, anchor=tk.W, padx=PADX, pady=PADY)

        # Analytical Information
        analytics_container = tk.Frame(admin_page, bg=BG, relief=RELIEF, bd=BD)
        analytics_container.pack(side=tk.LEFT, anchor=tk.N, padx=PADX, pady=PADY)

        analytics_header = tk.Label(analytics_container, text='Analytics', font=FONT, bg=BG)
        analytics_header.pack(anchor=tk.W, padx=PADX, pady=PADY, side=tk.TOP)

        # Number of total users
        # Fetch all accounts from the Account table
        fetch_number_users = c.execute("SELECT * FROM Accounts").fetchall()
        number_users = len([x[0] for x in fetch_number_users])

        number_users_frame = tk.Frame(analytics_container)
        number_users_frame.pack(padx=PADX, pady=PADY, side=tk.TOP, anchor=tk.N)

        self.number_users_label = tk.Label(number_users_frame, text='Total of All Users:%d' % number_users)
        self.number_users_label.pack(side=tk.LEFT, anchor=tk.N)

        # Number of total patron accounts
        # Fetch all patron accounts from the Accounts table
        fetch_number_patrons = c.execute("SELECT * FROM Accounts WHERE staff_mode=0 AND admin_mode=0").fetchall()
        number_patrons = len([x[0] for x in fetch_number_patrons])

        number_patrons_frame = tk.Frame(analytics_container)
        number_patrons_frame.pack(padx=PADX, pady=PADY, side=tk.TOP, anchor=tk.N)

        self.number_patrons_label = tk.Label(number_patrons_frame, text='Number of Patrons:%d' % number_patrons)
        self.number_patrons_label.pack(side=tk.LEFT, anchor=tk.N)

        # Number of total staff accounts
        # Fetch all staff accounts from the Accounts table
        fetch_number_staff = c.execute("SELECT * FROM Accounts WHERE staff_mode=1 AND admin_mode=0").fetchall()
        number_staff = len([x[0] for x in fetch_number_staff])

        number_staff_frame = tk.Frame(analytics_container)
        number_staff_frame.pack(padx=PADX, pady=PADY, side=tk.TOP, anchor=tk.N)

        self.number_staff_label = tk.Label(number_staff_frame, text='Number of Staff:%d' % number_staff)
        self.number_staff_label.pack(side=tk.LEFT, anchor=tk.N)

        # Number of total admin accounts
        # Fetch all admin accounts from the Accounts table.
        fetch_number_admins = c.execute("SELECT * FROM Accounts WHERE admin_mode=1").fetchall()
        number_admins = len([x[0] for x in fetch_number_admins])

        number_admins_frame = tk.Frame(analytics_container)
        number_admins_frame.pack(padx=PADX, pady=PADY, side=tk.TOP, anchor=tk.N)

        self.number_admins_label = tk.Label(number_admins_frame, text='Number of Admins:%d' % number_admins)
        self.number_admins_label.pack(side=tk.LEFT, anchor=tk.N)

        # Number of total HYBRID ACCOUNTS accounts
        # Fetch all admin accounts from the Accounts table.
        fetch_number_hybrids = c.execute("SELECT * FROM Accounts WHERE admin_mode=1").fetchall()
        number_hybrids = len([x[0] for x in fetch_number_hybrids])

        number_hybrids_frame = tk.Frame(analytics_container)
        number_hybrids_frame.pack(padx=PADX, pady=PADY, side=tk.TOP, anchor=tk.N)

        self.number_hybrids_label = tk.Label(number_hybrids_frame, text='Number of Hybrids:%d' % number_hybrids)
        self.number_hybrids_label.pack(side=tk.LEFT, anchor=tk.N)

        # Total book tally
        # Fetch all books from the Books table.
        fetch_number_books = c.execute("SELECT * FROM Books").fetchall()
        number_books = len([x[0] for x in fetch_number_books])

        number_books_frame = tk.Frame(analytics_container)
        number_books_frame.pack(padx=PADX, pady=PADY, side=tk.TOP, anchor=tk.N)

        self.number_books_label = tk.Label(number_books_frame, text='Number of Books:%d' % number_books)
        self.number_books_label.pack(side=tk.LEFT, anchor=tk.N)

        # Total issued book tally
        # Fetch all issued books from the Books table.
        fetch_number_issued_books = c.execute("SELECT * FROM Books WHERE issued=1").fetchall()
        number_issued_books = len([x[0] for x in fetch_number_issued_books])

        number_issued_books_frame = tk.Frame(analytics_container)
        number_issued_books_frame.pack(padx=PADX, pady=PADY, side=tk.TOP, anchor=tk.N)

        self.number_issued_books_label = tk.Label(number_issued_books_frame, text='Number of Issued Books:%d' % number_issued_books)
        self.number_issued_books_label.pack(side=tk.LEFT, anchor=tk.N)

        # Total non-issued book tally
        # Fetch all non-issued books from the Books table.
        fetch_number_non_issued_books = c.execute("SELECT * FROM Books WHERE issued=0").fetchall()
        number_non_issued_books = len([x[0] for x in fetch_number_non_issued_books])

        number_non_issued_books_frame = tk.Frame(analytics_container)
        number_non_issued_books_frame.pack(padx=PADX, pady=PADY, side=tk.TOP, anchor=tk.N)

        self.number_non_issued_books_label = tk.Label(number_non_issued_books_frame, text='Number of Non-Issued Books:%d' % number_non_issued_books)
        self.number_non_issued_books_label.pack(side=tk.LEFT, anchor=tk.N)

        # Average number of books issued out on a single day over the past week
        mean_avg_container = tk.Frame(analytics_container)
        mean_avg_container.pack(padx=PADX, pady=PADY, side=tk.TOP, anchor=tk.N)

        self.mean_avg_lbl = tk.Label(mean_avg_container, text='Mean Average of Books Issued\nOver the Last 7 Days\n(NOT Including today):')
        with open("mean_avg_storage.txt", "r") as file:
            lineArray = file.readlines()
        mean_avg = (int(re.findall("\d+", lineArray[6])[0]) + int(re.findall("\d+", lineArray[5])[0]) + int(re.findall("\d+", lineArray[4])[0]) + int(re.findall("\d+", lineArray[3])[0]) + int(re.findall("\d+", lineArray[2])[0]) + int(re.findall("\d+", lineArray[1])[0]) + int(re.findall("\d+", lineArray[0])[0]))/7
        file.close()
        self.mean_avg_lbl["text"] = 'Mean Average of Books Issued\nOver the Last 7 Days\n(NOT Including today): {:.2f}'.format(mean_avg)
        self.mean_avg_lbl.pack(side=tk.LEFT, anchor=tk.N)

        # Button to access genre popularity graph
        genre_popularity_btn = ttk.Button(analytics_container, text='Genre Popularity', command=lambda: self.genre_popularity())
        genre_popularity_btn.pack(side=tk.RIGHT, padx=10, pady=10)

        update_values_btn = ttk.Button(analytics_container, text='Update Values', command=lambda: self.update_values())
        update_values_btn.pack(side=tk.RIGHT, padx=10, pady=10)

        # Bind F5 to updating this page's values.
        notebook.bind("<F5>", self.update_values)

    def genre_popularity(self):
        '''
        Prompt the user with an interactive bar graph regarding the popularity of genres.
        '''

        #  Genre Popularity is based on the number of books currently issued and how many have the specific genre.
        #  x-axis plots the different genres
        #  y-axis plots the number of currently issued books with that genre.

        # Fetch genre of all currently issued books
        issued_genres_fetch = c.execute('SELECT genre FROM Books WHERE issued=1').fetchall()
        issued_genres = [x[0] for x in issued_genres_fetch]

        try:
            # Create dictionary with the keys: genre titles, linked to the values: number of books with that genre title.
            labels, values = zip(*Counter(issued_genres).items())
        except ValueError:
            labels = []
            values = []

        # indexes is the number of bars the graph will have, therefore the number of slices the x axis will need for each bar.
        indexes = np.arange(len(labels))

        width = 0.5

        # Clear any previous plots if the button is pressed many times.
        plt.clf()

        # How each bar will look on the graph.
        # indexes (how many titles along the x axis)
        # values (the value corresponding to that genre)
        # width (the width of the bar)

        plt.bar(indexes, values, width)
        plt.xticks(indexes + width * 0, labels)

        plt.title('Genre Popularity')
        plt.ylabel('Number of Books Currently Issued')
        plt.xlabel('Genres')
        plt.show()

    def update_values(self, *args):
        '''
        Update all values being displayed on the page.
        '''
        week_ago = (datetime.today() - timedelta(days=7)).date()

        # Write the values to a text file to read from and add upon.
        with open("mean_avg_storage.txt", "r") as file:
            lineArray = file.readlines()
        # Iterate over the span of 7 days.
        for j in range(7):

            #  date issued is the date a week ago + the number of days that have been iterated over.
            #  E.g j is on its 2nd loop.
            #  week_ago = 20/12/20
            #  day 20 + 1 = 21
            #  therefore, date_issued will be 21/12/2020

            date_issued = week_ago + timedelta(days=j)

            # Convert date issued to a string in the YYYY-MM-DD format.
            date_issued_string = date_issued.strftime('%Y-%m-%d')

            # Fetch issued books from the date_issued.
            fetch_issued_books_past_week = c.execute("SELECT bookID FROM MyBooks WHERE date_issued=?", (date_issued,))
            issued_books_past_week = [x[0] for x in fetch_issued_books_past_week]

            #  Make sure the books from the current date_issued loop are assigned to the correct variable.
            #  So if the current loop has just fetched all the books from the date 3 days ago, then all those books
            #  will be stored in the number_books_issued_3days_ago variable.
            if date_issued_string == week_ago.strftime("%Y-%m-%d"):
                # len() is used to gauge the number of books that were issued on that particular date.
                # This applies to all the similar variables in this if tree.
                number_books_issued_7days_ago = str(len(issued_books_past_week))
                lineArray[6] = number_books_issued_7days_ago+"\n"

            elif date_issued_string == (week_ago + timedelta(days=1)).strftime("%Y-%m-%d"):
                number_books_issued_6days_ago = str(len(issued_books_past_week))
                lineArray[5] = number_books_issued_6days_ago+"\n"

            elif date_issued_string == (week_ago + timedelta(days=2)).strftime("%Y-%m-%d"):
                number_books_issued_5days_ago = str(len(issued_books_past_week))
                lineArray[4] = number_books_issued_5days_ago+"\n"

            elif date_issued_string == (week_ago + timedelta(days=3)).strftime("%Y-%m-%d"):
                number_books_issued_4days_ago = str(len(issued_books_past_week))
                lineArray[3] = number_books_issued_4days_ago+"\n"

            elif date_issued_string == (week_ago + timedelta(days=4)).strftime("%Y-%m-%d"):
                number_books_issued_3days_ago = str(len(issued_books_past_week))
                lineArray[2] = number_books_issued_3days_ago+"\n"

            elif date_issued_string == (week_ago + timedelta(days=5)).strftime("%Y-%m-%d"):
                number_books_issued_2days_ago = str(len(issued_books_past_week))
                lineArray[1] = number_books_issued_2days_ago+"\n"

            elif date_issued_string == (week_ago + timedelta(days=6)).strftime("%Y-%m-%d"):
                number_books_issued_1days_ago = str(len(issued_books_past_week))
                lineArray[0] = number_books_issued_1days_ago+"\n"

        with open('mean_avg_storage.txt', 'w') as file:
            file.writelines(lineArray)

        # Add up the number of books issued on each individual day for the past 7 days, excluding the current day, and divide it by the 7 days.
        # re.findall(\d+) simply finds any number in the specific line, to avoid attempting to include '\n' in the addition, which causes a type error.
        mean_avg = (int(re.findall("\d+", lineArray[6])[0]) + int(re.findall("\d+", lineArray[5])[0]) + int(re.findall("\d+", lineArray[4])[0]) + int(re.findall("\d+", lineArray[3])[0]) + int(re.findall("\d+", lineArray[2])[0]) + int(re.findall("\d+", lineArray[1])[0]) + int(re.findall("\d+", lineArray[0])[0]))/7
        self.mean_avg_lbl["text"] = 'Mean Average of Books Issued\nOver the Last 7 Days\n(NOT Including today): {:.2f}'.format(mean_avg)
        self.mean_avg_lbl.pack(side=tk.LEFT, anchor=tk.N)

        # Call the database fetch function to get all the most recent values
        db_fetch = self.database_fetch()

        # Extract return values from database fetch function.
        userID_list = db_fetch[0]
        email_list = db_fetch[1]
        staff_list = db_fetch[2]
        admin_list = db_fetch[3]

        # Delete all rows in the tree to start with a fresh, empty tree that will be populated.
        for k in self.tree.get_children():
            self.tree.delete(k)

        # Iterate over each user_id in the Accounts table.
        for i in range(len(userID_list)):
            # Fetch the bookIDs of all the books under this specific user.
            c.execute("SELECT bookID FROM MyBooks WHERE user_id=?", (userID_list[i],))
            issued_bookIDs_fetch = c.fetchall()
            issued_bookIDs_list = [x[0] for x in issued_bookIDs_fetch]

            # Iterate over each book and present all the books in the table as a string with a comma seperating each book.
            for x in range(len(issued_bookIDs_list)):
                issued_book_list_string = ','.join(map(str, issued_bookIDs_list)) 

            # Fetch all the return dates under this specific user.
            c.execute("SELECT return_date FROM MyBooks WHERE user_id=?", (userID_list[i],))
            return_date_fetch = c.fetchall()
            return_date_list = [x[0] for x in return_date_fetch]

            # convert the return_date_list from a list of strings to a list of dates
            dates_list = [datetime.strptime(date, '%Y-%m-%d').date() for date in return_date_list]

            try:
                # Try to store the earliest return date this user has.
                earliest_date = str(min(dates_list))
            except ValueError:
                # If the user does not have any return dates tied to their account, display N/A.
                earliest_date = 'N/A'

            # Check if there were any issued books and hence return dates to be placed on the table under this user's row.
            if len(issued_bookIDs_list)==0 or len(return_date_list)==0:
                # If there were no issued books and therefore no return dates under this user's account, display N/A in the corresponding columns to show such.
                self.tree_ids.append(self.tree.insert("", "end", values=(userID_list[i], email_list[i], staff_list[i], admin_list[i], 'N/A', 'N/A')))
            else:
                # If there was issued books and therefore return dates under this user's account, show them on the row this user is in.
                self.tree_ids.append(self.tree.insert("", "end", values=(userID_list[i], email_list[i], staff_list[i], admin_list[i], issued_book_list_string, earliest_date)))

        # Only now we pack the tree onto the page.
        self.tree.pack()

        # Database fetch for the book information to go on the analytics part will go here.
        # Based on any changes made to the database, the labels will be changed in here too using self.example_label["text"]

        # The Process described below applies to all the analytics beyond this point.
        # Fetch all accounts from the Accounts table.
        fetch_number_users = c.execute("SELECT * FROM Accounts").fetchall()

        # Store the number of users returned from the query above.
        number_users = len([x[0] for x in fetch_number_users])

        # Update the analytic displayed on the page.
        self.number_users_label["text"] = 'Total of All Users:%d' % number_users

        # Number of total patron accounts (not staff or admin)
        fetch_number_patrons = c.execute("SELECT * FROM Accounts WHERE staff_mode=0 AND admin_mode=0").fetchall()
        number_patrons = len([x[0] for x in fetch_number_patrons])
        self.number_patrons_label["text"] = 'Number of Patrons:%d' % number_patrons

        # Number of purely staff accounts.
        fetch_number_staff = c.execute("SELECT * FROM Accounts WHERE staff_mode=1 AND admin_mode=0").fetchall()
        number_staff = len([x[0] for x in fetch_number_staff])
        self.number_staff_label["text"] = 'Number of Staff:%d' % number_staff

        # Number of total admin accounts
        fetch_number_admins = c.execute("SELECT * FROM Accounts WHERE (staff_mode=1 AND admin_mode=1) OR (staff_mode=0 AND admin_mode=1) ").fetchall()
        number_admins = len([x[0] for x in fetch_number_admins])
        self.number_admins_label["text"] = 'Number of Admins:%d' % number_admins

        # Total book tally
        fetch_number_books = c.execute("SELECT * FROM Books").fetchall()
        number_books = len([x[0] for x in fetch_number_books])
        self.number_books_label["text"] = 'Number of Books:%d' % number_books

        # Total issued book tally
        fetch_number_issued_books = c.execute("SELECT * FROM Books WHERE issued=1").fetchall()
        number_issued_books = len([x[0] for x in fetch_number_issued_books])
        self.number_issued_books_label["text"] = 'Number of Issued Books:%d' % number_issued_books

        # Total non-issued book tally
        fetch_number_non_issued_books = c.execute("SELECT * FROM Books WHERE issued=0").fetchall()
        number_non_issued_books = len([x[0] for x in fetch_number_non_issued_books])
        self.number_non_issued_books_label["text"] = 'Number of Non-Issued Books:%d' % number_non_issued_books

    def send_alert(self):
        '''
        Send a global email alert to patrons whose book return dates are nearing.
        '''
        #  Fetch all the accounts that are within 3 days of needing to return their book
        db_return_fetch = c.execute("SELECT user_id, bookID, return_date FROM MyBooks").fetchall()

        NO_BOOKS_REMINDER_FLAG = []
        # The for loop iterates over the user_id, bookID and return_date fetched from the query above.
        for parameter in db_return_fetch:
            date = parameter[2]

            # Convert the return dates returned into datetime objects
            datetime_conversion = datetime.strptime(date, '%Y-%m-%d').date()

            # Fetches the date 3 days within the current date.
            within_three_days = (datetime.today() - timedelta(days=3)).date()

            if within_three_days <= datetime_conversion:
                # If we're within three days of the return

                # Identify the bookID behind the return date
                target_bookID = parameter[1]
                target_userID = parameter[0]

                # Fetch all of that books information.
                db_title_fetch = c.execute("SELECT title FROM Books WHERE bookID=?", (target_bookID,)).fetchall()
                db_title = [x[0] for x in db_title_fetch][0]

                db_author_fetch = c.execute("SELECT author FROM Books WHERE bookID=?", (target_bookID,)).fetchall()
                db_author = [x[0] for x in db_author_fetch][0]

                db_genre_fetch = c.execute("SELECT genre FROM Books WHERE bookID=?", (target_bookID,)).fetchall()
                db_genre = [x[0] for x in db_genre_fetch][0]

                db_issue_date_fetch = c.execute("SELECT date_issued FROM MyBooks WHERE bookID=?", (target_bookID,)).fetchall()
                db_issue_date = [x[0] for x in db_issue_date_fetch][0]

                db_expected_return_date_fetch = c.execute("SELECT return_date FROM MyBooks WHERE bookID=?", (target_bookID,)).fetchall()
                db_expected_return_date = [x[0] for x in db_expected_return_date_fetch][0]

                db_target_email_address = c.execute("SELECT email_address FROM Accounts WHERE user_id=?", (target_userID,)).fetchall()
                db_target_email_address = [x[0] for x in db_target_email_address][0]

                # Instantiate email class in the email_sys file.
                e = Email()
                # Establish the API service connection
                service = e.get_service()
                # Create the to, from and message along with passing the required variables to the email template that need to be shown to the user in the email.
                message = e.create_reminder_message("from@gmail.com", db_target_email_address, "Books4All Return Reminder", db_title, db_author, db_genre, db_issue_date, db_expected_return_date)
                # Send the email.
                e.send_message(service, "from@gmail.com", message)
                NO_BOOKS_REMINDER_FLAG.append(True)
            else:
                # Append a False to the NO_BOOKS_REMINDER_FLAG to say that the account checked on that for loop iteration does not need an email sent.
                NO_BOOKS_REMINDER_FLAG.append(False)

        if not any(NO_BOOKS_REMINDER_FLAG):
            # Return date is not within allocated time to be emailed.
            ms.showwarning('Warning', 'No books within reminder limit!')
        else:
            ms.showinfo('Success', 'Emails to the target addresses have been sent!')

    def add_account(self):
        '''
        Add an account onto the system, regardless of access level.
        '''

        # Password Regex check chars
        special_characters_regex = re.compile("""[!@#$%^*-_+=|\\\{\}\[\]`¬;:@"'<>,./?]()""")

        # Get all required variables from entry fields.
        add_email = self.email_var.get()

        # Broad regex to avoid invalid addresses
        email_regex = '^\S+@\S+$'
        if (re.search(email_regex, add_email)):

            add_password = self.password_var.get()
            add_confirm_password = self.confirm_password_var.get()

            if add_password != add_confirm_password:
                ms.showwarning('Warning','Your passwords do not match.')
            elif add_password == '' or add_confirm_password == '':
                ms.showwarning('Warning', 'You left the password fields empty!')
            elif len(add_password) >= 8:
                if special_characters_regex.search(add_password) != None:
                    # Encrypt+Salt PWs
                    hashable_pw = bytes(add_password, 'utf-8')
                    hashed_pw = bcrypt.hashpw(hashable_pw, bcrypt.gensalt())

                    # Convert into base64string
                    self.db_hashed_pw = hashed_pw.decode("utf-8")

                    # Send password to DB
                    find_user = ('SELECT * FROM Accounts WHERE email_address = ?')
                    c.execute(find_user, [(add_email)])

                    if c.fetchall():
                        ms.showerror('Error!', 'Email is already registered to an Account.')
                    else:
                        # 1. TopLevel window and layout.
                        self.accountVerification = tk.Toplevel()

                        # configurations
                        self.accountVerification.title("Account Verification")
                        self.accountVerification.option_add('*Font', 'System 12')
                        self.accountVerification.option_add('*Label.Font', 'System 12')
                        self.accountVerification.geometry(SMALL_GEOMETRY)
                        self.accountVerification.resizable(False, False)

                        main_frame = tk.Frame(self.accountVerification, relief=tk.FLAT)
                        main_frame.pack(fill=tk.BOTH, side=tk.TOP)

                        main_label = tk.Label(main_frame, text='Library System v'+VERSION)
                        main_label.pack(fill=tk.X, anchor=tk.N)

                        header_frame = tk.Frame(self.accountVerification)
                        header_frame.pack(fill=tk.X, side=tk.TOP)

                        header = tk.Label(header_frame, text='Account Verification', font=HEADER_FONT)
                        header.pack(side=tk.TOP)

                        header_description = tk.Label(header_frame, text='A 6 digit verification code has been sent to\n'+add_email+'\n Please enter the 6 digit code into the entry field below.', font='System 8')
                        header_description.pack(side=tk.TOP)

                        self.timer = tk.Label(header_frame, text='')
                        self.timer.pack(side=tk.TOP)

                        # Establish timer to avoid spamming inbox.
                        self.time_remaining = 0
                        self.countdown(60)

                        # Codes Full Container
                        code_container = tk.Frame(self.accountVerification, bg=BG)
                        code_container.pack(padx=PADX, pady=PADY)

                        # Code Entry Field Container
                        verification_code_container = tk.Frame(code_container, bg=BG)
                        verification_code_container.pack(expand=True)

                        verification_code_label = tk.Label(verification_code_container, text='    Verification Code:   ', bg=BG)
                        verification_code_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

                        self.verification_code_reg = self.root.register(self.verification_code_validate)

                        self.verification_code_var = tk.StringVar()
                        self.verification_code_var.set('')
                        self.verification_code_entry = ttk.Entry(verification_code_container, textvariable=self.verification_code_var,
                                                                font='System 6', validate="key",
                                                                validatecommand=(self.verification_code_reg, "%P"))
                        self.verification_code_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

                        # Buttons Container
                        button_container = tk.Frame(code_container, bg=BG)
                        button_container.pack(expand=True)

                        check_code_button = ttk.Button(button_container, text='Check Verification Code', command=lambda: self.check_code(self.verification_code_var.get()))
                        resend_code_button = ttk.Button(button_container, text='Resend Verification Code', command=lambda: self.resend_code(self.verification_code_var.get()))

                        check_code_button.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)
                        resend_code_button.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

                        self.verification_code_entry.bind("<Return>", self.check_code)

                        # 2.1. Randomly generate a 6 digit code to be sent by email
                        self.email_verification_code = ''
                        i = 0
                        while i < 6:
                            # random.SystemRandom() is used because it is cryptographically secure, due to its use of entropy - that is unpredictable from a source that cannot be observed.
                            random_integer = random.SystemRandom().randint(0, 9)
                            i += 1
                            self.email_verification_code += str(random_integer)

                        # 2.2. Send Email to user with the verification code.
                        # Call the Email class
                        e = Email()
                        service = e.get_service()
                        message = e.create_verification_message("from@gmail.com", add_email, "Books4All Re", self.email_verification_code)
                        e.send_message(service, "from@gmail.com", message)
                else:
                    ms.showerror('Error', 'The password entered does not have any special characters.')
            else:
                ms.showerror('Error', 'The password entered does not have at least 8 characters.')
        else:
            ms.showerror('Error', 'Invalid Email Address')

    def check_code(self, *args):
        '''
        Check that the code entered into the verification entry field matches the code that was send to the user via email.
        '''
        # 3. Compare the email code with the input code
        if self.verification_code_var.get() != self.email_verification_code:
            ms.showerror('Error','The verification code does not match the code sent.')
        else:
            ms.showinfo('Success','The verification code matches the code we sent!')
            self.accountVerification.destroy()

            # Fetch the next highest user_id in the table that is empty.
            select_highest_val = c.execute('SELECT MAX(user_id) + 1 FROM Accounts').fetchall()
            highest_val = [x[0] for x in select_highest_val][0]

            insert = 'INSERT INTO Accounts(email_address,password,user_id,staff_mode,admin_mode) VALUES(?,?,?,?,?)'
            c.execute(insert,[(self.email_var.get()),(self.db_hashed_pw),(highest_val),(self.add_staff_mode_var.get()),(self.add_admin_mode_var.get())])
            db.commit()

            # Update the next highest userID after this user has added their account.
            select_highest_val = c.execute('SELECT MAX(user_id) + 1 FROM Accounts').fetchall()
            highest_val = [x[0] for x in select_highest_val][0]
            self.userID_var.set(highest_val)

            # Call the database fetch function to get all the most recent values
            db_fetch = self.database_fetch()

            # Extract return values from database fetch function.
            userID_list = db_fetch[0]
            email_list = db_fetch[1]
            staff_list = db_fetch[2]
            admin_list = db_fetch[3]

            # Delete all rows to clear the table.
            for k in self.tree.get_children():
                self.tree.delete(k)

            # Iterate over each user_id in the Accounts table.
            for i in range(len(userID_list)):
                # issued_bookIDs
                c.execute("SELECT bookID FROM MyBooks WHERE user_id=?", (userID_list[i],))
                issued_bookIDs_fetch = c.fetchall()
                issued_bookIDs_list = [x[0] for x in issued_bookIDs_fetch]

                for x in range(len(issued_bookIDs_list)):
                    issued_book_list_string = ','.join(map(str, issued_bookIDs_list))

                # earliest return date
                c.execute("SELECT return_date FROM MyBooks WHERE user_id=?", (userID_list[i],))
                return_date_fetch = c.fetchall()
                return_date_list = [x[0] for x in return_date_fetch]

                # convert the return_date_list from a list of strins to a list of dates
                dates_list = [datetime.strptime(date, '%Y-%m-%d').date() for date in return_date_list]

                try:
                    # Store the earliest return date in the date list
                    earliest_date = str(min(dates_list))
                except ValueError:
                    # If no dates are in the list, display the earliest date as N/A
                    earliest_date = 'N/A'

                # Check if the issued_books and return date lists are empty
                if len(issued_bookIDs_list) == 0 or len(return_date_list) == 0:
                    # If there were no issued books and therefore no return dates under this user's account, display N/A in the corresponding columns to show such.
                    self.tree_ids.append(self.tree.insert("", "end", values=(userID_list[i], email_list[i], staff_list[i], admin_list[i], 'N/A', 'N/A')))
                else:
                    # If there was issued books and therefore return dates under this user's account, show them on the row this user is in.
                    self.tree_ids.append(self.tree.insert("", "end", values=(userID_list[i], email_list[i], staff_list[i], admin_list[i], issued_book_list_string, earliest_date)))
            self.tree.pack()

            self.email_var.set('')
            self.password_var.set('')
            self.confirm_password_var.set('')
            self.add_staff_mode_var.set(0)
            self.add_staff_mode_var.set(0)

            ms.showinfo('Success!', 'Account Created!')

    def resend_code(self, *args):
        '''
        Resend the code upon user button prompt to do so.
        '''
        # When the timer counts to 0, it updates the label to show that it is ready.
        if self.timer["text"] == "Ready to Resend Code!":
            # If this condition is met, another code will be generated and sent to the target address.
            self.email_verification_code = ''
            i = 0
            while i < 6:
                # Generate 6 digit code.
                random_integer = random.SystemRandom().randint(0,9)
                i += 1
                self.email_verification_code += str(random_integer)

            # 2.2. Send Email to user with the verification code.
            # Call the Email class
            e = Email()
            service = e.get_service()
            message = e.create_verification_message("from@gmail.com", self.email_var.get(), "Books4All Verification Code", self.email_verification_code)
            e.send_message(service, "from@gmail.com", message)

            # Reset the timer.
            self.time_remaining = 0
            self.countdown(60)
        else:
            # Tell the user that the timer has not ran down to 0.
            ms.showwarning('Warning', 'Please wait another '+self.timer["text"]+' seconds to resend a code.')

    def countdown(self, time_remaining=None):
        '''
        Counts the timer down and updates the timer label accordingly.
        '''
        if time_remaining is not None:
            # Condition is met only when the timer has started.
            self.time_remaining = time_remaining

        if self.time_remaining <= 0:
            # Timer has counted to 0.
            self.timer["text"] = "Ready to Resend Code!"
        else:
            # Timer is still counting down.
            self.timer["text"] = ("%d" % self.time_remaining)

            # Subtract 1 from the current time.
            self.time_remaining = self.time_remaining - 1

            # Wait 1000ms (equal to 1 second).
            self.accountVerification.after(1000, self.countdown)

    def verification_code_validate(self, verification_code_inp):
        '''
        Validate the verification code entry field.
        '''

        # Is the input a digit?
        if verification_code_inp.isdigit():
            # Is the input more than 6 digits long?
            if len(verification_code_inp) > 6:
                return False
            else:
                return True
        # Is the entry field empty?
        elif verification_code_inp == "":
            return True
        else:
            return False

    def update_account(self):
        '''
        Update an account's access level.
        '''

        # Get relevant input fields.
        try:
            user_id = self.update_userID_var.get()

            # Check if userID exists.
            check_account_existance = c.execute("SELECT user_id FROM Accounts WHERE user_id=?", (user_id,)).fetchall()
            if len(check_account_existance) == 0:
                ms.showerror('Error', 'Invalid User ID.')
            else:
                # Return user userid given the email address.
                check_current_user = c.execute("SELECT user_id FROM Accounts WHERE email_address=?", (self.user_email,)).fetchall()[0][0]
                if user_id != check_current_user:
                    # Returns the access level of the user at a given userid
                    check_admin = c.execute("SELECT admin_mode FROM Accounts WHERE user_id=?", (user_id,)).fetchall()[0][0]
                    if check_admin == 1:
                        ms.showerror('Error', 'You cannot update the account of another admin account.')
                    else:
                        update = 'UPDATE Accounts SET staff_mode=?, admin_mode=? WHERE user_id=?'
                        c.execute(update, [(self.update_staff_mode_var.get()), (self.update_admin_mode_var.get()), (user_id)])
                        db.commit()

                        find_email_tied_to_user = c.execute("SELECT email_address FROM Accounts WHERE user_id=?", (user_id,)).fetchall()
                        user_email = [x[0] for x in find_email_tied_to_user][0]

                        # Call the email class from the email_sys file.
                        e = Email()
                        # Establish the Google API connection.
                        service = e.get_service()
                        # Create the message along with passing any additional information that must go on the message.
                        message = e.create_admin_update_acc_message("from@gmail.com", user_email,"Books4All Account Permissions Update", self.update_staff_mode_var.get(), self.update_admin_mode_var.get())
                        # Send the message.
                        e.send_message(service, "from@gmail.com", message)

                        ms.showinfo('Success', 'Account Updated!\nAn email has been sent to\n'+user_email+'\nwith the details of this action.')
                        ms.showinfo('Changes', 'To see the changes to the account, the account must relog, if currently logged in.')
                else:
                    ms.showerror('Error', 'You cannot change your own account privileges')

            # Call the database fetch function to get all the most recent values
            db_fetch = self.database_fetch()

            # Extract return values from database fetch function.
            userID_list = db_fetch[0]
            email_list = db_fetch[1]
            staff_list = db_fetch[2]
            admin_list = db_fetch[3]

            for k in self.tree.get_children():
                self.tree.delete(k)

            for i in range(len(userID_list)):
                # issued_bookIDs
                c.execute("SELECT bookID FROM MyBooks WHERE user_id=?", (userID_list[i],))
                issued_bookIDs_fetch = c.fetchall()
                issued_bookIDs_list = [x[0] for x in issued_bookIDs_fetch]

                for x in range(len(issued_bookIDs_list)):
                    issued_book_list_string = ','.join(map(str, issued_bookIDs_list))

                # earliest return date
                c.execute("SELECT return_date FROM MyBooks WHERE user_id=?", (userID_list[i],))
                return_date_fetch = c.fetchall()
                return_date_list = [x[0] for x in return_date_fetch]

                # convert the return_date_list from a list of strins to a list of dates
                dates_list = [datetime.strptime(date, '%Y-%m-%d').date() for date in return_date_list]

                try:
                    earliest_date = str(min(dates_list))
                except ValueError:
                    earliest_date = 'N/A'

                if len(issued_bookIDs_list) == 0 or len(return_date_list) == 0:
                    self.tree_ids.append(self.tree.insert("", "end", values=(userID_list[i], email_list[i], staff_list[i], admin_list[i], 'N/A', 'N/A')))
                else:
                    self.tree_ids.append(self.tree.insert("", "end", values=(userID_list[i], email_list[i], staff_list[i], admin_list[i], issued_book_list_string, earliest_date)))
                self.tree.pack()
        except Exception:
            ms.showerror('Error', 'Invalid Input')

    def remove_account(self):
        '''
        Remove an account from the system.
        '''
        # The same structural premise as the update_account function

        # Get relevant values.
        try:
            user_id = int(self.remove_userID_var.get())
            # Find all user_ids to check if the admin is attempting to remove the last account from the system.
            all_accounts_fetch = c.execute("SELECT user_id FROM Accounts").fetchall()
            all_accounts = [x[0] for x in all_accounts_fetch]
            if len(all_accounts) == 1:
                ms.showerror("Error", "Do not remove any more accounts\nto keep the system stable and ensure optimal performance.")
            else:
                # Check if the user_id is an integer.
                if isinstance(user_id, int) is True:
                    # Check if userID exists.
                    check_account_existance = c.execute("SELECT user_id FROM Accounts WHERE user_id=?", (user_id,)).fetchall()
                    if len(check_account_existance) == 0:
                        ms.showerror('Error', 'Invalid User ID.')
                    else:
                        # Return user userid given the email address.
                        check_current_user = c.execute("SELECT user_id FROM Accounts WHERE email_address=?", (self.user_email,)).fetchall()[0][0]
                        if user_id != check_current_user:
                            # Returns the access level of the user at a given userid
                            check_admin = c.execute("SELECT admin_mode FROM Accounts WHERE user_id=?", (user_id,)).fetchall()[0][0]
                            if check_admin == 1:
                                ms.showerror('Error', 'You cannot update the account of another admin account.')
                            else:
                                # Unlink any books connected to this account and make them available.
                                # Must also delete the user from the MyBooks table.

                                db_check_linked_books_fetch = c.execute('SELECT bookID FROM MyBooks WHERE user_id=?', (user_id,)).fetchall()
                                db_check_linked_books = [x[0] for x in db_check_linked_books_fetch]
                                if len(db_check_linked_books) != 0:
                                    # Must unlink the books and delete the MyBooks user_id entry.
                                    for i in range(len(db_check_linked_books)):
                                        c.execute('UPDATE Books SET issued=0 WHERE bookID=?', (db_check_linked_books[i],))

                                    # Delete MyBooks row of this user.
                                    c.execute('DELETE FROM MyBooks WHERE user_id=?', (user_id,))
                                    db.commit()

                                find_email_tied_to_user = c.execute("SELECT email_address FROM Accounts WHERE user_id=?", (user_id,)).fetchall()
                                user_email = [x[0] for x in find_email_tied_to_user][0]

                                # Call the email class from the email_sys file.
                                e = Email()

                                # Establish the Google API connection.
                                service = e.get_service()

                                # Create the message along with passing any additional information that must go on the message.
                                message = e.create_admin_acc_removal_message("from@gmail.com", user_email,"Books4All Account Removal")

                                # Send the message.
                                e.send_message(service, "from@gmail.com", message)

                                # Delete the entire row where the user_id matches the user_id entered by the admin.
                                c.execute('DELETE FROM Accounts WHERE user_id=?', (user_id,))
                                db.commit()

                                ms.showinfo('Success', 'Account Removed\nAn email has been sent to\n'+user_email+'\nwith the details of this action.')
                                ms.showinfo('Changes', 'To see the changes to the account, the account must relog, if currently logged in.')

                                # Clear the entry fields.
                                self.remove_userID_var.set('')
                                # Fetch the next highest user_id in the table that is empty.
                                select_highest_val = c.execute('SELECT MAX(user_id) + 1 FROM Accounts').fetchall()
                                highest_val = [x[0] for x in select_highest_val][0]
                                self.userID_var.set(highest_val)
                else:
                    ms.showerror('Error', 'Invalid User ID')

            # Call the database fetch function to get all the most recent values
            db_fetch = self.database_fetch()

            # Extract return values from database fetch function.
            userID_list = db_fetch[0]
            email_list = db_fetch[1]
            staff_list = db_fetch[2]
            admin_list = db_fetch[3]

            for k in self.tree.get_children():
                self.tree.delete(k)

            for i in range(len(userID_list)):
                # issued_bookIDs
                c.execute("SELECT bookID FROM MyBooks WHERE user_id=?", (userID_list[i],))
                issued_bookIDs_fetch = c.fetchall()
                issued_bookIDs_list = [x[0] for x in issued_bookIDs_fetch]

                for x in range(len(issued_bookIDs_list)):
                    issued_book_list_string = ','.join(map(str, issued_bookIDs_list))

                # earliest return date
                c.execute("SELECT return_date FROM MyBooks WHERE user_id=?", (userID_list[i],))
                return_date_fetch = c.fetchall()
                return_date_list = [x[0] for x in return_date_fetch]

                # convert the return_date_list from a list of strins to a list of dates
                dates_list = [datetime.strptime(date, '%Y-%m-%d').date() for date in return_date_list]

                try:
                    earliest_date = str(min(dates_list))
                except ValueError:
                    earliest_date = 'N/A'

                if len(issued_bookIDs_list) == 0 or len(return_date_list) == 0:
                    self.tree_ids.append(self.tree.insert("", "end", values=(userID_list[i], email_list[i], staff_list[i], admin_list[i], 'N/A', 'N/A')))
                else:
                    self.tree_ids.append(self.tree.insert("", "end", values=(userID_list[i], email_list[i], staff_list[i], admin_list[i], issued_book_list_string, earliest_date)))
                self.tree.pack()
        except Exception:
            ms.showerror('Error', 'Invalid user ID')

    def show_password(self, *args):
        '''
        Allow the user toggle between showing their password
        in plaintext and hidden behind asterisks.
        '''
        if self.password_entry["show"] == "*":
            self.password_entry["show"] = ''
            self.confirm_password_entry["show"] = ''
        else:
            self.password_entry["show"] = '*'
            self.confirm_password_entry["show"] = '*'

    def password_strength(self, *args):
        '''
        Evaluate the strength of the password
        based on length and characters used.
        '''

        # A regex with a docstring of all of the valid characters
        # that can be used in the password.
        special_characters_regex = re.compile("""[!@#$%^*-_+=|\\\{\}\[\]`¬;:@"'<>,./?]()""")
        password_input = self.password_var.get()

        # Check if the password is longer than the 8 character minimum.
        if len(password_input) >= 8:

            # Hide the label describing the password strength requirements
            # to show that the password meets that requirement.
            self.password_strength_container_1.pack_forget()
            if special_characters_regex.search(password_input) != None:
                self.password_strength_container_2.pack_forget()
            else:
                self.password_strength_container_2.pack(expand=True)

        elif len(password_input) < 8:
            # Show the label describing the password strength requirements
            # to show that the password does not meet that requirement.
            self.password_strength_container_1.pack(expand=True)
            if special_characters_regex.search(password_input) != None:
                self.password_strength_container_2.pack_forget()
            else:
                self.password_strength_container_2.pack(expand=True)

    def database_fetch(self):
        '''
        Fetches the most commonly required values from the database
        that are mostly used when the table has to be updated.
        '''

        # User IDs
        c.execute("SELECT user_id FROM Accounts")
        userIDs_fetch = c.fetchall()
        userID_list = [x[0] for x in userIDs_fetch]

        # Email addresses
        c.execute("SELECT email_address FROM Accounts")
        email_fetch = c.fetchall()
        email_list = [x[0] for x in email_fetch]

        # staff mode
        c.execute("SELECT staff_mode FROM Accounts")
        staff_fetch = c.fetchall()
        staff_list = [x[0] for x in staff_fetch]

        # admin mode
        c.execute("SELECT admin_mode FROM Accounts")
        admin_fetch = c.fetchall()
        admin_list = [x[0] for x in admin_fetch]

        return (userID_list, email_list, staff_list, admin_list)

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
        query_userID = str(self.db_search_userID_var.get())
        query_email = str(self.db_search_email_var.get())
        query_staff = str(self.db_search_staff_mode_var.get())
        query_admin = str(self.db_search_admin_mode_var.get())
        query_issuedIDs = str(self.db_search_issuedIDs_var.get())

        # Call the function that will re-order the tree according to the search parameters entered by the user.
        self.search_tv(children, query_userID, query_email, query_staff, query_admin, query_issuedIDs)

    def search_tv(self, children, query_userID, query_email, query_staff, query_admin, query_issuedIDs):
        '''
        Returns a tree that is ordered according to the search parameters entered by the user.
        '''

        # Iterable variable that will iterate from row 0 on the tree.
        i_r = -1

        # Iterate over each item_id (which is the row id) in the whole tree, both the hidden and currently displayed rows.
        for item_id in children:
            # Get the string values of each column value of the current row.
            userID_text = str(self.tree.item(item_id)['values'][0])
            email_text = str(self.tree.item(item_id)['values'][1])
            staff_text = str(self.tree.item(item_id)['values'][2])
            admin_text = str(self.tree.item(item_id)['values'][3])
            issuedIDs_text = str(self.tree.item(item_id)['values'][4])

            # If the current search parameter is empty, the tree will display all the rows on the table.
            # E.g. If all the search fields are empty, meaning nothing has been searched for, then the table will display all the values as a default.
            if query_userID != '':
                if query_userID in userID_text:
                    # If any of the characters in the user search query are in the column string value (in this case the userID_text string value);
                    # The iterable will increase to find the next row (if this is the start of the search, then the iterable will increment to 0, which is the top row of the table.)
                    i_r += 1
                    # The tree will reattach the correct row (item_id) onto the top of the table, as well as any other searches which contain the same characters so far.
                    # E.g. searching userID=1 in a database with userIDs= 1, 11, 133. This will prompt the table to show all those rows on the table, because they all begin with the 1
                    # that the user searched for.
                    # This process repeats for the rest of the function.
                    self.tree.reattach(item_id, '', i_r)
                else:
                    self._detached.add(item_id)
                    self.tree.detach(item_id)

            elif query_email != '':
                if query_email in email_text:
                    i_r += 1
                    self.tree.reattach(item_id, '', i_r)
                else:
                    self._detached.add(item_id)
                    self.tree.detach(item_id)

            elif query_staff != '-EMPTY-':
                if query_staff in staff_text:
                    i_r += 1
                    self.tree.reattach(item_id, '', i_r)
                else:
                    self._detached.add(item_id)
                    self.tree.detach(item_id)

            elif query_admin != '-EMPTY-':
                if query_admin in admin_text:
                    i_r += 1
                    self.tree.reattach(item_id, '', i_r)
                else:
                    self._detached.add(item_id)
                    self.tree.detach(item_id)

            elif query_issuedIDs != '':
                if query_issuedIDs in issuedIDs_text:
                    i_r += 1
                    self.tree.reattach(item_id, '', i_r)
                else:
                    self._detached.add(item_id)
                    self.tree.detach(item_id)
            else:
                # If all the fields are empty or in their default state, display the default table.
                self.tree.reattach(item_id, '', i_r)

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
        tv.heading(col, command=lambda: self.quickSort(tv, col, arr, low, high, not reverse))

        if reverse is True:
            # To save time and avoid having to sort the list again when it has already been sorted,
            # when the reverse sort is triggered, the array simply inverts itself, rather than go
            # through the whole partitioning sort process again.
            arr_reverse = arr[::-1]
            # The tree is re-ordered as this function is described above.
            for index, (val, k) in enumerate(arr_reverse):
                tv.move(k, '', index)


class AutoCompleteEntryAP_UpdateAccountID(ttk.Entry):
    '''
    Autocomplete function to display all the possible values that could go into the field, based on what is currently being typed into the entry field.

    Structuraly the same as all the other Autocomplete classes, however this applies to the updating process of accounts.
    Already described above.
    '''
    def __init__(self, update_container_autocomplete, update_userID_entry, update_userID_var, update_container_canvas, *args, **kwargs):

        self.update_container_autocomplete = update_container_autocomplete
        self.update_container_canvas = update_container_canvas

        #  Listbox length
        if 'listboxLength' in kwargs:
            self.listboxLength = kwargs['listboxLength']
            del kwargs['listboxLength']
        else:
            self.listboxLength = 8

        ttk.Entry.__init__(self, *args, **kwargs)
        self.focus()

        # User IDs
        c.execute("SELECT user_id FROM Accounts")
        update_userID_fetch = c.fetchall()
        update_userID_list = [x[0] for x in update_userID_fetch]

        self.lista = update_userID_list

        self.update_userID_var = update_userID_var

        self.update_userID_entry = self["textvariable"]
        if self.update_userID_entry == '':
            self.update_userID_entry = self["textvariable"] = tk.StringVar()

        self.update_userID_var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)

        self.lb_up = False

    def changed(self, name, index, mode):
        # User IDs
        c.execute("SELECT user_id FROM Accounts")
        books_userID_fetch = c.fetchall()
        update_userID_list = [x[0] for x in books_userID_fetch]

        self.lista = update_userID_list

        if self.update_container_autocomplete.winfo_ismapped() is False:
            self.update_container_autocomplete.pack(anchor=tk.W, fill=tk.X, side=tk.TOP)

        if self.update_userID_var.get() == '':
            if self.lb_up:
                self.lb.destroy()
                self.lb_up = False
        else:
            words = self.comparison()
            if words:
                if not self.lb_up:
                    self.lb = tk.Listbox(self.update_container_canvas, width=self["width"], height=self.listboxLength)
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

                    self.update_container_autocomplete.pack_forget()
                    self.update_container_canvas["height"] = 0
                    self.update_container_canvas["width"] = 0

    def selection(self, event):
        if self.lb_up:
            self.update_userID_var.set(self.lb.get(tk.ACTIVE))

            update_userID_fetch = c.execute('SELECT user_id FROM Accounts WHERE user_id=?', (self.update_userID_var.get(),)).fetchall()
            update_userID = [x[0] for x in update_userID_fetch][0]

            self.update_userID_var.set(update_userID)

            self.update_container_autocomplete.pack_forget()
            self.update_container_canvas["height"] = 0
            self.update_container_canvas["width"] = 0

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
        pattern = re.compile('.*' + self.update_userID_var.get() + '.*')
        return [w for w in self.lista if re.match(pattern, str(w))]


class AutoCompleteEntryAP_RemoveAccountID(ttk.Entry):
    '''
    Autocomplete function to display all the possible values that could go into the field, based on what is currently being typed into the entry field.

    Structuraly the same as all the other Autocomplete classes, however this applies to the removal of accounts.
    Already described above.
    '''
    def __init__(self, remove_container_autocomplete, remove_userID_entry, remove_userID_var, remove_container_canvas, *args, **kwargs):

        self.remove_container_autocomplete = remove_container_autocomplete
        self.remove_container_canvas = remove_container_canvas

        #  Listbox length
        if 'listboxLength' in kwargs:
            self.listboxLength = kwargs['listboxLength']
            del kwargs['listboxLength']
        else:
            self.listboxLength = 8

        ttk.Entry.__init__(self, *args, **kwargs)
        self.focus()

        # User IDs
        c.execute("SELECT user_id FROM Accounts")
        remove_userID_fetch = c.fetchall()
        remove_userID_list = [x[0] for x in remove_userID_fetch]

        self.lista = remove_userID_list

        self.remove_userID_var = remove_userID_var

        self.remove_userID_entry = self["textvariable"]
        if self.remove_userID_entry == '':
            self.remove_userID_entry = self["textvariable"] = tk.StringVar()

        self.remove_userID_var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)

        self.lb_up = False

    def changed(self, name, index, mode):
        # User IDs
        c.execute("SELECT user_id FROM Accounts")
        books_userID_fetch = c.fetchall()
        remove_userID_list = [x[0] for x in books_userID_fetch]

        self.lista = remove_userID_list

        if self.remove_container_autocomplete.winfo_ismapped() is False:
            self.remove_container_autocomplete.pack(anchor=tk.W, fill=tk.X, side=tk.TOP)

        if self.remove_userID_var.get() == '':
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
            self.remove_userID_var.set(self.lb.get(tk.ACTIVE))

            remove_userID_fetch = c.execute('SELECT user_id FROM Accounts WHERE user_id=?', (self.remove_userID_var.get(),)).fetchall()
            remove_userID = [x[0] for x in remove_userID_fetch][0]

            self.remove_userID_var.set(remove_userID)

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
        pattern = re.compile('.*' + self.remove_userID_var.get() + '.*')
        return [w for w in self.lista if re.match(pattern, str(w))]