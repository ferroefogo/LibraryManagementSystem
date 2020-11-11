'''
- Requirements:
        - Database to store all relevant fields for the book information
        - Database to store all relevant issuer's information
        - UI for library staff to update book database (if new books come in/out)
        - UI for library staff to issue out a book
        - UI for users to look at the available books
        - Set a return date based on the day they took the book out.
        - Allow library staff to set return date manually
        - Send email alert if book has not been returned (optional)

Ideas Up for Debate:
    - Date of Return can be chosen by the staff or be a fixed amount (currently 2 weeks)
    - 
    -
    -
    -
'''

# UPDATE 02/08/2020
# - FIXED DATABASE ISSUES REGARDING MyBooks page displaying incorrect information HUGE ISSUE EZY CLAP
# - NEXT STEP: ALLOW STAFF TO RETRIEVE USER BOOK (would involve making the 'issued' field in the Books table 0 instead of 1 when it has been turned in) DONE

# UPDATE 03/08/2020
# - ADDED RETURN BOOK FUNCTIONALITY AS NEEDED ABOVE.
# - REQUIRED FIXES: UPDATE TREEVIEWS ACCORDING TO THE BOOK RETURN. <--- STILL ON THIS. Nope
# - NEXT STEP: ALLOW ADMIN ACCOUNTS TO INTRODUCE NEW BOOKS INTO THE SYSTEM.
# - REMEMBER TO RESET DB BECAUSE THERE IS A NEW FIELD (return_date) AND BECAUSE I MESSED AROUND WITH SOME VALUES.


# UPDATE 09/08/2020
# - FIXED TREEVIEWS NOT UPDATING UPON ISSUE/RETURN
# - REQUIRED FIXES: AUTOCOMPLETE BOX NOT FETCHING UPDATED DATABASE TABLES AFTER A BOOK ISSUE/RETURN

# UPDATE 02/09/2020
# - FIXED MY BOOKS TREEVIEW NOT UPDATING (ADDED REFRESH TREEVIEW BUTTON)
# - REQUIRED FIXES: AUTOCOMPLETE BOX (ON BOOK DATABASE CLASS) NOT FETCHING UPDATED DATABASE TITLES AFTER A BOOK ISSUE/RETURN, HOWEVER IT FIXES ITSELF AFTER A RESTART/ CAUSED BY PRESSING RETURN/ISSUE BUTTON;
#                   AUTOCOMPLETE BOX (ON BOOK DATABASE CLASS) APPEARING TWICE UPON ISSUE/RETURN BUTTON BEING PRESSED
#                   AUTOCOMPLETE FILTER BOX (ON MY BOOKS CLASS) SHOWING ALL BOOKS RATHER USER'S BOOKS.

# UPDATE 03/09/2020 AND 04/09/2020
# - FIXES:
#       - AUTOCOMPLETE BOX (ON BOOK DATABASE CLASS) NOT FETCHING UPDATED DATABASE TITLES AFTER A BOOK ISSUE/RETURN, HOWEVER IT FIXES ITSELF AFTER A RESTART/ CAUSED BY PRESSING RETURN/ISSUE BUTTON;
#       - AUTOCOMPLETE BOX (ON BOOK DATABASE CLASS) APPEARING TWICE UPON ISSUE/RETURN BUTTON BEING PRESSED
#       - AUTOCOMPLETE FILTER BOX (ON MY BOOKS CLASS) SHOWING ALL BOOKS RATHER USER'S BOOKS.

#       - AUTOCOMPLETE IS NOW INDEPENDENT FOR EACH ENTRY BOX. HOWEVER, IF YOU SELECT AN AUTOCOMPLETE OPTION,
#         THE OTHERS WILL TRIGGER AND YOU WONT BE ABLE TO CLOSE ALL THE AUTOCOMPLETE BOXES.
#       - FIXED BY REMOVING ALL AUTOCOMPLETE BOXES EXCEPT FOR THE BOOKID FIELD.
#
# - REQUIRED FIXES/ADDITIONS:
#       - ALLOW BOOKS TO BE ISSUED BY THEIR bookID - COMPLETE
#       - ALLOW STAFF TO INTRODUCE NEW BOOKS/REMOVE MISSING BOOKS FROM THE DATABASE. - COMPLETE
#       - ALLOW LIBRARY AND MY BOOKS PAGE TO BE SEARCHED BY bookID - COMPLETE
#       - SHOW bookID COLUMN ON THE TREEVIEW TABLES. - COMPLETE

# UPDATE 05/09/2020
# - QUALITY OF LIFE ADDITIONS/FIXES:
#       - FOCUS SIGN IN PAGE ONTO THE LOGIN BOX (so that the user can start typing their email immediately) - COMPLETE
#       - ALLOW <Return> BUTTON TO LOGIN/REGISTER THE USER AMONG OTHER PLACES WHERE PRESSING <Return> FEELS NATURAL TO COMPLETE A TASK - COMPLETE
#       - MOVE SOME OF THE FILTER FRAMES CLOSER TO THE TREEVIEWS FOR EASIER ACCESS AND INTERPRETATION - COMPLETE
#       - DON'T ALLOW STAFF TO CHANGE THE DATE OF ISSUING/RETURN ON THE BOOK DATABASE PAGE
#       - INPUT VALIDATION SO THAT INCORRECT/INVALID DATA CANNOT BE ENTERED INTO MANY FIELDS LIKE THE ISSUE/RETURN BOOKS PAGE
#       - ADD A FEW CUSTOMISATION OPTIONS ONTO THE OPTIONS PAGE
#       - FIND USE FOR HOME PAGE OR REMOVE IT AND MAKE THE DEFAULT PAGE UPON LOGIN THE LIBRARY PAGE.
#       - MOVE THE AUTOCOMPLETE BOX TO A MORE ADEQUATE LOCATION - COMPLETE
#       - FIND A WAY TO FETCH THE LOWEST AVAILABLE BOOK IDS THAT ARE NOT BEING USED, DUE TO THEM BEING REMOVED PREVIOUSLY. FIND VACANT BOOKIDS IF YOU WILL. - NOT NEEDED ANYMORE
#       - ALLOW STAFF TO ADD NEW GENRES TO THE OptionMenu - HALFWAY THROUGH THIS - COMPLETE

# UPDATE 06/09/2020
#       - MAKE ALL DATE ENTRIES THE SAME FORMAT (UK FORMAT DD/MM/YYYY) - COMPLETE
#       - FIX ENCRYPTED PASSWORD SHTICK
#
#       - DISALLOW USERS FROM TAKING OUT THE SAME BOOK MULTIPLE TIMES, SO IF I HAVE A BOOK WITH THE bookID = 1, THAT BOOK CANNOT BE ISSUED OUT ANYMORE. -COMPLETE
#
#       - INPUT VALIDATION FOR THE FOLLOWING:
#             - BOOKID FILTER IN MYBOOKS MUST BE INTEGERS ONLY - COMPLETE
#             - BOOKID SEARCH IN LIBRARY MUST BE INTEGERS ONLY - COMPLETE
#             - BOOKID SEARCH IN ISSUE BOOK, RETURN BOOK AND REMOVE BOOK FROM SYSTEM MUST BE INTEGERS ONLY - COMPLETE
#             - DATE OF ISSUED/DATE OF RETURN MUST HAVE A DATE THAT HASNT ALREADY GONE BY
#             - GENRE NAME IN ADD BOOK INTO SYSTEM IN BOOK DB PAGE MUST NOT HAVE NUMBERS 

# UPDATE 07/09/2020
# - FIXES:
#       - Dates now show in UK format.
# - TODO:
#       - Fix password encryption.
#       - CONCEPT: Make section in BookDB page that allows staff to search the treeview below. - COMPLETED
#       - Connect Email Functionality to the software:
#                   - Add Functionality to the Send Request button on the Forgot Password? Page at the application startup.
#                   - Add Functionality to the Change Password? button on the Account page whilst logged in
#                   - Add email notification that is sent out upon book being issued to said recipients' email.
#                   - Add email notification that is sent out upon book being returned to said recipients' email.
#                   - Add email notification that is sent out upon return date being passed. *CONCEPT, MAY BE HARD*
#
#       - Allow user to sort treeview tables by pressing the column headers *CONCEPT*
#       - Add Options Page Functionality to the software, allowing the user to customise/change:
#                   - Background Colours
#                   - Foreground Colours
#                   - Fonts
#                   - More to come etc...
#       - Add ttk.Style to make design more sleek
#

# UPDATE 16/09/2020
# - FIXES:
#       - ADDED ABILITY TO SEARCH THE BOOKDB PAGE TREEVIEW BY ANY FIELD FROM BOOKID TO ISSUED STATE.
# - TODO:
#       - Fix 'Date of Return' field on Return Book container in Book Database Page.
#       - Decide what happens with the font stuff. Either all widgets have font field or none.
#       - Add ttk.Style to make design more sleek (Needs to be explored, never used before.)
#       - Check ttk.Style possible issues
#       - 'Return Book' button text is slightly shifted down when the autocomplete box is dragged down. investigate
#       - Allow admin to assign other admin accounts (staff accounts) to new employees.
#

