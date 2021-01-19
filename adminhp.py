# Admin Help
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as ms
import linecache
import re

HEADER_FONT = re.sub('^.*?=', '', linecache.getline('config.txt',11)).strip()
class AdminHelp():
    def __init__(self, root, notebook, user_email):
        self.root = root
        self.notebook = notebook

        admin_help_page = tk.Frame(self.notebook)
        notebook.add(admin_help_page, text="Admin Help Page")

        header_frame = tk.Frame(admin_help_page)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        header = tk.Label(header_frame, text="Admin Help Page", font=HEADER_FONT)
        header.pack(side=tk.TOP)

        large_frame = tk.Frame(admin_help_page)
        large_frame.pack(fill=tk.BOTH, expand=True)

        _help = tk.Label(large_frame, text="""The admin page is responsible for allowing
you as an admin, to do the following, with a description of how to accomplish it:

Add Account:
    1. Enter the email address in the 'Email Address' field;
    2. Enter the password in the 'Password' field;
    3. Enter the password confirmation in the 'Confirm Password' field;
    4. Enter the privileges the account will hold, by selecting the staff mode, admin mode, both or none;
    5. Press 'Add Account' button.

Remove Account:
    1. Enter either the User ID or the Email Address and choose an account to autocomplete to;
    2. Press 'Remove Account' button.

Update Account:
    1. Enter either the User ID or the Email Address and choose an account to autocomplete to;
    2. Select the priviliges to be updates on the account. Either staff mode, admin mode, both or none;
    3. Press 'Update Account'.

Manual Returs Reminder:
    Sends an email to all the email address that have a book that is close to needing to be returned.

Using the database at the bottom of the page:
    Use the search parameters to find accounts in the database and any information regarding them (except passwords).
    Issued BookIDs refers to the books that the account has currently issued out.
    Earliest return date refers to the earliest date that one of the books must be returned by.

    The column headings of the database table can be pressed to sort them in ascending/descending order.

Extra Information:
    Analytics must be updated MANUALLY after a change has happened to the database, therefore, if you would like
    to analyse some of the analytics on the system, make sure that you press the 'Update Values' button to get the
    latest, updated information.

    You are not allowed to remove another admins account or update their account details.
""", justify=tk.LEFT)
        _help.pack()
