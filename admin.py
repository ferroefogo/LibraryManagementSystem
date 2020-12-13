#Admin Page
import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox as ms
import bcrypt
import sys
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import re

conn = sqlite3.connect('LibrarySystem.db')
c = conn.cursor()

width=225
padx=8
pady=5

geometry = '1500x1500'
bg='gray90'
font='System 18'







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
        select_highest_userID = c.execute("SELECT MAX(user_id)+1 FROM Accounts").fetchall()
        highest_userID = [x[0] for x in select_highest_userID][0]
        self.userID_var.set(highest_userID)

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

        self.password_entry = ttk.Entry(self.password_container, textvariable=self.password_var, show='*')
        self.password_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Confirm Password Entry Field
        self.confirm_password_container = tk.Frame(add_account_container, bg=bg)
        self.confirm_password_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        confirm_password_label = tk.Label(self.confirm_password_container, text='Confirm Password: ', bg=bg)
        confirm_password_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.confirm_password_var = tk.StringVar()

        self.confirm_password_entry = ttk.Entry(self.confirm_password_container, textvariable=self.confirm_password_var, show='*')
        self.confirm_password_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)

        
        #Staff Mode Box
        add_mode_container = tk.Frame(add_account_container, bg=bg)
        add_mode_container.pack(anchor=tk.W, fill=tk.X, side=tk.TOP)

        add_mode_label = tk.Label(add_mode_container, text='Staff Mode: ', bg=bg)
        add_mode_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.add_staff_mode_var = tk.IntVar()

        add_staff_mode_checkbtn = ttk.Checkbutton(add_mode_container, variable=self.add_staff_mode_var)
        add_staff_mode_checkbtn.pack(side=tk.LEFT, anchor=tk.E, padx=padx, pady=pady)


        #Admin Mode Box
        add_admin_mode_label = tk.Label(add_mode_container, text='Admin Mode: ', bg=bg)
        add_admin_mode_label.pack(side=tk.LEFT, anchor=tk.E, padx=padx, pady=pady)

        self.add_admin_mode_var = tk.IntVar()

        add_admin_mode_checkbtn = ttk.Checkbutton(add_mode_container, variable=self.add_admin_mode_var)
        add_admin_mode_checkbtn.pack(side=tk.LEFT, anchor=tk.E, padx=padx, pady=pady)


        #Add Account
        add_account_button_container = tk.Frame(add_account_container, bg=bg)
        add_account_button_container.pack(anchor=tk.W, fill=tk.X, expand=True)


        add_account_btn = ttk.Button(add_account_button_container)
        add_account_btn.config(text='    Add Account    ', command=self.add_account)
        add_account_btn.pack(side=tk.RIGHT, anchor=tk.W, padx=padx, pady=pady)



        #Update Existing Account
        #Allows an admin to update the permissions of a staff/user account.
        update_account_header = tk.Label(add_account_container, text='Update Account', font='System 18', bg=bg)
        update_account_header.pack(anchor=tk.W, padx=padx, pady=pady)

        #UserID Entry Field
        self.update_account_userID_container = tk.Frame(add_account_container, bg=bg)
        self.update_account_userID_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        update_userID_label = tk.Label(self.update_account_userID_container, text='User ID: ', bg=bg)
        update_userID_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.update_userID_var = tk.IntVar()

        self.update_userID_var = ttk.Entry(self.update_account_userID_container)
        self.update_userID_var.config(textvariable=self.update_userID_var)
        self.update_userID_var.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Email Address Entry Field
        self.update_account_email_container = tk.Frame(add_account_container, bg=bg)
        self.update_account_email_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        update_email_label = tk.Label(self.update_account_email_container, text='Email Address: ', bg=bg)
        update_email_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.update_email_var = tk.StringVar()

        self.update_email_entry = ttk.Entry(self.update_account_email_container, textvariable=self.update_email_var)
        self.update_email_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)


        #Update staff mode frame
        update_mode_container = tk.Frame(add_account_container, bg=bg)
        update_mode_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        update_staff_mode_label = tk.Label(update_mode_container, text='Staff Mode: ', bg=bg)
        update_staff_mode_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.update_staff_mode_var = tk.IntVar()

        update_staff_mode_checkbtn = ttk.Checkbutton(update_mode_container, variable=self.update_staff_mode_var)
        update_staff_mode_checkbtn.pack(side=tk.LEFT, anchor=tk.E, padx=padx, pady=pady)


        #Admin Mode Box
        update_admin_mode_label = tk.Label(update_mode_container, text='Admin Mode: ', bg=bg)
        update_admin_mode_label.pack(side=tk.LEFT, anchor=tk.E, padx=padx, pady=pady)

        self.update_admin_mode_var = tk.IntVar()

        update_admin_mode_checkbtn = ttk.Checkbutton(update_mode_container, variable=self.update_admin_mode_var)
        update_admin_mode_checkbtn.pack(side=tk.LEFT, anchor=tk.E, padx=padx, pady=pady)


        #Update Account Button
        update_account_button_container = tk.Frame(add_account_container, bg=bg)
        update_account_button_container.pack(anchor=tk.W, fill=tk.X, expand=True)

        update_account_btn = ttk.Button(update_account_button_container)
        update_account_btn.config(text='    Update Account    ', command=self.update_account)
        update_account_btn.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)



        #Remove Account
        remove_account_container = tk.Frame(admin_page, bg=bg)
        remove_account_container.pack(side=tk.LEFT, anchor=tk.N, padx=padx, pady=pady)

        remove_account_header = tk.Label(remove_account_container, text='Remove Account', font='System 18', bg=bg)
        remove_account_header.pack(anchor=tk.W, padx=padx, pady=pady)

        #User ID Field
        self.remove_userID_container = tk.Frame(remove_account_container, bg=bg)
        self.remove_userID_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        remove_userID_label = tk.Label(self.remove_userID_container, text='User ID: ', bg=bg)
        remove_userID_label.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)

        self.remove_userID_var = tk.IntVar()
        self.remove_userID_var.set('')

        self.remove_userID_entry = ttk.Entry(self.remove_userID_container)
        self.remove_userID_entry.config(textvariable=self.remove_userID_var)
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


        #Send Email Alert
        #Allows an admin to send email alerts to those whose return date is nearby (within 3 days of return).
        alert_container = tk.Frame(admin_page, bg=bg)
        alert_container.pack(side=tk.LEFT, anchor=tk.N, padx=padx, pady=pady)

        alert_header = tk.Label(alert_container, text='Returns Reminder Manual Email', font='System 18', bg=bg)
        alert_header.pack(anchor=tk.W, padx=padx, pady=pady)

        alert_desc = tk.Label(alert_container, text='Sends an email alert to all users whose book is\n within three days of needing to be returned.', font='System 10', bg=bg)
        alert_desc.pack(anchor=tk.W, padx=padx, pady=pady)

        #Send Email Alert Container
        alert_email_button_container = tk.Frame(alert_container, bg=bg)
        alert_email_button_container.pack(anchor=tk.W, fill=tk.X, expand=True)

        alert_btn = ttk.Button(alert_email_button_container)
        alert_btn.config(text='    Alert    ', command=self.send_alert)
        alert_btn.pack(side=tk.RIGHT, anchor=tk.W, padx=padx, pady=pady)


        #Analytical Information
        analytics_container = tk.Frame(admin_page, bg=bg)
        analytics_container.pack(side=tk.LEFT, anchor=tk.N, padx=padx, pady=pady)

        analytics_header = tk.Label(analytics_container, text='Analytics', font='System 18')
        analytics_header.pack(anchor=tk.W, padx=padx, pady=pady, side=tk.TOP)


        #Number of total users
        fetch_number_users = c.execute("SELECT * FROM Accounts").fetchall()
        number_users = len([x[0] for x in fetch_number_users])

        number_users_frame = tk.Frame(analytics_container)
        number_users_frame.pack(padx=padx, pady=pady, side=tk.TOP, anchor=tk.N)

        number_users_label = tk.Label(number_users_frame, text='Total of All Users:%d' % number_users)
        number_users_label.pack(side=tk.LEFT, anchor=tk.N)


        #Number of total patron accounts
        fetch_number_patrons = c.execute("SELECT * FROM Accounts WHERE staff_mode=0 AND admin_mode=0").fetchall()
        number_patrons = len([x[0] for x in fetch_number_patrons])

        number_patrons_frame = tk.Frame(analytics_container)
        number_patrons_frame.pack(padx=padx, pady=pady, side=tk.TOP, anchor=tk.N)

        number_patrons_label = tk.Label(number_patrons_frame, text='Number of Patrons:%d' % number_patrons)
        number_patrons_label.pack(side=tk.LEFT, anchor=tk.N)


        #Number of total staff accounts
        fetch_number_staff = c.execute("SELECT * FROM Accounts WHERE staff_mode=1 AND admin_mode=0").fetchall()
        number_staff = len([x[0] for x in fetch_number_staff])

        number_staff_frame = tk.Frame(analytics_container)
        number_staff_frame.pack(padx=padx, pady=pady, side=tk.TOP, anchor=tk.N)

        number_staff_label = tk.Label(number_staff_frame, text='Number of Staff:%d' % number_staff)
        number_staff_label.pack(side=tk.LEFT, anchor=tk.N)


        #Number of total admin accounts
        fetch_number_admins = c.execute("SELECT * FROM Accounts WHERE staff_mode=1 AND admin_mode=1").fetchall()
        number_admins = len([x[0] for x in fetch_number_admins])

        number_admins_frame = tk.Frame(analytics_container)
        number_admins_frame.pack(padx=padx, pady=pady, side=tk.TOP, anchor=tk.N)

        number_admins_label = tk.Label(number_admins_frame, text='Number of Admins:%d' % number_admins)
        number_admins_label.pack(side=tk.LEFT, anchor=tk.N)




        #Total book tally
        fetch_number_books = c.execute("SELECT * FROM Books").fetchall()
        number_books = len([x[0] for x in fetch_number_books])

        number_books_frame = tk.Frame(analytics_container)
        number_books_frame.pack(padx=padx, pady=pady, side=tk.TOP, anchor=tk.N)

        number_books_label = tk.Label(number_books_frame, text='Number of books:%d' % number_books)
        number_books_label.pack(side=tk.LEFT, anchor=tk.N)


        #Total issued book tally
        fetch_number_issued_books = c.execute("SELECT * FROM Books WHERE issued=1").fetchall()
        number_issued_books = len([x[0] for x in fetch_number_issued_books])

        number_issued_books_frame = tk.Frame(analytics_container)
        number_issued_books_frame.pack(padx=padx, pady=pady, side=tk.TOP, anchor=tk.N)

        number_issued_books_label = tk.Label(number_issued_books_frame, text='Number of issued books:%d' % number_issued_books)
        number_issued_books_label.pack(side=tk.LEFT, anchor=tk.N)


        #Total non-issued book tally
        fetch_number_non_issued_books = c.execute("SELECT * FROM Books WHERE issued=0").fetchall()
        number_non_issued_books = len([x[0] for x in fetch_number_non_issued_books])

        number_non_issued_books_frame = tk.Frame(analytics_container)
        number_non_issued_books_frame.pack(padx=padx, pady=pady, side=tk.TOP, anchor=tk.N)

        number_non_issued_books_label = tk.Label(number_non_issued_books_frame, text='Number of non-issued books:%d' % number_non_issued_books)
        number_non_issued_books_label.pack(side=tk.LEFT, anchor=tk.N)



        # #Average Number of days before return
        # fetch_issue_dates = c.execute("SELECT date_issued FROM MyBooks").fetchall()
        # issue_dates_list = [x[0] for x in fetch_issue_dates]

        # fetch_actual_return_dates = c.execute("SELECT actual_return_date FROM MyBooks").fetchall()
        # actual_dates_list = [x[0] for x in fetch_actual_return_dates]

        # day_difference_list = []

        # print(issue_dates_list)
        # for i in len(issue_dates_list):
        #     if actual_dates_list[i] != '':
        #         day_difference_list.append(actual_dates_list[i] - issue_dates_list[i])



       
        #Average number of books issued out on a single day over the past week
        week_ago = (datetime.today() - timedelta(days=7)).date()
        try:
            for j in range(7):
                date_issued = week_ago + timedelta(days=j)
                date_issued_string = date_issued.strftime('%Y-%m-%d')
                fetch_issued_books_past_week = c.execute("SELECT bookID FROM MyBooks WHERE date_issued=?",(date_issued,))
                issued_books_past_week = [x[0] for x in fetch_issued_books_past_week]

                if date_issued_string == week_ago.strftime("%Y-%m-%d"):
                    number_books_issued_7days_ago = len(issued_books_past_week)
                    

                elif date_issued_string == (week_ago + timedelta(days=1)).strftime("%Y-%m-%d"):
                    number_books_issued_6days_ago = len(issued_books_past_week)
                    

                elif date_issued_string == (week_ago + timedelta(days=2)).strftime("%Y-%m-%d"):
                    number_books_issued_5days_ago = len(issued_books_past_week)
                    

                elif date_issued_string == (week_ago + timedelta(days=3)).strftime("%Y-%m-%d"):
                    number_books_issued_4days_ago = len(issued_books_past_week)
                    

                elif date_issued_string == (week_ago + timedelta(days=4)).strftime("%Y-%m-%d"):
                    number_books_issued_3days_ago = len(issued_books_past_week)
                    

                elif date_issued_string == (week_ago + timedelta(days=5)).strftime("%Y-%m-%d"):
                    number_books_issued_2days_ago = len(issued_books_past_week)
                    

                elif date_issued_string == (week_ago + timedelta(days=6)).strftime("%Y-%m-%d"):
                    number_books_issued_1days_ago = len(issued_books_past_week)
                    

            mean_avg = (number_books_issued_7days_ago + number_books_issued_6days_ago + number_books_issued_5days_ago + number_books_issued_4days_ago + number_books_issued_3days_ago + number_books_issued_2days_ago + number_books_issued_1days_ago)/7
            #Tkinter display output here
        except Exception:
            ms.showwarning('Graph Warning','Not enough data to populate graph.')


        self.tree_ids = []
        # Library TreeView Book Database Frame
        tree_container = tk.Frame(admin_page, bg=bg)
        tree_container.pack(side=tk.BOTTOM, anchor=tk.N, padx=padx, pady=pady)

        tree_header = tk.Label(tree_container, text='Database', font='System 18', bg=bg)
        tree_header.pack(padx=padx, pady=pady)

        #Set up TreeView table
        self.columns = ('User ID','Email Address', 'Staff Mode', 'Admin Mode', 'Issued BookIDs', 'Earliest Return Date')
        self.tree = ttk.Treeview(tree_container, columns=self.columns, show='headings') #create tree
        self.tree.heading("User ID", text='User ID')
        self.tree.heading("Email Address", text='Email Address')
        self.tree.heading("Staff Mode", text='Staff Mode')
        self.tree.heading("Admin Mode", text='Admin Mode')
        self.tree.heading("Issued BookIDs", text='Issued BookIDs')
        self.tree.heading("Earliest Return Date", text='Earliest Return Date')

        self.tree.column("User ID", width=50, anchor=tk.CENTER)
        self.tree.column("Email Address", width=width, anchor=tk.CENTER)
        self.tree.column("Staff Mode", width=80, anchor=tk.CENTER)
        self.tree.column("Admin Mode", width=80, anchor=tk.CENTER)
        self.tree.column("Issued BookIDs", width=width, anchor=tk.CENTER)
        self.tree.column("Earliest Return Date", width=width, anchor=tk.CENTER)

        #User IDs
        c.execute("SELECT user_id FROM Accounts")
        userIDs_fetch = c.fetchall()
        userID_list = [x[0] for x in userIDs_fetch]

        #Email addresses
        c.execute("SELECT email_address FROM Accounts")
        email_fetch = c.fetchall()
        email_list = [x[0] for x in email_fetch]

        #staff mode
        c.execute("SELECT staff_mode FROM Accounts")
        staff_fetch = c.fetchall()
        staff_list = [x[0] for x in staff_fetch]

        #admin mode
        c.execute("SELECT admin_mode FROM Accounts")
        admin_fetch = c.fetchall()
        admin_list = [x[0] for x in admin_fetch]


        for k in self.tree.get_children():
            self.tree.delete(k)

        for i in range(len(userID_list)):
            #issued_bookIDs
            c.execute("SELECT bookID FROM MyBooks WHERE user_id=?",(userID_list[i],))
            issued_bookIDs_fetch = c.fetchall()
            issued_bookIDs_list = [x[0] for x in issued_bookIDs_fetch]

            for x in range(len(issued_bookIDs_list)):
                issued_book_list_string = ','.join(map(str, issued_bookIDs_list)) 

            #earliest return date
            c.execute("SELECT return_date FROM MyBooks WHERE user_id=?",(userID_list[i],))
            return_date_fetch = c.fetchall()
            return_date_list = [x[0] for x in return_date_fetch]

            #convert the return_date_list from a list of strins to a list of dates
            dates_list = [datetime.strptime(date, '%Y-%m-%d').date() for date in return_date_list]

            try:
                earliest_date = str(min(dates_list))
            except ValueError:
                pass
            if len(issued_bookIDs_list)==0 or len(return_date_list)==0:
                self.tree_ids.append(self.tree.insert("", "end", values=(userID_list[i], email_list[i], staff_list[i], admin_list[i],'N/A','N/A')))
            else:
                self.tree_ids.append(self.tree.insert("", "end", values=(userID_list[i], email_list[i], staff_list[i], admin_list[i], issued_bookIDs_list, earliest_date)))
        self.tree.pack()







        #Analytical graphs will be created using numpy or something alike. This will be a great opportunity to use quicksort to sort a table of data values for the user.
        #There will be buttons that open TopLevels that show the information regarding its topic accordingly.

        #Types of data we could include here:
        #   - Number of user accounts
        #   - Number of staff accounts
        #   - Number of admin accounts
        #   - Total book tally
        #   - Total issued book tally
        #   - Total Non-Issued book tally
        #   - Average number of days before return
        #   - Average number of books issued out on a single day over the past week
        #   - Genre Popularity (numpy bar chart required).

    def send_alert(self):
        # Fetch all the accounts that are within 3 days of needing to return their book
        with sqlite3.connect('LibrarySystem.db') as db:
            c = db.cursor()

        db_return_fetch = c.execute("SELECT user_id, bookID, return_date FROM MyBooks").fetchall()

        #Convert the return dates returned into datetime objects
        for parameter in db_return_fetch:
            date = parameter[2]
            datetime_conversion = datetime.strptime(date, '%Y-%m-%d').date()

            within_three_days = (datetime.today() + timedelta(days=3)).date()

            if within_three_days > datetime_conversion:
                #If we're within three days of the return

                #Identify the bookID behind the return date
                target_bookID = parameter[1]
                target_userID = parameter[0]

                #Fetchall of that books information.
                db_title_fetch = c.execute("SELECT title FROM Books WHERE bookID=?",(target_bookID,)).fetchall()
                db_title = [x[0] for x in db_title_fetch][0]

                db_author_fetch = c.execute("SELECT author FROM Books WHERE bookID=?",(target_bookID,)).fetchall()
                db_author = [x[0] for x in db_author_fetch][0]

                db_genre_fetch = c.execute("SELECT genre FROM Books WHERE bookID=?",(target_bookID,)).fetchall()
                db_genre = [x[0] for x in db_genre_fetch][0]

                db_issue_date_fetch = c.execute("SELECT date_issued FROM MyBooks WHERE bookID=?",(target_bookID,)).fetchall()
                db_issue_date = [x[0] for x in db_issue_date_fetch][0]

                db_expected_return_date_fetch = c.execute("SELECT return_date FROM MyBooks WHERE bookID=?",(target_bookID,)).fetchall()
                db_expected_return_date = [x[0] for x in db_expected_return_date_fetch][0]

                db_target_email_address = c.execute("SELECT email_address FROM Accounts WHERE user_id=(SELECT user_id FROM MyBooks WHERE bookID=?)",(target_bookID,)).fetchall()
                db_target_email_address = [x[0] for x in db_target_email_address][0]


                #Email user
                e = Email()
                service = e.get_service()
                message = e.create_reminder_message("from@gmail.com", db_target_email_address, "Books4All Return Reminder", db_title, db_author, db_genre, db_issue_date, db_expected_return_date)
                e.send_message(service, "from@gmail.com", message)

                
            elif within_three_days == datetime_conversion:
                #We are dead on three days of the return

                #Identify the bookID behind the return date
                target_bookID = parameter[1]
                target_userID = parameter[0]

                #Fetchall of that books information.
                db_title_fetch = c.execute("SELECT title FROM Books WHERE bookID=?",(target_bookID,)).fetchall()
                db_title = [x[0] for x in db_title_fetch][0]

                db_author_fetch = c.execute("SELECT author FROM Books WHERE bookID=?",(target_bookID,)).fetchall()
                db_author = [x[0] for x in db_author_fetch][0]

                db_genre_fetch = c.execute("SELECT genre FROM Books WHERE bookID=?",(target_bookID,)).fetchall()
                db_genre = [x[0] for x in db_genre_fetch][0]

                db_issue_date_fetch = c.execute("SELECT date_issued FROM MyBooks WHERE bookID=?",(target_bookID,)).fetchall()
                db_issue_date = [x[0] for x in db_issue_date_fetch][0]

                db_expected_return_date_fetch = c.execute("SELECT return_date FROM MyBooks WHERE bookID=?",(target_bookID,)).fetchall()
                db_expected_return_date = [x[0] for x in db_expected_return_date_fetch][0]

                db_target_email_address = c.execute("SELECT email_address FROM Accounts WHERE user_id=(SELECT user_id FROM MyBooks WHERE bookID=?)",(target_bookID,)).fetchall()
                db_target_email_address = [x[0] for x in db_target_email_address][0]


                #Email user
                e = Email()
                service = e.get_service()
                message = e.create_reminder_message("from@gmail.com", db_target_email_address, "Books4All Return Reminder", db_title, db_author, db_genre, db_issue_date, db_expected_return_date)
                e.send_message(service, "from@gmail.com", message)
            else:
                #Return date is not within allocated time to be emailed.
                ms.showwarning('Warning','No books within reminder limit!')
        

    def add_account(self):
        add_email = self.email_var.get()
        add_staff_mode = self.add_staff_mode_var.get()
        add_admin_mode = self.add_admin_mode_var.get()

        email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if (re.search(email_regex, add_email)):
            #Continue process
            add_password = self.password_var.get()
            add_confirm_password = self.confirm_password_var.get()

            if add_password != add_confirm_password:
                ms.showwarning('Warning','Your passwords do not match.')
            elif add_password == '' or add_confirm_password == '':
                ms.showwarning('Warning', 'You left the password fields empty!')
            else:
                #Encrypt+Salt PWs
                hashable_pw = bytes(add_password, 'utf-8')
                hashed_pw = bcrypt.hashpw(hashable_pw, bcrypt.gensalt())

                #Convert into base64string
                self.db_hashed_pw = hashed_pw.decode("utf-8")

                #Send password to DB
                with sqlite3.connect('LibrarySystem.db') as db:
                    c = db.cursor()

                find_user = ('SELECT * FROM Accounts WHERE email_address = ?')
                c.execute(find_user,[(add_email)])

                if c.fetchall():
                    ms.showerror('Error!','Email is already registered to an Account.')
                else:
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

                    header_description = tk.Label(header_frame, text='A 6 digit verification code has been sent to\n'+add_email+'\n Please enter the 6 digit code into the entry field below.', font='System 8')
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
                    message = e.create_verification_message("from@gmail.com",add_email,"Books4All Re", self.email_verification_code)
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

            select_highest_val = c.execute('SELECT MAX(user_id) + 1 FROM Accounts').fetchall()
            highest_val = [x[0] for x in select_highest_val][0]

            insert = 'INSERT INTO Accounts(email_address,password,user_id,staff_mode,admin_mode) VALUES(?,?,?,?,?)'
            c.execute(insert,[(self.email_var.get()),(self.db_hashed_pw),(highest_val),(self.add_staff_mode_var.get()),(self.add_admin_mode_var.get())])
            db.commit()

            #User IDs
            c.execute("SELECT user_id FROM Accounts")
            userIDs_fetch = c.fetchall()
            userID_list = [x[0] for x in userIDs_fetch]

            #Email addresses
            c.execute("SELECT email_address FROM Accounts")
            email_fetch = c.fetchall()
            email_list = [x[0] for x in email_fetch]

            #staff mode
            c.execute("SELECT staff_mode FROM Accounts")
            staff_fetch = c.fetchall()
            staff_list = [x[0] for x in staff_fetch]

            #admin mode
            c.execute("SELECT admin_mode FROM Accounts")
            admin_fetch = c.fetchall()
            admin_list = [x[0] for x in admin_fetch]


            for k in self.tree.get_children():
                self.tree.delete(k)

            for i in range(len(userID_list)):
                #issued_bookIDs
                c.execute("SELECT bookID FROM MyBooks WHERE user_id=?",(userID_list[i],))
                issued_bookIDs_fetch = c.fetchall()
                issued_bookIDs_list = [x[0] for x in issued_bookIDs_fetch]

                for x in range(len(issued_bookIDs_list)):
                    issued_book_list_string = ','.join(map(str, issued_bookIDs_list))

                #earliest return date
                c.execute("SELECT return_date FROM MyBooks WHERE user_id=?",(userID_list[i],))
                return_date_fetch = c.fetchall()
                return_date_list = [x[0] for x in return_date_fetch]

                #convert the return_date_list from a list of strins to a list of dates
                dates_list = [datetime.strptime(date, '%Y-%m-%d').date() for date in return_date_list]

                try:
                    earliest_date = str(min(dates_list))
                except ValueError:
                    pass

                if len(issued_bookIDs_list)==0 or len(return_date_list)==0:
                    self.tree_ids.append(self.tree.insert("", "end", values=(userID_list[i], email_list[i], staff_list[i], admin_list[i],'N/A','N/A')))
                else:
                    self.tree_ids.append(self.tree.insert("", "end", values=(userID_list[i], email_list[i], staff_list[i], admin_list[i], issued_bookIDs_list, earliest_date)))
            self.tree.pack()

            ms.showinfo('Success!','Account Created!')


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
            message = e.create_verification_message("from@gmail.com", self.email_var.get(), "Books4All Verification Code", self.email_verification_code)
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

    def show_password(self, *args):
        if self.password_entry["show"] == "*":
            self.password_entry["show"]=''
            self.confirm_pw_entry["show"]=''
        else:
            self.password_entry["show"]='*'
            self.confirm_pw_entry["show"]='*'

    def update_account(self):
        user_id = int(self.update_userID_var.get())
        update_email = self.update_email_var.get()
        with sqlite3.connect('LibrarySystem.db') as db:
            c = db.cursor()

        if user_id == '':
            if update_email != '':
                email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
                if (re.search(email_regex, update_email)):

                    update = 'UPDATE Accounts SET staff_mode=? AND admin_mode=?'
                    c.execute(update,[(self.update_staff_mode_var.get()),(self.update_admin_mode_var.get())])
                    db.commit()

                    ms.showinfo('Success!','Account Updated!')
                else:
                    ms.showerror('Error', 'Invalid Email Address')
            else:
                ms.showerror('Error','Empty Email Field.')
        else:
            #Check if userID exists.
            check_account_existance = c.execute("SELECT user_id FROM Accounts WHERE user_id=?",(user_id,)).fetchall()
            if len(check_account_existance) == 0:
                ms.showerror('Error','Invalid User ID.')
            else:
                update = 'UPDATE Accounts SET staff_mode=? AND admin_mode=?'
                c.execute(update,[(self.update_staff_mode_var.get()),(self.update_admin_mode_var.get())])
                db.commit()

                #User IDs
                c.execute("SELECT user_id FROM Accounts")
                userIDs_fetch = c.fetchall()
                userID_list = [x[0] for x in userIDs_fetch]

                #Email addresses
                c.execute("SELECT email_address FROM Accounts")
                email_fetch = c.fetchall()
                email_list = [x[0] for x in email_fetch]

                #staff mode
                c.execute("SELECT staff_mode FROM Accounts")
                staff_fetch = c.fetchall()
                staff_list = [x[0] for x in staff_fetch]

                #admin mode
                c.execute("SELECT admin_mode FROM Accounts")
                admin_fetch = c.fetchall()
                admin_list = [x[0] for x in admin_fetch]


                for k in self.tree.get_children():
                    self.tree.delete(k)

                for i in range(len(userID_list)):
                    #issued_bookIDs
                    c.execute("SELECT bookID FROM MyBooks WHERE user_id=?",(userID_list[i],))
                    issued_bookIDs_fetch = c.fetchall()
                    issued_bookIDs_list = [x[0] for x in issued_bookIDs_fetch]

                    for x in range(len(issued_bookIDs_list)):
                        issued_book_list_string = ','.join(map(str, issued_bookIDs_list)) 

                    #earliest return date
                    c.execute("SELECT return_date FROM MyBooks WHERE user_id=?",(userID_list[i],))
                    return_date_fetch = c.fetchall()
                    return_date_list = [x[0] for x in return_date_fetch]

                    #convert the return_date_list from a list of strins to a list of dates
                    dates_list = [datetime.strptime(date, '%Y-%m-%d').date() for date in return_date_list]

                    try:
                        earliest_date = str(min(dates_list))
                    except ValueError:
                        pass

                    if len(issued_bookIDs_list)==0 or len(return_date_list)==0:
                        self.tree_ids.append(self.tree.insert("", "end", values=(userID_list[i], email_list[i], staff_list[i], admin_list[i],'N/A','N/A')))
                    else:
                        self.tree_ids.append(self.tree.insert("", "end", values=(userID_list[i], email_list[i], staff_list[i], admin_list[i], issued_bookIDs_list, earliest_date)))
                    self.tree.pack()

                ms.showinfo('Success','Account Updated!')


    def remove_account(self):
        user_id = self.remove_userID_var.get()
        remove_email = self.remove_email_var.get()
        with sqlite3.connect('LibrarySystem.db') as db:
            c = db.cursor()

        if user_id == '':
            if remove_email != '':
                email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
                if (re.search(email_regex, remove_email)):

                    remove = c.execute('DELETE FROM Accounts WHERE email_address=?',(remove_email,))
                    db.commit()

                    ms.showinfo('Success!','Account Removed!')
                else:
                    ms.showerror('Error', 'Invalid Email Address')
            else:
                ms.showerror('Error','Empty Email Field.')
        else:
            if isinstance(user_id, int) == True:
                #Check if userID exists.
                check_account_existance = c.execute("SELECT user_id FROM Accounts WHERE user_id=?",(user_id,)).fetchall()
                if len(check_account_existance) == 0:
                    ms.showerror('Error','Invalid User ID.')
                else:
                    remove = c.execute('DELETE FROM Accounts WHERE user_id=?',(user_id,))
                    db.commit()

                    #User IDs
                    c.execute("SELECT user_id FROM Accounts")
                    userIDs_fetch = c.fetchall()
                    userID_list = [x[0] for x in userIDs_fetch]

                    #Email addresses
                    c.execute("SELECT email_address FROM Accounts")
                    email_fetch = c.fetchall()
                    email_list = [x[0] for x in email_fetch]

                    #staff mode
                    c.execute("SELECT staff_mode FROM Accounts")
                    staff_fetch = c.fetchall()
                    staff_list = [x[0] for x in staff_fetch]

                    #admin mode
                    c.execute("SELECT admin_mode FROM Accounts")
                    admin_fetch = c.fetchall()
                    admin_list = [x[0] for x in admin_fetch]


                    for k in self.tree.get_children():
                        self.tree.delete(k)

                    for i in range(len(userID_list)):
                        #issued_bookIDs
                        c.execute("SELECT bookID FROM MyBooks WHERE user_id=?",(userID_list[i],))
                        issued_bookIDs_fetch = c.fetchall()
                        issued_bookIDs_list = [x[0] for x in issued_bookIDs_fetch]

                        for x in range(len(issued_bookIDs_list)):
                            issued_book_list_string = ','.join(map(str, issued_bookIDs_list)) 

                        #earliest return date
                        c.execute("SELECT return_date FROM MyBooks WHERE user_id=?",(userID_list[i],))
                        return_date_fetch = c.fetchall()
                        return_date_list = [x[0] for x in return_date_fetch]

                        #convert the return_date_list from a list of strins to a list of dates
                        dates_list = [datetime.strptime(date, '%Y-%m-%d').date() for date in return_date_list]

                        try:
                            earliest_date = str(min(dates_list))
                        except ValueError:
                            pass


                        if len(issued_bookIDs_list)==0 or len(return_date_list)==0:
                            self.tree_ids.append(self.tree.insert("", "end", values=(userID_list[i], email_list[i], staff_list[i], admin_list[i],'N/A','N/A')))
                        else:
                            self.tree_ids.append(self.tree.insert("", "end", values=(userID_list[i], email_list[i], staff_list[i], admin_list[i], issued_bookIDs_list, earliest_date)))
                        self.tree.pack()

                    ms.showinfo('Success!','Account Removed!')
            else:
                ms.showerror('Error','Invalid User ID.')