# UPDATE 29/09/2020
# - FIXES:
#       - DATABASE NOW STORES PASSWORDS USING A HASHING ALGORITHM AND SALT
# - TODO:
#       - ALL ISSUE/RETURN buttons get pushed down outside the frame. /FIXED
#       - ERROR: ValueError: time data '13/10/2020' does not match format '%Y-%m-%d' when a is entered into issue date box /FIXED
#       - autocomplete box is being packed below issue/return button after being forgotten. /FIXED
#       - Genre list in the database needs to be updated to have all the correct genres stored. /FIXED
#       - When removing book, remove any links it has to any users (idk if ive covered this yet) /already fixed previously
#       - Add prompt feedback when pressing the buttons to let user know the action has gone through. /ADDED
#
#       - Set register details to empty strings after registration and automatically redirect the user to the login page. /ADDED
#       - Add logout feature (always in the top corner? or on the account page?) /ADDED
#       - Add account deletion feature on Account page /ADDED
#       - Add functionality to Change Password part in Accounts page. /ADDED
#       - Add the thing that shows how strong the password is upon registration /DONE
#       - Add ability to see their own password with a toggle button /DONE
#       - Added Restrictions on password using regex. /DONE? I THINK?
#       
#       - Add location of book in the library in the database. (MAY REQUIRE DATABASE RECONFIGURATION AND WILL CHANGE THE SCOPE OF THE PROJECT SLIGHTLY IN THE WORD DOCUMENT)
#       - Only allow user to remove a genre if its not in use by any other books. /DONE
#       - Add feature to allow staff accounts to add other staff accounts to the database.
#       - Compact repeated code into functions to make code a bit less overwhelming
#       
#       - Find a way to implement Quicksort into this.
#       - The autofill algorithm should display what fields its going to fill in the title, author and all that before a selection is made, rather than just show the bookID that tells the staff nothing at first glance.
#
#
#       cba to update log (06/11/20) but i need to fix the send request function a bit. good stuff tho
#
# - TODO:
#       - Validate BookID entry on "Add Book into System" section/DONE
#       - No option showing up for "-EMPTY-" genre on" Add Book Into System" section/DONE
#       - "Issue Book" section labels have "Book" before their respective entries, remove that./DONE
#       - "Issue date" and "return date" is not being saved to the MyBooks page/DONE
#       - "location" is not being saved to the "Books" table./DONE
#       - Search by genre on BookDatabase page at the bottom does not show "-EMPTY-" as an option./DONE
#       - No option showing up for "-EMPTY-" genre on "Remove Book From System" section/DONE
#       - No books showing up on the Library treeview/DONE
#       - No books showing up on the MyBooks treeview/DONE
#       - MyBooks filter section, the genre optionmenu does not show the "-EMPTY-" option/DONE
#        
# - TODO: (07/11/20)
#       - Treeview sorting algorithm using quicksort (already works with what i have, but it isnt coursework. I want to apply it for more marks) /DONE (Needs tweaking so that when the filters are put on it can filter within that.)
#       - Autocomplete book with all fields in the issue book, return book and remove book sections
#       - Send emails regarding return dates as they draw near. (Admin button to send out alerts that are nearing perhaps)
#       - Complete analytics side of admin page with numpy maybe and other graphs
#       - Make Filters on Library and MyBooks work together to find a value. (optimising the filters)
#       - Add filters using tkCalendar to allow the staff to search by return date or issue date. The same applies to the MyBooks page where the user can search the treeview based on a return/issue date using a filter.
#       -
#       -
#       -
#       -
#       -
#       -
#       -
#       -
#       -
#       -
#

import tkinter as tk
from tkinter import ttk
import re
from tkinter import messagebox as ms
import sys
import bcrypt
import sqlite3
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import base64
import logging
import mimetypes
import os
import os.path
import pickle
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient import errors
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import random
import secrets
import string

conn = sqlite3.connect('LibrarySystem.db')
c = conn.cursor()

global firstRun
firstRun = True
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



class Admin():
    #ADMIN ACCESS ONLY (NO STAFF OR REGULAR USERS ALLOWED)
    #Allows library admin(s) to create accounts for the staff.
    #Displays analytical data for the admin users to read from.
    def __init__(self, root, notebook, user_email):
        self.root = root
        self.notebook = notebook

        admin_page = tk.Frame(self.notebook)
        notebook.add(admin_page, text="Admin")

        header_frame = tk.Frame(admin_page)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        header = tk.Label(header_frame, text="Admin", font='System 30')
        header.pack(side=tk.TOP)

        #Add Staff Account
        add_account_container = tk.Frame(admin_page, bg=bg)
        add_account_container.pack(side=tk.LEFT, anchor=tk.N, padx=padx, pady=pady)

        add_account_header = tk.Label(add_account_container, text='Add Account', font='System 18', bg=bg)
        add_account_header.pack(anchor=tk.W, padx=padx, pady=pady)

        #User ID Field
        self.userID_container = tk.Frame(add_account_container, bg=bg)
        self.userID_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        userID_label = tk.Label(self.userID_container, text='User ID: ', bg=bg)
        userID_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.userID_var = tk.StringVar()
        #set the variable to +1 the highest userID in the database to make a new account on that record.
        self.userID_var.set('')

        self.userID_entry = ttk.Entry(self.userID_container)
        self.userID_entry.config(textvariable=self.userID_var, state=tk.DISABLED)
        self.userID_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)

        #Email Address Entry Field
        self.email_container = tk.Frame(add_account_container, bg=bg)
        self.email_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        email_label = tk.Label(self.email_container, text='Email Address: ', bg=bg)
        email_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.email_var = tk.StringVar()

        self.email_entry = ttk.Entry(self.email_container, textvariable=self.email_var)
        self.email_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)

        #Password Entry Field
        self.password_container = tk.Frame(add_account_container, bg=bg)
        self.password_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        password_label = tk.Label(self.password_container, text='Password: ', bg=bg)
        password_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.password_var = tk.StringVar()

        self.password_entry = ttk.Entry(self.password_container, textvariable=self.password_var)
        self.password_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Password Entry Field
        self.confirm_password_container = tk.Frame(add_account_container, bg=bg)
        self.confirm_password_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        confirm_password_label = tk.Label(self.confirm_password_container, text='Confirm Password: ', bg=bg)
        confirm_password_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.confirm_password_var = tk.StringVar()

        self.confirm_password_entry = ttk.Entry(self.confirm_password_container, textvariable=self.confirm_password_var)
        self.confirm_password_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Add Account
        add_account_button_container = tk.Frame(add_account_container, bg=bg)
        add_account_button_container.pack(anchor=tk.W, fill=tk.X, expand=True)


        add_account_btn = ttk.Button(add_account_button_container)
        add_account_btn.config(text='    Add Account    ', command=self.add_account)
        add_account_btn.pack(side=tk.RIGHT, anchor=tk.W, padx=padx, pady=pady)





         #Add Staff Account
        remove_account_container = tk.Frame(admin_page, bg=bg)
        remove_account_container.pack(side=tk.LEFT, anchor=tk.N, padx=padx, pady=pady)

        remove_account_header = tk.Label(remove_account_container, text='Remove Account', font='System 18', bg=bg)
        remove_account_header.pack(anchor=tk.W, padx=padx, pady=pady)

        #User ID Field
        self.remove_userID_container = tk.Frame(remove_account_container, bg=bg)
        self.remove_userID_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        remove_userID_label = tk.Label(self.remove_userID_container, text='User ID: ', bg=bg)
        remove_userID_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.remove_userID_var = tk.StringVar()
        #set the variable to +1 the highest userID in the database to make a new account on that record.
        self.remove_userID_var.set('')

        self.remove_userID_entry = ttk.Entry(self.remove_userID_container)
        self.remove_userID_entry.config(textvariable=self.remove_userID_var, state=tk.DISABLED)
        self.remove_userID_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)

        #Email Address Entry Field
        self.remove_email_container = tk.Frame(remove_account_container, bg=bg)
        self.remove_email_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        remove_email_label = tk.Label(self.remove_email_container, text='Email Address: ', bg=bg)
        remove_email_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.remove_email_var = tk.StringVar()

        self.remove_email_entry = ttk.Entry(self.remove_email_container, textvariable=self.remove_email_var)
        self.remove_email_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Remove Account
        remove_account_button_container = tk.Frame(remove_account_container, bg=bg)
        remove_account_button_container.pack(anchor=tk.W, fill=tk.X, expand=True)


        remove_account_btn = ttk.Button(remove_account_button_container)
        remove_account_btn.config(text='    Remove Account    ', command=self.remove_account)
        remove_account_btn.pack(side=tk.RIGHT, anchor=tk.W, padx=padx, pady=pady)







        #Update Existing Account
        #Allows an admin to update the permissions of a staff/user account.
        update_account_container = tk.Frame(admin_page, bg=bg)
        update_account_container.pack(side=tk.LEFT, anchor=tk.N, padx=padx, pady=pady)

        update_account_header = tk.Label(update_account_container, text='Update Account', font='System 18', bg=bg)
        update_account_header.pack(anchor=tk.W, padx=padx, pady=pady)

        #UserID Entry Field
        self.update_account_userID_container = tk.Frame(update_account_container, bg=bg)
        self.update_account_userID_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        update_userID_label = tk.Label(self.update_account_userID_container, text='User ID: ', bg=bg)
        update_userID_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.update_userID_var = tk.StringVar()

        self.update_userID_var = ttk.Entry(self.update_account_userID_container)
        self.update_userID_var.config(textvariable=self.update_userID_var, state=tk.DISABLED)
        self.update_userID_var.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Email Address Entry Field
        self.update_account_email_container = tk.Frame(update_account_container, bg=bg)
        self.update_account_email_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        update_email_label = tk.Label(self.update_account_email_container, text='Email Address: ', bg=bg)
        update_email_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.update_email_var = tk.StringVar()

        self.update_email_entry = ttk.Entry(self.update_account_email_container, textvariable=self.update_email_var)
        self.update_email_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Update staff mode frame
        update_mode_container = tk.Frame(update_account_container, bg=bg)
        update_mode_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        update_mode_label = tk.Label(update_mode_container, text='Staff Mode: ', bg=bg)
        update_mode_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.staff_mode_var = tk.IntVar()

        staff_mode_checkbtn = ttk.Checkbutton(update_mode_container, variable=self.staff_mode_var)
        staff_mode_checkbtn.pack(side=tk.LEFT, anchor=tk.E, padx=padx, pady=pady)


        #Update Account Button
        update_account_button_container = tk.Frame(update_account_container, bg=bg)
        update_account_button_container.pack(anchor=tk.W, fill=tk.X, expand=True)

        update_account_btn = ttk.Button(update_account_button_container)
        update_account_btn.config(text='    Update Account    ', command=self.update_account)
        update_account_btn.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)



        #Analytical Information
        analytics_container = tk.Frame(admin_page, bg=bg)
        analytics_container.pack(side=tk.LEFT, anchor=tk.N, padx=padx, pady=pady)

        analytics_header = tk.Label(analytics_container, text='Analytics', font='System 18', bg=bg)
        analytics_header.pack(anchor=tk.W, padx=padx, pady=pady, expand=True, fill=tk.BOTH)
        


        #Analytical graphs will be created using numpy or something alike. This will be a great opportunity to use quicksort to sort a table of data values for the user.
        #There will be buttons that open TopLevels that show the information regarding its topic accordingly.

        #Types of data we could include here:
        #   - Number of user accounts
        #   - Number of staff accounts
        #   - Number of admin accounts
        #   - Total book tally
        #   - Total issued book tally
        #   - Total Non-Issued book tally
        #   - Ratio of successfully returned books to books that have been issued and not returned (more complex)
        #   - Average number of days before return
        #   - Average number of books issued out on a single day
        #

    def add_account(self):
        pass

    def update_account(self):
        pass

    def remove_account(self):
        pass
    # def password_strength(self, *args):
    #     special_characters_regex = re.compile("""[!@#$%^*-_+=|\\\{\}\[\]`¬;:@"'<>,./?]""")
    #     password_input = self.user_password_var.get()

    #     if len(password_input) >= 8:
    #         self.password_strength_container_1.pack_forget()
    #         if special_characters_regex.search(password_input) != None :
    #             self.password_strength_container_2.pack_forget()
    #         else:
    #             self.password_strength_container_2.pack(expand=True)

    #     elif len(password_input) < 8:
    #         self.password_strength_container_1.pack(expand=True)
    #         if special_characters_regex.search(password_input) != None :
    #             self.password_strength_container_2.pack_forget()
    #         else:
    #             self.password_strength_container_2.pack(expand=True)

    # def show_password(self, *args):
    #     if self.password_entry["show"] == "*":
    #         self.password_entry["show"]=''
    #         self.confirm_pw_entry["show"]=''
    #     else:
    #         self.password_entry["show"]='*'
    #         self.confirm_pw_entry["show"]='*'







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
            c.execute("SELECT date_issued FROM MyBooks WHERE my_booksID=(SELECT my_booksID WHERE bookID=?)",(bookID_list[i],))
            date_issued_fetch = c.fetchall()
            date_issued_list = [x[0] for x in date_issued_fetch]

            #Return Date
            c.execute("SELECT return_date FROM MyBooks WHERE my_booksID=(SELECT my_booksID WHERE bookID=?)",(bookID_list[i],))
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
        date_container = tk.Frame(filter_container, bg=bg)
        date_container.pack(anchor=tk.W, fill=tk.X, expand=True)

        recipient_label = tk.Label(date_container, text='Date of Issuing: ', bg=bg)
        recipient_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.date_entry = DateEntry(date_container, width=12, background='darkblue',
                    foreground='white', borderwidth=2, mindate=datetime.now(), maxdate=datetime.now(), locale='en_UK')
        self.date_entry.pack(padx=padx, pady=pady)



        #Return date frame
        return_date_container = tk.Frame(filter_container, bg=bg)
        return_date_container.pack(anchor=tk.W, fill=tk.X, expand=True)

        return_date_label = tk.Label(return_date_container, text='Last Valid Return Date: ', bg=bg)
        return_date_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        return_date_calc = str(self.date_entry.get_date() + timedelta(days=14))
        return_date_value = str(datetime.strptime(return_date_calc, "%Y-%m-%d").strftime('%Y-%m-%d'))

        self.return_date_var = tk.StringVar()
        self.return_date_var.set(return_date_value)

        return_date_entry = ttk.Entry(return_date_container, state=tk.DISABLED, textvariable=self.return_date_var)
        return_date_entry.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)


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
                    foreground='white', borderwidth=2, locale='en_UK')
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
            c.execute("SELECT date_issued FROM MyBooks WHERE my_booksID=(SELECT my_booksID WHERE bookID=?)",(bookID_list[i],))
            date_issued_fetch = c.fetchall()
            date_issued_list = [x[0] for x in date_issued_fetch]

            #Return Date
            c.execute("SELECT return_date FROM MyBooks WHERE my_booksID=(SELECT my_booksID WHERE bookID=?)",(bookID_list[i],))
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
        check_book_owned = c.execute('SELECT my_booksID FROM MyBooks WHERE bookID=?',(remove_bookID_var,)).fetchall()
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
            c.execute("SELECT date_issued FROM MyBooks WHERE my_booksID=(SELECT my_booksID WHERE bookID=?)",(bookID_list[i],))
            date_issued_fetch = c.fetchall()
            date_issued_list = [x[0] for x in date_issued_fetch]

            #Return Date
            c.execute("SELECT return_date FROM MyBooks WHERE my_booksID=(SELECT my_booksID WHERE bookID=?)",(bookID_list[i],))
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
        date_issued = self.date_entry.get_date()

        date_issued_string = str(date_issued.strftime('%d-%m-%Y'))

        if str(date_issued_string) == str(datetime.today().strftime('%d-%m-%Y')):
            date_return = self.return_date_var.get()

            book_id_search = c.execute('SELECT bookID FROM Books WHERE title=? AND author=? ',(title_var, author_var)).fetchall()
            book_id = [x[0] for x in book_id_search][0]

            # Send info to db
            account_info_fetch = c.execute('SELECT * FROM Accounts WHERE email_address=?',(recipient_email,)).fetchall()
            account_mybooks_check = [x[5] for x in account_info_fetch][0]

            #Check if book is already issued out
            book_already_issued_fetch = c.execute('SELECT issued FROM Books WHERE bookID=?',(bookID_var,)).fetchall()
            book_already_issued = [x[0] for x in book_already_issued_fetch][0]

            if book_already_issued == 0:
                insert_my_bookID = 'INSERT INTO MyBooks(my_booksID,bookID) VALUES(?,?)'
                c.execute(insert_my_bookID,[(account_mybooks_check),(book_id)])
                conn.commit()

                update_issued_val = c.execute('UPDATE Books SET issued=1 WHERE bookID=?',(book_id,))
                conn.commit()

                update_date_issued_val = c.execute("""UPDATE MyBooks
                    SET date_issued=?
                    WHERE my_booksID = (SELECT my_booksID FROM Accounts WHERE email_address=?)""",(date_issued, recipient_email))
                conn.commit()

                update_return_date_val = c.execute("""UPDATE MyBooks
                    SET return_date=?
                    WHERE my_booksID = (SELECT my_booksID FROM Accounts WHERE email_address=?)""",(date_return, recipient_email))
                conn.commit()
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
                c.execute("SELECT date_issued FROM MyBooks WHERE my_booksID=(SELECT my_booksID WHERE bookID=?)",(bookID_list[i],))
                date_issued_fetch = c.fetchall()
                date_issued_list = [x[0] for x in date_issued_fetch]

                #Return Date
                c.execute("SELECT return_date FROM MyBooks WHERE my_booksID=(SELECT my_booksID WHERE bookID=?)",(bookID_list[i],))
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

            ms.showinfo('Success', 'Book issued out successfully')
        else:
            ms.showerror('Error','Invalid DOI (Date of Issue)')



    def return_book(self):
        #Send entered information to the database.
        #Retrieve all entryboxes variables

        #May need try/except block here
        title_var = self.ret_title_var.get()
        author_var = self.ret_author_var.get()
        return_email = self.return_email_var.get()
        date_return = self.return_date_var.get()

        book_id_search = c.execute('SELECT bookID FROM Books WHERE title=? AND author=? ',(title_var, author_var)).fetchall()
        book_id = [x[0] for x in book_id_search][0]

        # Send info to db
        #could be shortened a bit.
        account_info_fetch = c.execute('SELECT * FROM Accounts WHERE email_address=?',(return_email,)).fetchall()
        account_mybooks_check = [x[4] for x in account_info_fetch][0]

        #Remove my_booksID from the ownership of the user and onto the public library.

        remove_my_booksID = 'DELETE FROM MyBooks WHERE bookID=?'
        c.execute(remove_my_booksID,[(book_id)])
        conn.commit()

        update_issued_val = c.execute('UPDATE Books SET issued=0 WHERE bookID=?',(book_id,))
        conn.commit()

        #Set entryfields to empty after return
        self.ret_bookID_var.set('')
        self.ret_title_var.set('')
        self.ret_author_var.set('')
        self.return_email_var.set('')

        #Update Treeview table in BookDatabase Page
        #Maybe pack into a function?
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
            c.execute("SELECT date_issued FROM MyBooks WHERE my_booksID=(SELECT my_booksID WHERE bookID=?)",(bookID_list[i],))
            date_issued_fetch = c.fetchall()
            date_issued_list = [x[0] for x in date_issued_fetch]

            #Return Date
            c.execute("SELECT return_date FROM MyBooks WHERE my_booksID=(SELECT my_booksID WHERE bookID=?)",(bookID_list[i],))
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

        ms.showinfo('Success', 'Book returned successfully')

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
            print(issued_text)

            if query_issued in str(issued_text):
                i_r += 1
                self.tree.reattach(item_id, '', i_r)

            elif query_issued == '-EMPTY-':
                self.tree.reattach(item_id, '', i_r)

            else:
                self._detached.add(item_id)
                self.tree.detach(item_id)

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
            self.ret_date_entry.set_date(datetime.strptime(return_date, '%d-%m-%Y'))

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


class Library():
    #USER ACCESS
    #Look for more books in the database (VIEW ONLY).
    def __init__(self, root, notebook):
        self.tree_ids = [] #creates a list to store the ids of each entry in the tree

        library_page = tk.Frame(notebook)
        notebook.add(library_page, text='Library')

        notebook.bind("<<NotebookTabChanged>>", self.notebook_tab_change)

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
        self.bookID_var.trace("w", self._columns_searcher_bookID) #callback if stringvar is updated

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
        self.title_var.trace("w", self._columns_searcher_title) #callback if stringvar is updated

        self.title_entry = ttk.Entry(search_container_title, textvariable=self.title_var) #create entry

        self.title_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Author Filter
        search_author_container = tk.Frame(filter_container, bg=bg)
        search_author_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        author_filter_label = tk.Label(search_author_container, text='Author:', bg=bg)
        author_filter_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.author_var = tk.StringVar()
        self.author_var.trace("w", self._columns_searcher_author)

        self.author_entry = ttk.Entry(search_author_container, textvariable=self.author_var, font='System 6')
        self.author_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Genre Filter
        genre_filter_label = tk.Label(filter_container, text='Genre:', bg=bg)
        genre_filter_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.genre_var = tk.StringVar()
        self.genre_var.set("-EMPTY-")
        self.genre_var.trace("w", self._columns_searcher_genre)

        self.genre_menu = ttk.OptionMenu(filter_container, self.genre_var,genre_choice_list[0], *genre_choice_list)
        self.genre_menu.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)

        #location Filter
        location_filter_label = tk.Label(filter_container, text='Location:', bg=bg)
        location_filter_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.location_var = tk.StringVar()
        self.location_var.set("-EMPTY-")
        self.location_var.trace("w", self._columns_searcher_location)

        self.location_menu = ttk.OptionMenu(filter_container, self.location_var,location_choice_list[0], *location_choice_list)
        self.location_menu.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


    def notebook_tab_change(self, event):
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
        c.execute("SELECT genre FROM Genres")
        genres_list_fetch = c.fetchall()
        genre_choice_list = [x[0] for x in genres_list_fetch]

        genre_menu = self.genre_menu["menu"]
        genre_menu.delete(0, tk.END)
        for string in genre_choice_list:
            genre_menu.add_command(label=string,
                             command=lambda value=string: self.genre_var.set(value))

    def bookID_validate(self, bookID_input):
        if bookID_input.isdigit():
            return True
        elif bookID_input is "":
            return True
        else:
            return False




    # Works, but all filters are independent from each other, meaning if you search for a title and then enter a completely unrelated author, it will search
    # for the last key field entered search. So the author's books would show up, with no relation to the Title searched.
    # Improvement: Allow for the filters to be dependant on each other, eg. search for author 'John', and one of his books called 'Test' amongst other books he
    # may have released under different titles.
    def _columns_searcher_bookID(self, *args):
        children = list(self._detached) + list(self.tree.get_children())
        self._detached = set()
        query_bookID = self.bookID_entry.get()

        self.search_bookID_tv(children, query_bookID)

    def _columns_searcher_title(self, *args):
        children = list(self._detached) + list(self.tree.get_children())
        self._detached = set()
        query_title = self.title_entry.get()

        self.search_title_tv(children, query_title)

    def _columns_searcher_author(self, *args):
        children = list(self._detached) + list(self.tree.get_children())
        self._detached = set()
        query_author = self.author_entry.get()

        self.search_author_tv(children, query_author)

    def _columns_searcher_genre(self, *args):
        children = list(self._detached) + list(self.tree.get_children())
        self._detached = set()
        query_genre = self.genre_var.get()

        self.search_genre_tv(children, query_genre)

    def _columns_searcher_location(self, *args):
        children = list(self._detached) + list(self.tree.get_children())
        self._detached = set()
        query_location = self.location_var.get()

        self.search_genre_tv(children, query_location)

    def search_bookID_tv(self, children, query_bookID):
        i_r = -1

        for item_id in children:
            bookID_text = str(self.tree.item(item_id)['values'][0])

            if query_bookID in bookID_text:
                i_r += 1
                self.tree.reattach(item_id, '', i_r)

            else:
                self._detached.add(item_id)
                self.tree.detach(item_id)

    def search_title_tv(self, children, query_title):
        i_r = -1

        for item_id in children:
            title_text = self.tree.item(item_id)['values'][1]

            if query_title in title_text:
                i_r += 1
                self.tree.reattach(item_id, '', i_r)

            else:
                self._detached.add(item_id)
                self.tree.detach(item_id)

    def search_author_tv(self, children, query_author):
        i_r = -1

        for item_id in children:
            author_text = self.tree.item(item_id)['values'][2]

            if query_author in author_text:
                i_r += 1
                self.tree.reattach(item_id, '', i_r)

            else:
                self._detached.add(item_id)
                self.tree.detach(item_id)

    def search_genre_tv(self, children, query_genre):
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

    def search_location_tv(self, children, query_location):
        i_r = -1

        for item_id in children:
            location_text = self.tree.item(item_id)['values'][3]

            if query_location in location_text:
                i_r += 1
                self.tree.reattach(item_id, '', i_r)

            elif query_location == '-EMPTY-':
                self.tree.reattach(item_id, '', i_r)

            else:
                self._detached.add(item_id)
                self.tree.detach(item_id)



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

        # Library TreeView Book Database Frame
        tree_container = tk.Frame(my_books_page)
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

        #BookIDs
        c.execute("""SELECT Books.bookID
            FROM MyBooks
            INNER JOIN Books
            ON MyBooks.bookID = Books.bookID
            INNER JOIN Accounts
            ON MyBooks.my_booksID = Accounts.my_booksID
            WHERE Accounts.my_booksID = (SELECT my_booksID FROM Accounts WHERE email_address=?)""",(self.user_email,))
        user_books_bookIDs_fetch = c.fetchall()
        user_book_bookID_list = [x[0] for x in user_books_bookIDs_fetch]


        #Titles
        c.execute("""SELECT Books.title
            FROM MyBooks
            INNER JOIN Books
            ON MyBooks.bookID = Books.bookID
            INNER JOIN Accounts
            ON MyBooks.my_booksID = Accounts.my_booksID
            WHERE Accounts.my_booksID = (SELECT my_booksID FROM Accounts WHERE email_address=?)""",(self.user_email,))
        user_books_title_fetch = c.fetchall()
        user_book_title_list = [x[0] for x in user_books_title_fetch]


        #Authors
        c.execute("""SELECT Books.author
            FROM MyBooks
            INNER JOIN Books
            ON MyBooks.bookID = Books.bookID
            INNER JOIN Accounts
            ON MyBooks.my_booksID = Accounts.my_booksID
            WHERE Accounts.my_booksID = (SELECT my_booksID FROM Accounts WHERE email_address=?)""",(self.user_email,))
        user_books_author_fetch = c.fetchall()
        user_book_author_list = [x[0] for x in user_books_author_fetch]


        #Genres
        c.execute("""SELECT Books.genre
            FROM MyBooks
            INNER JOIN Books
            ON MyBooks.bookID = Books.bookID
            INNER JOIN Accounts
            ON MyBooks.my_booksID = Accounts.my_booksID
            WHERE Accounts.my_booksID = (SELECT my_booksID FROM Accounts WHERE email_address=?)""",(self.user_email,))
        user_books_genre_fetch = c.fetchall()
        user_book_genre_list = [x[0] for x in user_books_genre_fetch]

        for i in range(len(user_book_bookID_list)):
            #creates an entry in the tree for each element of the list
            #then stores the id of the tree in the self.ids list
            self.tree_ids.append(self.tree.insert("", "end", values=(user_book_bookID_list[i], user_book_title_list[i], user_book_author_list[i], user_book_genre_list[i])))
        self.tree.pack()

        #Search Books UI
        filter_container = tk.Frame(my_books_page, bg=bg)
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
        self.bookID_var.trace("w", self._columns_searcher_bookID) #callback if stringvar is updated

        self.bookID_entry = ttk.Entry(search_container_bookID)
        self.bookID_entry.config(textvariable=self.bookID_var, validate="key",
                            validatecommand=(self.bookID_reg, "%P"))
        self.bookID_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Titles Filter
        search_container_title = tk.Frame(filter_container, bg=bg)
        search_container_title.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        title_label = tk.Label(search_container_title, text='Title: ', bg=bg)
        title_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self._detached = set()
        self.title_var = tk.StringVar() #create stringvar for entry widget
        self.title_var.trace("w", self._columns_searcher_title) #callback if stringvar is updated

        self.title_entry = ttk.Entry(search_container_title, textvariable=self.title_var)
        self.title_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Author Filter
        search_container_author = tk.Frame(filter_container, bg=bg)
        search_container_author.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        author_label = tk.Label(search_container_author, text='Author: ', bg=bg)
        author_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self._detached = set()
        self.author_var = tk.StringVar() #create stringvar for entry widget
        self.author_var.trace("w", self._columns_searcher_author) #callback if stringvar is updated

        self.author_entry = ttk.Entry(search_container_author, textvariable=self.author_var)
        self.author_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Genre Filter
        search_container_genre = tk.Frame(filter_container, bg=bg)
        search_container_genre.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        genre_label = tk.Label(search_container_genre, text='Genre:', bg=bg)
        genre_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.genre_var = tk.StringVar()
        self.genre_var.set("-EMPTY-")
        self.genre_var.trace("w", self._columns_searcher_genre)

        self.genre_menu = ttk.OptionMenu(search_container_genre, self.genre_var,genre_choice_list[0], *genre_choice_list)
        self.genre_menu.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)

        #Location Filter
        search_container_location = tk.Frame(filter_container, bg=bg)
        search_container_location.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        location_label = tk.Label(search_container_location, text='Location:', bg=bg)
        location_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.location_var = tk.StringVar()
        self.location_var.set("-EMPTY-")
        self.location_var.trace("w", self._columns_searcher_location)

        self.location_menu = ttk.OptionMenu(search_container_location, self.location_var,location_choice_list[0], *location_choice_list)
        self.location_menu.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)



        refresh_container = tk.Frame(filter_container, bg=bg)
        refresh_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        refresh_label = tk.Label(refresh_container, text='Update Page Values: ', bg=bg)
        refresh_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        refresh_button = ttk.Button(refresh_container, text='Refresh', command=self.refresh_page)
        refresh_button.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

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
            ON MyBooks.my_booksID = Accounts.my_booksID
            WHERE Accounts.my_booksID = (SELECT my_booksID FROM Accounts WHERE email_address=?)""",(self.user_email,))
        user_books_bookIDs_fetch = c.fetchall()
        user_book_bookID_list = [x[0] for x in user_books_bookIDs_fetch]


        #Titles
        c.execute("""SELECT Books.title
            FROM MyBooks
            INNER JOIN Books
            ON MyBooks.bookID = Books.bookID
            INNER JOIN Accounts
            ON MyBooks.my_booksID = Accounts.my_booksID
            WHERE Accounts.my_booksID = (SELECT my_booksID FROM Accounts WHERE email_address=?)""",(self.user_email,))
        user_books_title_fetch = c.fetchall()
        user_book_title_list = [x[0] for x in user_books_title_fetch]


        #Authors
        c.execute("""SELECT Books.author
            FROM MyBooks
            INNER JOIN Books
            ON MyBooks.bookID = Books.bookID
            INNER JOIN Accounts
            ON MyBooks.my_booksID = Accounts.my_booksID
            WHERE Accounts.my_booksID = (SELECT my_booksID FROM Accounts WHERE email_address=?)""",(self.user_email,))
        user_books_author_fetch = c.fetchall()
        user_book_author_list = [x[0] for x in user_books_author_fetch]


        #Genres
        c.execute("""SELECT Books.genre
            FROM MyBooks
            INNER JOIN Books
            ON MyBooks.bookID = Books.bookID
            INNER JOIN Accounts
            ON MyBooks.my_booksID = Accounts.my_booksID
            WHERE Accounts.my_booksID = (SELECT my_booksID FROM Accounts WHERE email_address=?)""",(self.user_email,))
        user_books_genre_fetch = c.fetchall()
        user_book_genre_list = [x[0] for x in user_books_genre_fetch]

        #Location
        c.execute("""SELECT Books.location
            FROM MyBooks
            INNER JOIN Books
            ON MyBooks.bookID = Books.bookID
            INNER JOIN Accounts
            ON MyBooks.my_booksID = Accounts.my_booksID
            WHERE Accounts.my_booksID = (SELECT my_booksID FROM Accounts WHERE email_address=?)""",(self.user_email,))
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

    def _columns_searcher_bookID(self, *args):
        children = list(self._detached) + list(self.tree.get_children())
        self._detached = set()
        query_bookID = self.bookID_entry.get()

        self.search_bookID_tv(children, query_bookID)

    def _columns_searcher_title(self, *args):
        children = list(self._detached) + list(self.tree.get_children())
        self._detached = set()
        query_title = self.title_entry.get()

        self.search_title_tv(children, query_title)

    def _columns_searcher_author(self, *args):
        children = list(self._detached) + list(self.tree.get_children())
        self._detached = set()
        query_author = self.author_entry.get()

        self.search_author_tv(children, query_author)

    def _columns_searcher_genre(self, *args):
        children = list(self._detached) + list(self.tree.get_children())
        self._detached = set()
        query_genre = self.genre_var.get()

        self.search_genre_tv(children, query_genre)

    def _columns_searcher_location(self, *args):
        children = list(self._detached) + list(self.tree.get_children())
        self._detached = set()
        query_location = self.location_var.get()

        self.search_location_tv(children, query_location)

    def search_bookID_tv(self, children, query_bookID):
        i_r = -1

        for item_id in children:
            bookID_text = str(self.tree.item(item_id)['values'][0])

            if query_bookID in bookID_text:
                i_r += 1
                self.tree.reattach(item_id, '', i_r)

            else:
                self._detached.add(item_id)
                self.tree.detach(item_id)

    def search_title_tv(self, children, query_title):
        i_r = -1

        for item_id in children:
            title_text = self.tree.item(item_id)['values'][1]

            if query_title in title_text:
                i_r += 1
                self.tree.reattach(item_id, '', i_r)

            else:
                self._detached.add(item_id)
                self.tree.detach(item_id)

    def search_author_tv(self, children, query_author):
        i_r = -1

        for item_id in children:
            author_text = self.tree.item(item_id)['values'][2]

            if query_author in author_text:
                i_r += 1
                self.tree.reattach(item_id, '', i_r)

            else:
                self._detached.add(item_id)
                self.tree.detach(item_id)

    def search_genre_tv(self, children, query_genre):
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

    def search_location_tv(self, children, query_location):
        i_r = -1

        for item_id in children:
            location_text = self.tree.item(item_id)['values'][3]

            if query_location in location_text:
                i_r += 1
                self.tree.reattach(item_id, '', i_r)

            elif query_location == '-EMPTY-':
                self.tree.reattach(item_id, '', i_r)

            else:
                self._detached.add(item_id)
                self.tree.detach(item_id)


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
            ON MyBooks.my_booksID = Accounts.my_booksID
            WHERE Accounts.my_booksID = (SELECT my_booksID FROM Accounts WHERE email_address=?)""",(self.user_email,))
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
            ON MyBooks.my_booksID = Accounts.my_booksID
            WHERE Accounts.my_booksID = (SELECT my_booksID FROM Accounts WHERE email_address=?)""",(self.user_email,))
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


class Account():
    #USER ACCESS
    #Display logged in user information.
    def __init__(self, root, notebook, current_user_email):
        user_email= current_user_email

        account_page = tk.Frame(notebook)
        notebook.add(account_page, text='Account')

        header_frame = tk.Frame(account_page)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        header = tk.Label(header_frame, text='Account', font='System 30')
        header.pack(side=tk.TOP)

        # Account Details Frame
        details_container = tk.Frame(account_page, bg=bg)
        details_container.pack(side=tk.LEFT, anchor=tk.N)

        container_header = tk.Label(details_container, text='Account Details', font='System 18', bg=bg)
        container_header.pack(anchor=tk.W, padx=padx, pady=pady)


        
        #Change password Container
        self.change_password_container = tk.Frame(account_page, bg=bg)
        self.container_change_password_header = tk.Label(self.change_password_container, text='Change Password', font='System 18', bg=bg)
        



        #Change password email entry
        self.change_pw_email_container = tk.Frame(self.change_password_container, bg=bg)
        self.change_pw_email_label = tk.Label(self.change_pw_email_container, text='Email:',bg=bg)
        

        self.change_pw_email_var = tk.StringVar()
        self.change_pw_email_entry = ttk.Entry(self.change_pw_email_container, textvariable=self.change_pw_email_var)
        



        #Current password entry
        self.current_pw_container = tk.Frame(self.change_password_container, bg=bg)
        self.current_pw_label = tk.Label(self.current_pw_container, text='Current Password:',bg=bg)
        

        self.current_pw_var = tk.StringVar()
        self.current_pw_entry = ttk.Entry(self.current_pw_container, textvariable=self.current_pw_var, show='*')
        



        #New password entry
        self.new_pw_container = tk.Frame(self.change_password_container, bg=bg)
        self.new_pw_label = tk.Label(self.new_pw_container, text='New Password:',bg=bg)
        

        self.new_pw_var = tk.StringVar()
        self.new_pw_entry = ttk.Entry(self.new_pw_container, textvariable=self.new_pw_var, show='*')
        



        #New password confirmation entry
        self.new_pw_confirm_container = tk.Frame(self.change_password_container, bg=bg)
        self.new_pw_confirm_label = tk.Label(self.new_pw_confirm_container, text='Confirm New Password:',bg=bg)
        

        self.new_pw_confirm_var = tk.StringVar()
        self.new_pw_confirm_entry = ttk.Entry(self.new_pw_confirm_container, textvariable=self.new_pw_confirm_var, show='*')
        

        #Change password button
        self.change_password_button_container = tk.Frame(self.change_password_container, bg=bg)
        self.change_password_button = ttk.Button(self.change_password_button_container, text='Change Password', command=lambda:self.change_password())




        #Delete Account Container
        self.delete_account_container = tk.Frame(account_page, bg=bg)
        self.container_delete_account_header = tk.Label(self.delete_account_container, text='Delete Account', font='System 18', bg=bg)
        


        # Email Container
        self.delete_acc_email_container = tk.Frame(self.delete_account_container, bg=bg)
        self.delete_acc_email_label = tk.Label(self.delete_acc_email_container, text='Email:',bg=bg)
        

        self.delete_acc_pw_email_var = tk.StringVar()
        self.delete_acc_pw_email_entry = ttk.Entry(self.delete_acc_email_container, textvariable=self.delete_acc_pw_email_var)
        



        #Password entry
        self.pw_container = tk.Frame(self.delete_account_container, bg=bg)
        self.pw_label = tk.Label(self.pw_container, text='Password:',bg=bg)
        

        self.pw_var = tk.StringVar()
        self.pw_entry = ttk.Entry(self.pw_container, textvariable=self.pw_var)
        



        #New password entry
        self.confirm_pw_container = tk.Frame(self.delete_account_container, bg=bg)
        self.confirm_pw_label = tk.Label(self.confirm_pw_container, text='Confirm Password:',bg=bg)
        

        self.confirm_pw_var = tk.StringVar()
        self.confirm_pw_entry = ttk.Entry(self.confirm_pw_container, textvariable=self.confirm_pw_var, show='*')


        #Delete account button
        self.delete_account_button_container = tk.Frame(self.delete_account_container, bg=bg)
        self.delete_account_button = ttk.Button(self.delete_account_button_container, text='Delete Account', command=lambda:self.deletion_confirmation())



        




        email_container = tk.Frame(details_container, bg=bg)
        email_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        email_label = tk.Label(email_container, text='   Email:   {}'.format(user_email), padx=padx, pady=pady)
        email_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        change_password_label = tk.Label(details_container, text='Change Password?', cursor="hand2",
                                                bg=bg, fg='blue')
        change_password_label.pack(anchor=tk.W, padx=padx, pady=pady)
        change_password_label.bind("<Button-1>", lambda e: self.change_password_container_func())

        delete_account_label = tk.Label(details_container, text='Delete Account?', cursor="hand2",
                                                bg=bg, fg='orange red')
        delete_account_label.pack(anchor=tk.W, padx=padx, pady=pady)
        delete_account_label.bind("<Button-1>", lambda e: self.delete_account_container_func())

    def change_password(self, *args):
        change_password_confirmation = ms.askquestion('Change Password', 'Are you sure you want to change password?')
        if change_password_confirmation == 'yes':
            #Update password in database to fit the new password and its hash

            current_pw = self.current_pw_var.get()
            new_pw = self.new_pw_var.get()
            email_address = self.change_pw_email_var.get()

            #Check if the current password entered matches the one stored in the database

            #Hash the password to check against the database one
            db_current_pw_fetch = c.execute('SELECT password FROM Accounts WHERE email_address = ?', (email_address,))
            db_current_pw = c.fetchone()[0]

            #Password stored in database
            db_current_pw_encode = db_current_pw.encode('utf-8')

            #Password userhas just typed in, converted into bytes literal.
            bytes_current_pw = bytes(current_pw, 'utf-8')
            

            if bcrypt.checkpw(bytes_current_pw, db_current_pw_encode):
                #Encrypt+Salt New PW
                hashable_new_pw = bytes(new_pw, 'utf-8')
                hashed_new_pw = bcrypt.hashpw(hashable_new_pw, bcrypt.gensalt())

                #Convert into base64string
                db_hashed_pw = hashed_new_pw.decode("utf-8")

                db_new_pw_update = c.execute('UPDATE Accounts SET password=? WHERE email_address=?',(db_hashed_pw, email_address))
                conn.commit()
            else:
                ms.showerror('Error','Current password does not match.')

    def deletion_confirmation(self, *args):
        account_deletion_confirmation = ms.askquestion('Account Deletion', 'Are you sure you want to delete your account?\n\nYou will not be able to recover any information saved on this account.\nAll personal information associated to this account will be deleted permanently.')
        if account_deletion_confirmation == 'yes':
            #logic for deleting account goes here
            pass

    def change_password_container_func(self, *args):
        #If the user has pressed the button after the widgets were already packed, unpack them.
        if self.change_password_container.winfo_ismapped() == True:
            #May be able to just use a for loop that iterates over child widget using winfo_children().
            self.change_password_container.pack_forget()
            self.container_change_password_header.pack_forget()
            self.change_pw_email_container.pack_forget()
            self.change_pw_email_label.pack_forget()
            self.change_pw_email_entry.pack_forget()
            self.current_pw_container.pack_forget()
            self.current_pw_label.pack_forget()
            self.current_pw_entry.pack_forget()
            self.new_pw_container.pack_forget()
            self.new_pw_label.pack_forget()
            self.new_pw_entry.pack_forget()
            self.new_pw_confirm_container.pack_forget()
            self.new_pw_confirm_label.pack_forget()
            self.new_pw_confirm_entry.pack_forget()
            self.change_password_button_container.pack_forget()
            self.change_password_button.pack_forget()
        else:
            #Pack all the widgets upon the user pressing the button.
            self.change_password_container.pack(side=tk.LEFT, anchor=tk.N)
            self.container_change_password_header.pack(anchor=tk.W, padx=padx, pady=pady)
            self.change_pw_email_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)
            self.change_pw_email_label.pack(side=tk.LEFT, anchor=tk.W, fill=tk.X, padx=padx, pady=pady)
            self.change_pw_email_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)
            self.current_pw_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)
            self.current_pw_label.pack(side=tk.LEFT, anchor=tk.W, fill=tk.X, padx=padx, pady=pady)
            self.current_pw_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)
            self.new_pw_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)
            self.new_pw_label.pack(side=tk.LEFT, anchor=tk.W, fill=tk.X, padx=padx, pady=pady)
            self.new_pw_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)
            self.new_pw_confirm_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)
            self.new_pw_confirm_label.pack(side=tk.LEFT, anchor=tk.W, fill=tk.X, padx=padx, pady=pady)
            self.new_pw_confirm_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)
            self.change_password_button_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)
            self.change_password_button.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

    def delete_account_container_func(self, *args):
        #If the user has pressed the button after the widgets were already packed, unpack them.
        if self.delete_account_container.winfo_ismapped() == True:
            self.delete_account_container.pack_forget()
            self.container_delete_account_header.pack_forget()
            self.delete_acc_email_container.pack_forget()
            self.delete_acc_email_label.pack_forget()
            self.delete_acc_pw_email_entry.pack_forget()
            self.pw_container.pack_forget()
            self.pw_label.pack_forget()
            self.pw_entry.pack_forget()
            self.confirm_pw_container.pack_forget()
            self.confirm_pw_label.pack_forget()
            self.confirm_pw_entry.pack_forget()
            self.delete_account_button_container.pack_forget()
            self.delete_account_button.pack_forget()
        else:
            #Pack all the widgets to show the panel upon pressing the delete_account box in account details
            self.delete_account_container.pack(side=tk.LEFT, anchor=tk.N)
            self.container_delete_account_header.pack(anchor=tk.W, padx=padx, pady=pady)
            self.delete_acc_email_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)
            self.delete_acc_email_label.pack(side=tk.LEFT, anchor=tk.W, fill=tk.X, padx=padx, pady=pady)
            self.delete_acc_pw_email_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)
            self.pw_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)
            self.pw_label.pack(side=tk.LEFT, anchor=tk.W, fill=tk.X, padx=padx, pady=pady)
            self.pw_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)
            self.confirm_pw_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)
            self.confirm_pw_label.pack(side=tk.LEFT, anchor=tk.W, fill=tk.X, padx=padx, pady=pady)
            self.confirm_pw_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)
            self.delete_account_button_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)
            self.delete_account_button.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)
       

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

class ForgotPW():
    def __init__(self,parent, sign_in_notebook):
        self.sign_in_notebook = sign_in_notebook
        forgot_pw_page = tk.Frame(sign_in_notebook)
        sign_in_notebook.add(forgot_pw_page, text='Forgot Password?')

        main_frame = tk.Frame(forgot_pw_page, relief=tk.FLAT)
        main_frame.pack(fill=tk.BOTH, side=tk.TOP)

        main_label = tk.Label(main_frame, text='Library System v1.0')
        main_label.pack(fill=tk.X, anchor=tk.N)

        header_frame = tk.Frame(forgot_pw_page)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        header = tk.Label(header_frame, text='Forgot Password?', font='System 30')
        header.pack(side=tk.TOP)

        #Credentials Container
        credentials_container = tk.Frame(forgot_pw_page, bg=bg)
        credentials_container.pack(padx=padx, pady=pady)

        #Email Container
        email_container = tk.Frame(credentials_container, bg=bg)
        email_container.pack(expand=True)

        email_label = tk.Label(email_container, text='    Email:   ', bg=bg)
        email_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.user_email_var = tk.StringVar()
        self.user_email_var.set('')
        self.email_entry = ttk.Entry(email_container, textvariable=self.user_email_var,
                                                font='System 6')
        self.email_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)

        #Send Request Button Container
        button_container = tk.Frame(credentials_container, bg=bg)
        button_container.pack(expand=True)

        send_request_button = ttk.Button(button_container, text='Send Request', command=lambda:self.send_request())
        exit_button = ttk.Button(button_container, text='Exit', command=lambda:self.system_exit())

        send_request_button.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)
        exit_button.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)

        self.email_entry.bind("<Return>", self.send_request)

    def send_request(self, *args):
        #Accepted email standard internarionally.
        input_email = self.user_email_var.get()
        email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        #Check if the email address exists in the database
        email_address_fetch = c.execute("SELECT email_address FROM Accounts WHERE email_address=?",(self.user_email_var.get(),))
        email_address_list = email_address_fetch.fetchall()

        if len(email_address_list)==0:
            ms.showerror('Error','This account does not exist in our system.')
        elif (re.search(email_regex, input_email)):
            #Open TopLevel Window so the user can enter the emailed password, then the new password they want
            #1. TopLevel window and layout.
            self.forgotPassword = tk.Toplevel()

            #configurations
            self.forgotPassword.title("Account Verification")
            self.forgotPassword.option_add('*Font', 'System 12')
            self.forgotPassword.option_add('*Label.Font', 'System 12')
            self.forgotPassword.geometry('500x500')
            self.forgotPassword.resizable(False, False)


            main_frame = tk.Frame(self.forgotPassword, relief=tk.FLAT)
            main_frame.pack(fill=tk.BOTH, side=tk.TOP)

            main_label = tk.Label(main_frame, text='Library System v1.0')
            main_label.pack(fill=tk.X, anchor=tk.N)

            header_frame = tk.Frame(self.forgotPassword)
            header_frame.pack(fill=tk.X, side=tk.TOP)

            header = tk.Label(header_frame, text='Forgot Password', font='System 30')
            header.pack(side=tk.TOP)

            header_description = tk.Label(header_frame, text='A randomly generated password has been send to \n'+input_email+'\n Please enter the password into the "Generated Password" entry field below.', font='System 8')
            header_description.pack(side=tk.TOP)

            self.timer_text = tk.Label(header_frame, text='Time until another password can be resent.')
            self.timer_text.pack(side=tk.TOP)

            self.timer = tk.Label(header_frame, text='')
            self.timer.pack(side=tk.TOP)

            self.time_remaining = 0
            self.countdown(60)


            #Passwords Full Container
            passwords_container = tk.Frame(self.forgotPassword, bg=bg)
            passwords_container.pack(padx=padx, pady=pady)

            #Generated Password Entry Field Container
            generated_password_container = tk.Frame(passwords_container, bg=bg)
            generated_password_container.pack(expand=True)

            generated_password_label = tk.Label(generated_password_container, text='    Generated Password:   ', bg=bg)
            generated_password_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)


            self.generated_password_var = tk.StringVar()
            self.generated_password_var.set('')
            self.generated_password_entry = ttk.Entry(generated_password_container, textvariable=self.generated_password_var,font='System 6')
            self.generated_password_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)

            #Password Container
            new_password_container = tk.Frame(passwords_container, bg=bg)
            new_password_container.pack(expand=True)

            new_password_label = tk.Label(new_password_container, text=' New Password:', bg=bg)
            new_password_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

            self.new_password_var = tk.StringVar()
            self.new_password_var.set('')
            self.new_password_var.trace("w", self.password_strength)

            self.new_password_entry = ttk.Entry(new_password_container, textvariable=self.new_password_var,
                                                    font='System 6', show='*')
            self.new_password_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)

            #Confirm Password Container
            confirm_pw_container = tk.Frame(passwords_container, bg=bg)
            confirm_pw_container.pack(expand=True)

            confirm_pw_label = tk.Label(confirm_pw_container, text='Confirm\n New Password:', bg=bg)
            confirm_pw_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

            self.confirm_pw_var = tk.StringVar()
            self.confirm_pw_var.set('')
            self.confirm_pw_entry = ttk.Entry(confirm_pw_container, textvariable=self.confirm_pw_var,
                                                    font='System 6', show='*')
            self.confirm_pw_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)

            #Password Strength measure container
            self.password_strength_container_1 = tk.Frame(passwords_container, bg=bg)
            self.password_strength_container_1.pack(expand=True)

            self.password_strength_label_1 = tk.Label(self.password_strength_container_1, text='Password must be a minimum of 8 characters.',
                                                    bg=bg, fg='orange red')
            self.password_strength_label_1.pack(anchor=tk.E, side=tk.RIGHT, padx=padx, pady=pady)


            self.password_strength_container_2 = tk.Frame(passwords_container, bg=bg)
            self.password_strength_container_2.pack(expand=True)

            self.password_strength_label_2 = tk.Label(self.password_strength_container_2, text="""Besides letters, include at least a number or symbol shown below \n)([!@#$%^*-_+=|\\\{\}\[\]`¬;:@"'<>,./?]""",
                                                    bg=bg, fg='orange red')
            self.password_strength_label_2.pack(anchor=tk.E, side=tk.RIGHT, padx=padx, pady=pady)


            #Buttons Container
            button_container = tk.Frame(passwords_container, bg=bg)
            button_container.pack(expand=True)

            update_password_button = ttk.Button(button_container, text='Update Password', command=lambda:self.update_password())
            show_password_button = ttk.Button(button_container, text='Show Password', command=lambda:self.show_password())
            resend_password_button = ttk.Button(button_container, text='Resend Password', command=lambda:self.resend_password())

            update_password_button.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)
            show_password_button.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)
            resend_password_button.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


            self.generated_password_entry.bind("<Return>", self.update_password)

            #Randomly generate a password
            charset="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()"
            self.gen_random_password = ''.join([secrets.choice(charset) for _ in range(0, 10)])

            #Send the password to the email constructor.
            e = Email()
            service = e.get_service()
            message = e.create_forgot_password_message("from@gmail.com",input_email,"Books4All Forgot Password?", self.gen_random_password)
            e.send_message(service,"from@gmail.com",message)

        else:
            ms.showerror('Error','Invalid email address')

    def update_password(self):
        if self.gen_random_password == self.generated_password_var.get().strip():  
            if self.new_password_var.get() != self.confirm_pw_var.get():
                ms.showwarning('Warning','Your passwords do not match.')
            elif self.new_password_var.get() == '' or self.confirm_pw_var.get() == '':
                ms.showwarning('Warning', 'You left the password fields empty!')
            else:
                #Update the password in the database to this.
                #Encrypt+Salt New PW
                hashable_new_pw = bytes(self.new_password_var.get(), 'utf-8')
                hashed_new_pw = bcrypt.hashpw(hashable_new_pw, bcrypt.gensalt())

                #Convert into base64string
                db_hashed_pw = hashed_new_pw.decode("utf-8")

                db_new_pw_update = c.execute('UPDATE Accounts SET password=? WHERE email_address=?',(db_hashed_pw, self.user_email_var.get()))
                conn.commit()

                ms.showinfo('Success','Your password has been updated!')
                self.forgotPassword.destroy()

                #Switch tabs after registration
                login_index = self.sign_in_notebook.index(0)
                self.sign_in_notebook.select(login_index)

        else:
            ms.showerror('Error','The password that was sent did not match the password you entered.')


    def resend_password(self):
        if self.timer["text"] == "Ready to Resend Password!":
            #Randomly generate a password
            charset="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()"
            self.gen_random_password = ''.join([secrets.choice(charset) for _ in range(0, 10)])

            #Send the password to the email constructor.
            e = Email()
            service = e.get_service()
            message = e.create_forgot_password_message("from@gmail.com",self.user_email_var.get(),"Books4All Forgot Password?", self.gen_random_password)
            e.send_message(service,"from@gmail.com",message)
            ms.showinfo('Success','A new randomly generated password has been sent to the email address.')

            self.time_remaining = 0
            self.countdown(60)
        else:
            ms.showwarning('Warning','Please wait another '+self.timer["text"]+'seconds to resend a password.')

    def password_strength(self, *args):
        special_characters_regex = re.compile("""[!@#$%^*-_+=|\\\{\}\[\]`¬;:@"'<>,./?]()""")
        password_input = self.new_password_var.get()

        if len(password_input) >= 8:
            self.password_strength_container_1.pack_forget()
            if special_characters_regex.search(password_input) != None :
                self.password_strength_container_2.pack_forget()
            else:
                self.password_strength_container_2.pack(expand=True)

        elif len(password_input) < 8:
            self.password_strength_container_1.pack(expand=True)
            if special_characters_regex.search(password_input) != None :
                self.password_strength_container_2.pack_forget()
            else:
                self.password_strength_container_2.pack(expand=True)

    def show_password(self, *args):
        if self.new_password_entry["show"] == "*":
            self.new_password_entry["show"]=''
            self.confirm_pw_entry["show"]=''
        else:
            self.new_password_entry["show"]='*'
            self.confirm_pw_entry["show"]='*'

    def countdown(self, time_remaining = None):
        if time_remaining is not None:
            self.time_remaining = time_remaining

        if self.time_remaining <= 0:
            self.timer["text"]="Ready to Resend Password!"
        else:
            self.timer["text"]=("%d" % self.time_remaining)
            self.time_remaining = self.time_remaining - 1
            self.forgotPassword.after(1000, self.countdown)

    def system_exit(self):
        root.destroy()
        sys.exit()

class Register():
    def __init__(self, parent, sign_in_notebook):
        register_page = tk.Frame(sign_in_notebook)
        self.sign_in_notebook = sign_in_notebook
        self.sign_in_notebook.add(register_page, text='Register')

        main_frame = tk.Frame(register_page, relief=tk.FLAT)
        main_frame.pack(fill=tk.BOTH, side=tk.TOP)

        main_label = tk.Label(main_frame, text='Library System v1.0')
        main_label.pack(fill=tk.X, anchor=tk.N)

        header_frame = tk.Frame(register_page)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        header = tk.Label(header_frame, text='Register', font='System 30')
        header.pack(side=tk.TOP)

        #Register Container
        register_container = tk.Frame(register_page, bg=bg)
        register_container.pack(padx=padx, pady=pady)

        #Email Container
        email_container = tk.Frame(register_container, bg=bg)
        email_container.pack(expand=True)

        email_label = tk.Label(email_container, text='    Email:   ', bg=bg)
        email_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.user_email_var = tk.StringVar()
        self.user_email_var.set('')
        self.email_entry = ttk.Entry(email_container, textvariable=self.user_email_var,
                                                font='System 6')
        self.email_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)

        #Password Container
        password_container = tk.Frame(register_container, bg=bg)
        password_container.pack(expand=True)

        password_label = tk.Label(password_container, text=' Password:', bg=bg)
        password_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.user_password_var = tk.StringVar()
        self.user_password_var.set('')
        self.user_password_var.trace("w", self.password_strength)

        self.password_entry = ttk.Entry(password_container, textvariable=self.user_password_var,
                                                font='System 6', show='*')
        self.password_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)



        #Confirm Password Container
        confirm_pw_container = tk.Frame(register_container, bg=bg)
        confirm_pw_container.pack(expand=True)

        confirm_pw_label = tk.Label(confirm_pw_container, text='Confirm\n Password:', bg=bg)
        confirm_pw_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.confirm_pw_var = tk.StringVar()
        self.confirm_pw_var.set('')
        self.confirm_pw_entry = ttk.Entry(confirm_pw_container, textvariable=self.confirm_pw_var,
                                                font='System 6', show='*')
        self.confirm_pw_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)

        #Register Button Container
        button_container = tk.Frame(register_container, bg=bg)
        button_container.pack(expand=True)

        register_button = ttk.Button(button_container, text='Register', command=lambda:self.register())
        exit_button = ttk.Button(button_container, text='Exit', command=lambda:self.system_exit())
        show_password_button = ttk.Button(button_container, text='Show Password', command=lambda:self.show_password())

        register_button.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)
        exit_button.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)
        show_password_button.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)

        self.email_entry.bind("<Return>", self.register)
        self.password_entry.bind("<Return>", self.register)
        self.confirm_pw_entry.bind("<Return>", self.register)

        #Password Strength measure container
        self.password_strength_container_1 = tk.Frame(register_container, bg=bg)
        self.password_strength_container_1.pack(expand=True)

        self.password_strength_label_1 = tk.Label(self.password_strength_container_1, text='Password must be a minimum of 8 characters.',
                                                bg=bg, fg='orange red')
        self.password_strength_label_1.pack(anchor=tk.E, side=tk.RIGHT, padx=padx, pady=pady)


        self.password_strength_container_2 = tk.Frame(register_container, bg=bg)
        self.password_strength_container_2.pack(expand=True)

        self.password_strength_label_2 = tk.Label(self.password_strength_container_2, text="""Besides letters, include at least a number or symbol )([!@#$%^*-_+=|\\\{\}\[\]`¬;:@"'<>,./?]""",
                                                bg=bg, fg='orange red')
        self.password_strength_label_2.pack(anchor=tk.E, side=tk.RIGHT, padx=padx, pady=pady)

    def register(self, *args):
        # delete if statement and replace with database check for user's input credentials
        #validity checks for entry field + logic
        self.reg_email = self.user_email_var.get()

        #Accepted email standard internarionally.
        email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

        if (re.search(email_regex, self.reg_email)):
            reg_pw = self.user_password_var.get()
            reg_confirm_pw = self.confirm_pw_var.get()

            if reg_pw != reg_confirm_pw:
                ms.showwarning('Warning','Your passwords do not match.')
            elif reg_pw == '' or reg_pw == '':
                ms.showwarning('Warning', 'You left the password fields empty!')
            else:
                #Encrypt+Salt PWs
                hashable_pw = bytes(reg_pw, 'utf-8')
                hashed_pw = bcrypt.hashpw(hashable_pw, bcrypt.gensalt())

                #Convert into base64string
                self.db_hashed_pw = hashed_pw.decode("utf-8")

                #Send password to DB
                with sqlite3.connect('LibrarySystem.db') as db:
                    c = db.cursor()

                find_user = ('SELECT * FROM Accounts WHERE email_address = ?')
                c.execute(find_user,[(self.reg_email)])

                if c.fetchall():
                    ms.showerror('Error!','Email is already registered to an Account.')
                else:
                    #Will need to verify whether this email address is linked to the user.
                    #Steps to take in the following code:
                    # 1. Open a TopLevel window to prompt the user to enter a code into an entry box /DONE
                    # 2. Send the user an email with a randomly generated 6 digit code
                    # 3. Compare the 6 digit code the user entered to the one that was sent.
                    # 4. If they match, close the TopLevel, and follow on with the rest of the code below.
                    # 5. If the codes do not match, then an error will be prompted.
                    # 6. A 'Resend Code' button will be available on a cooldown (1min to stop spammers) that sends another code to the user.
                    #    Upon this code being sent, the previous code needs to be made invalid.

                    #1. TopLevel window and layout.
                    self.accountVerification = tk.Toplevel()

                    #configurations
                    self.accountVerification.title("Account Verification")
                    self.accountVerification.option_add('*Font', 'System 12')
                    self.accountVerification.option_add('*Label.Font', 'System 12')
                    self.accountVerification.geometry('500x500')
                    self.accountVerification.resizable(False, False)


                    main_frame = tk.Frame(self.accountVerification, relief=tk.FLAT)
                    main_frame.pack(fill=tk.BOTH, side=tk.TOP)

                    main_label = tk.Label(main_frame, text='Library System v1.0')
                    main_label.pack(fill=tk.X, anchor=tk.N)

                    header_frame = tk.Frame(self.accountVerification)
                    header_frame.pack(fill=tk.X, side=tk.TOP)

                    header = tk.Label(header_frame, text='Account Verification', font='System 30')
                    header.pack(side=tk.TOP)

                    header_description = tk.Label(header_frame, text='A 6 digit verification code has been sent to\n'+self.reg_email+'\n Please enter the 6 digit code into the entry field below.', font='System 8')
                    header_description.pack(side=tk.TOP)

                    self.timer = tk.Label(header_frame, text='')
                    self.timer.pack(side=tk.TOP)

                    self.time_remaining = 0
                    self.countdown(60)

                    #Codes Full Container
                    code_container = tk.Frame(self.accountVerification, bg=bg)
                    code_container.pack(padx=padx, pady=pady)

                    #Code Entry Field Container
                    verification_code_container = tk.Frame(code_container, bg=bg)
                    verification_code_container.pack(expand=True)

                    verification_code_label = tk.Label(verification_code_container, text='    Verification Code:   ', bg=bg)
                    verification_code_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

                    self.verification_code_reg = root.register(self.verification_code_validate)

                    self.verification_code_var = tk.StringVar()
                    self.verification_code_var.set('')
                    self.verification_code_entry = ttk.Entry(verification_code_container, textvariable=self.verification_code_var,
                                                            font='System 6', validate="key",
                                                            validatecommand=(self.verification_code_reg, "%P"))
                    self.verification_code_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)

                    #Buttons Container
                    button_container = tk.Frame(code_container, bg=bg)
                    button_container.pack(expand=True)

                    check_code_button = ttk.Button(button_container, text='Check Verification Code', command=lambda:self.check_code(self.verification_code_var.get()))
                    resend_code_button = ttk.Button(button_container, text='Resend Verification Code', command=lambda:self.resend_code(self.verification_code_var.get()))

                    check_code_button.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)
                    resend_code_button.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)
                    

                    self.verification_code_entry.bind("<Return>", self.check_code)


                    #2.1. Randomly generate a 6 digit code to be sent by email
                    self.email_verification_code = ''
                    i=0
                    while i<6:
                        random_integer = random.SystemRandom().randint(0,9)
                        i+=1
                        self.email_verification_code += str(random_integer)


                    #2.2. Send Email to user with the verification code.
                    #Call the Email class
                    e = Email()
                    service = e.get_service()
                    message = e.create_verification_message("from@gmail.com",self.reg_email,"Books4All Verification Code", self.email_verification_code)
                    e.send_message(service,"from@gmail.com",message)

        else:
            ms.showerror('Error', 'Invalid Email Address')

    def check_code(self, *args):
        #3. Compare the email code with the input code
        if self.verification_code_var.get() != self.email_verification_code:
            ms.showerror('Error','The verification code does not match the code sent.')
        else:
            ms.showinfo('Success','The verification code matches the code we sent!')
            self.accountVerification.destroy()

            with sqlite3.connect('LibrarySystem.db') as db:
                    c = db.cursor()
            #IF YOU DELETED THE DB, COMMENT THE 2 LINES BELOW, AND COPY THIS PART BELOW IT
            # insert = 'INSERT INTO Accounts(email_address,password,my_booksID,staff_mode,admin_mode) VALUES(?,?,?,?,?)'
            # c.execute(insert,[(self.reg_email),(self.db_hashed_pw),("1"),("1"),("1")])
            # db.commit()

            select_highest_val = c.execute('SELECT MAX(my_booksID) + 1 FROM Accounts').fetchall()
            highest_val = [x[0] for x in select_highest_val][0]

            insert = 'INSERT INTO Accounts(email_address,password,my_booksID) VALUES(?,?,?)'
            c.execute(insert,[(self.reg_email),(self.db_hashed_pw),(highest_val)])
            db.commit()

            ms.showinfo('Success!','Account Created!')

            #Switch tabs after registration
            login_index = self.sign_in_notebook.index(0)
            self.sign_in_notebook.select(login_index)

            #Remove details from register entry fields
            self.user_email_var.set('')
            self.user_password_var.set('')
            self.confirm_pw_var.set('')


    def resend_code(self, *args):
        if self.timer["text"] == "Ready to Resend Code!":
            self.email_verification_code = ''
            i=0
            while i<6:
                random_integer = random.SystemRandom().randint(0,9)
                i+=1
                self.email_verification_code += str(random_integer)

            #2.2. Send Email to user with the verification code.
            #Call the Email class
            e = Email()
            service = e.get_service()
            message = e.create_verification_message("from@gmail.com", self.reg_email, "Books4All Verification Code", self.email_verification_code)
            e.send_message(service, "from@gmail.com", message)

            self.time_remaining = 0
            self.countdown(60)
        else:
            ms.showwarning('Warning','Please wait another '+self.timer["text"]+'seconds to resend a code.')

    def countdown(self, time_remaining = None):
        if time_remaining is not None:
            self.time_remaining = time_remaining

        if self.time_remaining <= 0:
            self.timer["text"]="Ready to Resend Code!"
        else:
            self.timer["text"]=("%d" % self.time_remaining)
            self.time_remaining = self.time_remaining - 1
            self.accountVerification.after(1000, self.countdown)
        
    def verification_code_validate(self, verification_code_inp):
        if verification_code_inp.isdigit():
            if len(verification_code_inp) > 6:
                return False
            else:
                return True
        elif verification_code_inp is "":
            return True
        else:
            return False

    def password_strength(self, *args):
        special_characters_regex = re.compile("""[!@#$%^*-_+=|\\\{\}\[\]`¬;:@"'<>,./?]()""")
        password_input = self.user_password_var.get()

        if len(password_input) >= 8:
            self.password_strength_container_1.pack_forget()
            if special_characters_regex.search(password_input) != None :
                self.password_strength_container_2.pack_forget()
            else:
                self.password_strength_container_2.pack(expand=True)

        elif len(password_input) < 8:
            self.password_strength_container_1.pack(expand=True)
            if special_characters_regex.search(password_input) != None :
                self.password_strength_container_2.pack_forget()
            else:
                self.password_strength_container_2.pack(expand=True)

    def show_password(self, *args):
        if self.password_entry["show"] == "*":
            self.password_entry["show"]=''
            self.confirm_pw_entry["show"]=''
        else:
            self.password_entry["show"]='*'
            self.confirm_pw_entry["show"]='*'


    def system_exit(self):
        root.destroy()
        sys.exit()


class Email():
    def __init__(self):
        logging.basicConfig(
                        format="[%(levelname)s] %(message)s",
                        level=logging.INFO
                    )
    @staticmethod
    def get_service():
        """Gets an authorized Gmail API service instance.

        Returns:
            An authorized Gmail API service instance..
        """    

        # If modifying these scopes, delete the file token.pickle.
        SCOPES = [
            'https://www.googleapis.com/auth/gmail.readonly',
            'https://www.googleapis.com/auth/gmail.send',
        ]

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('gmail', 'v1', credentials=creds)
        return service

    @staticmethod
    def send_message(service, sender, message):
        try:
            sent_message = (service.users().messages().send(userId='me', body=message)
                .execute())
            logging.info('Message Id: %s', sent_message['id'])
            return sent_message
        except errors.HttpError as error:
            logging.error('An HTTP error occurred: %s', error)

    @staticmethod
    def create_verification_message(sender, to, subject, verification_code):
        """Create a verification message.

        Returns:
          An object containing a base64url encoded email object.
        """
        html = open("verification_email.html")

        soup = BeautifulSoup(html, features="lxml")
        html.close()
        target = soup.find(id='verification_code')
        target_result = soup.find(id='verification_code').find_all(text=True, recursive=False)
        target_text = str(target_result[0])

        for v in target:
            v.replace_with(v.replace(target_text,verification_code))

        with open("verification_email.html", "w") as file:
            file.write(str(soup))

        updated_html = open("verification_email.html")

        message = MIMEText(updated_html.read(), 'html')



        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        s = message.as_string()
        b = base64.urlsafe_b64encode(s.encode('utf-8'))
        return {'raw': b.decode('utf-8')}

    @staticmethod
    def create_forgot_password_message(sender, to, subject, gen_random_password):
        """Create a forgot password message for an email.
        Returns:
          An object containing a base64url encoded email object.
        """
        html = open("forgot_password_email.html")

        soup = BeautifulSoup(html, features="lxml")
        html.close()
        target = soup.find(id='random_password')
        target_result = soup.find(id='random_password').find_all(text=True, recursive=False)
        target_text = str(target_result[0])

        for v in target:
            v.replace_with(v.replace(target_text,gen_random_password))

        with open("forgot_password_email.html", "w") as file:
            file.write(str(soup))

        updated_html = open("forgot_password_email.html")

        message = MIMEText(updated_html.read(), 'html')

        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        s = message.as_string()
        b = base64.urlsafe_b64encode(s.encode('utf-8'))
        return {'raw': b.decode('utf-8')}

class Login():
    def __init__(self, parent, sign_in_notebook):
        self.parent = parent
        login_page = tk.Frame(sign_in_notebook)
        sign_in_notebook.add(login_page, text='Login')

        main_frame = tk.Frame(login_page, relief=tk.FLAT)
        main_frame.pack(fill=tk.BOTH, side=tk.TOP)

        main_label = tk.Label(main_frame, text='Library System v1.0')
        main_label.pack(fill=tk.X, anchor=tk.N)

        header_frame = tk.Frame(login_page)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        header = tk.Label(header_frame, text='Login', font='System 30')
        header.pack(side=tk.TOP)

        #Login Container
        login_container = tk.Frame(login_page, bg=bg)
        login_container.pack(padx=padx, pady=pady)

        #Email Container
        email_container = tk.Frame(login_container, bg=bg)
        email_container.pack(expand=True)

        email_label = tk.Label(email_container, text='    Email:   ', bg=bg)
        email_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.user_email_var = tk.StringVar()
        self.user_email_var.set('')
        self.email_entry = ttk.Entry(email_container, textvariable=self.user_email_var, font='System 6',)
        self.email_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)
        self.email_entry.focus()


        #Password Container
        password_container = tk.Frame(login_container, bg=bg)
        password_container.pack(expand=True)

        password_label = tk.Label(password_container, text=' Password:', bg=bg)
        password_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.user_password_var = tk.StringVar()
        self.user_password_var.set('')
        self.password_entry = ttk.Entry(password_container, textvariable=self.user_password_var,
                                                font='System 6', show='*')
        self.password_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)

        #Login Button Container
        button_container = tk.Frame(login_container, bg=bg)
        button_container.pack(expand=True)

        login_button = ttk.Button(button_container, text='Login', command=lambda:self.login())
        exit_button = ttk.Button(button_container, text='Exit', command=lambda:self.system_exit())

        login_button.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)
        exit_button.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)

        self.email_entry.bind("<Return>", self.login)
        self.password_entry.bind("<Return>", self.login)

    def login(self, *args):
        login_email = self.user_email_var.get()
        login_password = self.user_password_var.get()

        # CHECK DETAILS AGAINST DATABASE DETAILS
        if login_password == '' and login_email  == '':
             ms.showwarning('Warning','Enter your email address and password')
        else:

            pass_hashed_fetch = c.execute('SELECT password FROM Accounts WHERE email_address = ?', (login_email,))
            pass_hashed = c.fetchone()[0]

            pass_hashed_encode = pass_hashed.encode('utf-8')

            bytes_login_password = bytes(login_password, 'utf-8')
            

            if bcrypt.checkpw(bytes_login_password, pass_hashed_encode):
                ms.showinfo('Success', 'Successfully Logged in!')
                for child in self.parent.winfo_children():
                    child.destroy()

                MainApplication(self.parent, login_email)

                self.user_email_var.set('')
                self.user_password_var.set('')
            else:
                ms.showerror('Error','Incorrect password/email')


    def system_exit(self):
        root.destroy()
        sys.exit()


class SignIn():
    def __init__(self, parent):
        self.parent = parent
        sign_in_notebook = ttk.Notebook(self.parent)
        sign_in_notebook.pack(expand=True, fill=tk.BOTH)

        login = Login(parent, sign_in_notebook)
        register = Register(parent, sign_in_notebook)
        forgot_pw = ForgotPW(parent, sign_in_notebook)

        

class MainApplication():
    def __init__(self, parent, email):
        # Declare variables
        self.parent = parent
        self.email = email


        parent.configure(bg='gray15')
        parent.title("Library System v1.0")
        parent.option_add('*Font', 'System 12')
        parent.option_add('*Label.Font', 'System 12')
        parent.geometry(geometry)


        #Global Header
        global_frame = tk.Frame(parent, relief=tk.FLAT)
        global_frame.pack(fill=tk.BOTH, side=tk.TOP)

        global_label = tk.Label(global_frame, text='Library System v1.0')
        global_label.pack(fill=tk.X, anchor=tk.N)

        #Logout button
        logout_button = ttk.Button(global_frame, text='Logout', command=self.logout)
        logout_button.pack(side=tk.RIGHT)


        self.main_notebook = ttk.Notebook(parent)
        self.main_notebook.pack(expand=True, fill=tk.BOTH)


        #Instantiate Classes (HP = Home Page, MBP = My Books Page, etc...)
        self.HP = Home(self.parent, self.main_notebook)
        self.AP = Account(self.parent, self.main_notebook, self.email)
        self.MBP = MyBooks(self.parent, self.main_notebook, self.email)
        self.LP = Library(self.parent, self.main_notebook)

        # Needs 'Staff' powers to see this page, put behind an if statement.
        #check if the user has staff privileges
        staff_mode_check = c.execute('SELECT staff_mode FROM Accounts WHERE email_address=?',(email,)).fetchall()
        staff_mode = [x[0] for x in staff_mode_check][0]

        if staff_mode == 1:
            self.BDP = BookDatabase(self.parent, self.main_notebook, self.email)

        admin_mode_check = c.execute('SELECT admin_mode FROM Accounts WHERE email_address=?',(email,)).fetchall()
        admin_mode = [x[0] for x in staff_mode_check][0]

        if admin_mode == 1:
            self.AP = Admin(self.parent, self.main_notebook, self.email)

        self.OP = Options(self.parent, self.main_notebook)

    def logout(self):
        logout_confirmation = ms.askquestion('Logout', 'Are you sure you want to logout?', icon='warning')
        if logout_confirmation == 'yes':
            for child in self.parent.winfo_children():
                child.destroy()
            SignIn(self.parent)







if __name__ == "__main__":
    root = tk.Tk()

    rlp = SignIn(root)

    root.mainloop()
