# Main run file

# Imports
import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox as ms
import bcrypt
import re
import sys
import random
import linecache

# File Imports
from email_sys import Email
from home import Home
from library import Library
from options import Options
from guesthp import GuestHelp
from userhp import UserHelp
from account import Account
from mybooks import MyBooks
from bookdatabase import BookDatabase
from staffhp import StaffHelp
from admin import Admin
from adminhp import AdminHelp
from forgotpw import ForgotPW

# Connect to the database
with sqlite3.connect('LibrarySystem.db') as db:
    c = db.cursor()

# Fetch configurations of the widgets from the config file.
# re.sub filters the title of the variable value in the config file. e.g. WIDTH = 225 becomes 225
# .strip() removes any potential whitespace that could cause issues.

PADX = re.sub('^.*?=', '', linecache.getline('config.txt', 2))
PADY = re.sub('^.*?=', '', linecache.getline('config.txt', 3))
MAIN_GEOMETRY = re.sub('^.*?=', '', linecache.getline('config.txt', 4)).strip()
SMALL_GEOMETRY = re.sub('^.*?=', '', linecache.getline('config.txt', 5)).strip()
BG = re.sub('^.*?=', '', linecache.getline('config.txt', 6)).strip()
DANGER_FG = re.sub('^.*?=', '', linecache.getline('config.txt', 7)).strip()
MAIN_APP_BG = re.sub('^.*?=', '', linecache.getline('config.txt', 9)).strip()
HEADER_FONT = re.sub('^.*?=', '', linecache.getline('config.txt', 11)).strip()
VERSION = re.sub('^.*?=', '', linecache.getline('config.txt', 12)).strip()
FG = re.sub('^.*?=', '', linecache.getline('config.txt', 13)).strip()
BD = re.sub('^.*?=', '', linecache.getline('config.txt', 14)).strip()
RELIEF = re.sub('^.*?=', '', linecache.getline('config.txt', 15)).strip()


class SignIn():
    '''
    Called when the Application Starts
    Returns a window with 3 tabs for registration, login and forgot password.
    '''
    def __init__(self, parent):
        '''
        Initialise the visual window for the system startup.
        '''
        # Window parameters
        parent.geometry(SMALL_GEOMETRY)
        parent.title('Library Management System')
        parent.configure(bg=BG)
        parent.option_add("*foreground", "yellow")
        parent.option_add("*background", "gray15")

        # Window Icon
        parent.iconbitmap('Books4All.ico')

        self.parent = parent
        sign_in_notebook = ttk.Notebook(self.parent)
        sign_in_notebook.pack(expand=True, fill=tk.BOTH)

        # Call the login, register and forgot password tabs and their
        # respective visual layout.
        Login(parent, sign_in_notebook)
        Register(parent, sign_in_notebook)
        ForgotPW(parent, sign_in_notebook)


class Login():
    '''
    Holds the login page visual layout and
    any login related functions.
    '''
    def __init__(self, parent, sign_in_notebook):
        '''
        Mostly used to layout the visuals of the page
        and establish all the user inputs and required
        variables to be extracted from the user, through
        this interface.
        '''

        # Establish the notebook and main page window.
        self.parent = parent
        login_page = tk.Frame(sign_in_notebook)
        sign_in_notebook.add(login_page, text='Login')

        main_frame = tk.Frame(login_page)
        main_frame.pack(fill=tk.BOTH, side=tk.TOP)

        main_label = tk.Label(main_frame, text='Library System v'+VERSION)
        main_label.pack(fill=tk.X, anchor=tk.N)

        header_frame = tk.Frame(login_page)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        header = tk.Label(header_frame, text='Login', font=HEADER_FONT)
        header.pack(side=tk.TOP)

        # Login Container
        login_container = tk.Frame(login_page, bg=BG, relief=RELIEF, bd=BD)
        login_container.pack(padx=PADX, pady=PADY)

        # Email Container
        email_container = tk.Frame(login_container, bg=BG)
        email_container.pack(expand=True)

        email_label = tk.Label(email_container, text='    Email:   ', bg=BG)
        email_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.user_email_var = tk.StringVar()
        self.user_email_var.set('')
        self.email_entry = ttk.Entry(email_container, textvariable=self.user_email_var, font='System 6')
        self.email_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)
        self.email_entry.focus()

        # Password Container
        password_container = tk.Frame(login_container, bg=BG)
        password_container.pack(expand=True)

        password_label = tk.Label(password_container, text=' Password:', bg=BG)
        password_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.user_password_var = tk.StringVar()
        self.user_password_var.set('')
        self.password_entry = ttk.Entry(password_container, textvariable=self.user_password_var,
                                                font='System 6', show='*')
        self.password_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # Login Button Container
        button_container = tk.Frame(login_container, bg=BG)
        button_container.pack(expand=True)

        login_button = ttk.Button(button_container, text='Login', command=lambda: self.login())
        guest_button = ttk.Button(button_container, text='Guest Login', command=lambda: self.guest_login())
        exit_button = ttk.Button(button_container, text='Exit', command=lambda: self.system_exit())

        login_button.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)
        guest_button.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)
        exit_button.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        self.email_entry.bind("<Return>", self.login)
        self.password_entry.bind("<Return>", self.login)

    def login(self, *args):
        '''
        Pass the email and password variables entered to be
        evaluated and determine if the user can login
        using these details.
        '''
        login_email = self.user_email_var.get()
        login_password = self.user_password_var.get()

        # CHECK DETAILS AGAINST DATABASE DETAILS
        if login_password == '' or login_email == '':
            # If either field is empty, return error.
            ms.showwarning('Warning', 'Enter your email address and password')
        else:
            # Within try statement, because the email/password may not be in a valid format.
            try:
                # Fetch the password from the database that matches the email address entered.
                c.execute('SELECT password FROM Accounts WHERE email_address = ?', (login_email,))
                pass_hashed = c.fetchone()[0]

                # Convert the password returned from the database into a byte string
                # The passwords must be converted into a byte string,
                # because the bcrypt hashing module works using this
                # data type.
                pass_hashed_encode = pass_hashed.encode('utf-8')

                # Convert the entered password into a bytestring.
                bytes_login_password = bytes(login_password, 'utf-8')

                # Check if the byte string entered password matches
                # the byte string password in the database.
                if bcrypt.checkpw(bytes_login_password, pass_hashed_encode):

                    # If the passwords match, display a successful login.
                    ms.showinfo('Success', 'Successfully Logged in!')

                    # Upon successful login, destroy the SignIn page
                    for child in self.parent.winfo_children():
                        child.destroy()

                    # Call the main application to come forth, also
                    # passing in the email to launch the user-specific
                    # layout of the pages (notably the Account and MyBooks page)
                    MainApplication(self.parent, login_email)

                    # Set the entry fields to be empty.
                    self.user_email_var.set('')
                    self.user_password_var.set('')
                else:
                    ms.showerror('Error', 'Incorrect password/email')
            except TypeError:
                ms.showerror('Error', 'Incorrect password/email')

    def guest_login(self):
        '''
        Allows the user to use the system with a guest login.
        This prevents any user-specific usage of the system, such as
        using the MyBooks or Account page.
        '''
        ms.showinfo('Success', 'Successfully logged in')

        # Destroy the SignIn page, widget by widget.
        for child in self.parent.winfo_children():
            child.destroy()

            # Call the main application to come into view.
            MainApplication(self.parent, 'guest')

    def system_exit(self):
        '''
        Allows the user to exit the system at any time.
        Destroys the window and exits the system.
        '''
        root.destroy()
        sys.exit()


class Register():
    '''
    Holds the registration page layout
    and any related functions.
    '''
    def __init__(self, parent, sign_in_notebook):
        '''
        Initialise the visual layout of the page
        and establish all the user inputs and required
        variables to be extracted from the user, through
        this interface.
        '''
        register_page = tk.Frame(sign_in_notebook)
        self.sign_in_notebook = sign_in_notebook
        self.sign_in_notebook.add(register_page, text='Register')

        main_frame = tk.Frame(register_page, relief=tk.FLAT)
        main_frame.pack(fill=tk.BOTH, side=tk.TOP)

        main_label = tk.Label(main_frame, text='Library System v'+VERSION)
        main_label.pack(fill=tk.X, anchor=tk.N)

        header_frame = tk.Frame(register_page)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        header = tk.Label(header_frame, text='Register', font=HEADER_FONT)
        header.pack(side=tk.TOP)

        # Register Container
        register_container = tk.Frame(register_page, bg=BG, relief=RELIEF, bd=BD)
        register_container.pack(padx=PADX, pady=PADY)

        # Email Container
        email_container = tk.Frame(register_container, bg=BG)
        email_container.pack(expand=True)

        email_label = tk.Label(email_container, text='    Email:   ', bg=BG)
        email_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.user_email_var = tk.StringVar()
        self.user_email_var.set('')
        self.email_entry = ttk.Entry(email_container, textvariable=self.user_email_var,
                                                font='System 6')
        self.email_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # Password Container
        password_container = tk.Frame(register_container, bg=BG)
        password_container.pack(expand=True)

        password_label = tk.Label(password_container, text=' Password:', bg=BG)
        password_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.user_password_var = tk.StringVar()
        self.user_password_var.set('')
        self.user_password_var.trace("w", self.password_strength)

        self.password_entry = ttk.Entry(password_container, textvariable=self.user_password_var,
                                                font='System 6', show='*')
        self.password_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # Confirm Password Container
        confirm_pw_container = tk.Frame(register_container, bg=BG)
        confirm_pw_container.pack(expand=True)

        confirm_pw_label = tk.Label(confirm_pw_container, text='Confirm\n Password:', bg=BG)
        confirm_pw_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.confirm_pw_var = tk.StringVar()
        self.confirm_pw_var.set('')
        self.confirm_pw_entry = ttk.Entry(confirm_pw_container, textvariable=self.confirm_pw_var,
                                                font='System 6', show='*')
        self.confirm_pw_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        # Register Button Container
        button_container = tk.Frame(register_container, bg=BG)
        button_container.pack(expand=True)

        register_button = ttk.Button(button_container, text='Register', command=lambda: self.register())
        exit_button = ttk.Button(button_container, text='Exit', command=lambda: self.system_exit())
        show_password_button = ttk.Button(button_container, text='Show Password', command=lambda: self.show_password())

        register_button.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)
        exit_button.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)
        show_password_button.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        self.email_entry.bind("<Return>", self.register)
        self.password_entry.bind("<Return>", self.register)
        self.confirm_pw_entry.bind("<Return>", self.register)

        # Password Strength measure container
        self.password_strength_container_1 = tk.Frame(register_container, bg=BG)
        self.password_strength_container_1.pack(expand=True)

        self.password_strength_label_1 = tk.Label(self.password_strength_container_1, text='Password must be a minimum of 8 characters.',
                                                bg=BG, fg=DANGER_FG)
        self.password_strength_label_1.pack(anchor=tk.E, side=tk.RIGHT, padx=PADX, pady=PADY)

        self.password_strength_container_2 = tk.Frame(register_container, bg=BG)
        self.password_strength_container_2.pack(expand=True)

        self.password_strength_label_2 = tk.Label(self.password_strength_container_2, text="""Besides letters, include at least a number or symbol )([!@#$%^*-_+=|\\\{\}\[\]`¬;:@"'<>,./?]""",
                                                bg=BG, fg=DANGER_FG)
        self.password_strength_label_2.pack(anchor=tk.E, side=tk.RIGHT, padx=PADX, pady=PADY)

    def register(self, *args):
        '''
        Pass the email, password and confirm password variables entered to be
        evaluated and determine if the user can login
        using these details.
        '''
        # delete if statement and replace with database check for user's input credentials
        # validity checks for entry field + logic
        self.reg_email = self.user_email_var.get()

        # Broad email standard.
        email_regex = '^\S+@\S+$'

        # Check if the email entered matches the email regex established.
        if (re.search(email_regex, self.reg_email)):

            # Get the password variables.
            reg_pw = self.user_password_var.get()
            reg_confirm_pw = self.confirm_pw_var.get()

            if reg_pw != reg_confirm_pw:
                ms.showwarning('Warning', 'Your passwords do not match.')
            elif reg_pw == '' or reg_pw == '':
                ms.showwarning('Warning', 'You left the password fields empty!')
            else:
                # Encrypt+Salt PWs
                hashable_pw = bytes(reg_pw, 'utf-8')
                hashed_pw = bcrypt.hashpw(hashable_pw, bcrypt.gensalt())

                # Convert into base64string
                self.db_hashed_pw = hashed_pw.decode("utf-8")

                # Fetch all accounts matching this email address (should only be one.)
                find_user = ('SELECT * FROM Accounts WHERE email_address = ?')
                c.execute(find_user, [(self.reg_email)])

                if c.fetchall():
                    ms.showerror('Error!', 'Email is already registered to an Account.')
                else:
                    # Will need to verify whether this email address is linked to the user.
                    # Steps to take in the following code:
                    # 1. Open a TopLevel window to prompt the user to enter a code into an entry box /DONE
                    # 2. Send the user an email with a randomly generated 6 digit code
                    # 3. Compare the 6 digit code the user entered to the one that was sent.
                    # 4. If they match, close the TopLevel, and follow on with the rest of the code below.
                    # 5. If the codes do not match, then an error will be prompted.
                    # 6. A 'Resend Code' button will be available on a cooldown (1min to stop spammers) that sends another code to the user.
                    #    Upon this code being sent, the previous code needs to be made invalid.

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

                    header_description = tk.Label(header_frame, text='A 6 digit verification code has been sent to\n'+self.reg_email+'\n Please enter the 6 digit code into the entry field below.', font='System 8')
                    header_description.pack(side=tk.TOP)

                    self.timer = tk.Label(header_frame, text='')
                    self.timer.pack(side=tk.TOP)

                    # 1 minute timer is placed to avoid spamming inboxes.
                    self.time_remaining = 0
                    self.countdown(60)

                    # Verification Code Full Container
                    code_container = tk.Frame(self.accountVerification, bg=BG)
                    code_container.pack(padx=PADX, pady=PADY)

                    # Verification Code Entry Field Container
                    verification_code_container = tk.Frame(code_container, bg=BG)
                    verification_code_container.pack(expand=True)

                    verification_code_label = tk.Label(verification_code_container, text='    Verification Code:   ', bg=BG)
                    verification_code_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

                    self.verification_code_reg = root.register(self.verification_code_validate)

                    self.verification_code_var = tk.StringVar()
                    self.verification_code_var.set('')
                    self.verification_code_entry = ttk.Entry(verification_code_container, textvariable=self.verification_code_var,
                                                            font='System 6', validate="key",
                                                            validatecommand=(self.verification_code_reg, "%P"))
                    self.verification_code_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

                    # Focus on the entry field for the user to enter the code.
                    self.email_entry.focus()

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
                        random_integer = random.SystemRandom().randint(0,9)
                        i += 1
                        self.email_verification_code += str(random_integer)

                    # 2.2. Send Email to user with the verification code.
                    # Call the Email class
                    e = Email()
                    service = e.get_service()
                    message = e.create_verification_message("from@gmail.com", self.reg_email, "Books4All Verification Code", self.email_verification_code)
                    e.send_message(service, "from@gmail.com", message)
        else:
            ms.showerror('Error', 'Invalid Email Address')

    def check_code(self, *args):
        '''
        Check the code that was sent by email
        with the code that the user entered.
        '''
        # 3. Compare the email code with the input code
        if self.verification_code_var.get() != self.email_verification_code:
            ms.showerror('Error', 'The verification code does not match the code sent.')
        else:
            ms.showinfo('Success', 'The verification code matches the code we sent!')
            self.accountVerification.destroy()

            # Find the next highest user_id value, so that the new user can be entered into this empty row.
            select_highest_val = c.execute('SELECT MAX(user_id) + 1 FROM Accounts').fetchall()
            highest_val = [x[0] for x in select_highest_val][0]
            print(highest_val)

            if highest_val is None:
                # If its the first ever account, make it have admin+staff access.
                # This is to allow the system to be setup at first.
                insert = 'INSERT INTO Accounts(email_address,password,user_id,staff_mode,admin_mode) VALUES(?,?,?,1,1)'
                c.execute(insert, [(self.reg_email), (self.db_hashed_pw), (highest_val)])
                db.commit()
            else:
                # Insert the user information in the next highest user id.
                insert = 'INSERT INTO Accounts(email_address,password,user_id) VALUES(?,?,?)'
                c.execute(insert, [(self.reg_email), (self.db_hashed_pw), (highest_val)])
                db.commit()

            ms.showinfo('Success!', 'Account Created!')

            # Switch tabs after registration
            login_index = self.sign_in_notebook.index(0)
            self.sign_in_notebook.select(login_index)

            # Remove details from register entry fields
            self.user_email_var.set('')
            self.user_password_var.set('')
            self.confirm_pw_var.set('')

    def resend_code(self, *args):
        '''
        If an issue is present with the delivery
        of the verification code, then the user
        can resend a code.
        '''

        # 'Ready to Resend Code!' will be displayed once 
        # the countdown has reached 0.
        if self.timer["text"] == "Ready to Resend Code!":

            # Set the entry field to be empty.
            self.email_verification_code = ''

            # Generate another verification code.
            i = 0
            while i < 6:
                random_integer = random.SystemRandom().randint(0,9)
                i += 1
                self.email_verification_code += str(random_integer)

            # 2.2. Send Email to user with the verification code.
            # Call the Email class
            e = Email()
            service = e.get_service()
            message = e.create_verification_message("from@gmail.com", self.reg_email, "Books4All Verification Code", self.email_verification_code)
            e.send_message(service, "from@gmail.com", message)

            # Reset the timer.
            self.time_remaining = 0
            self.countdown(60)
        else:
            # Display warning if the user attempts to resend the code, when the timer is not yet at 0.
            ms.showwarning('Warning', 'Please wait another '+self.timer["text"]+' seconds to resend a code.')

    def countdown(self, time_remaining=None):
        '''
        Starts a countdown timer of 1 minute
        once a verification code is sent
        to the target address.
        '''
        if time_remaining is not None:
            self.time_remaining = time_remaining

        if self.time_remaining <= 0:
            # The time is 0, and the code can be resent.
            self.timer["text"] = "Ready to Resend Code!"
        else:
            # The timer is still counting down.
            self.timer["text"] = ("%d" % self.time_remaining)
            self.time_remaining = self.time_remaining - 1

            # Tell the window to wait 1000ms (=1s) before updating the timer again.
            self.accountVerification.after(1000, self.countdown)

    def verification_code_validate(self, verification_code_inp):
        '''
        Validate that the code input is all integers.
        '''
        if verification_code_inp.isdigit():
            if len(verification_code_inp) > 6:
                return False
            else:
                return True
        elif verification_code_inp == "":
            return True
        else:
            return False

    def password_strength(self, *args):
        '''
        Evaluate the strength of the password
        based on length and characters used.
        '''

        # A regex with a docstring of all of the valid characters
        # that can be used in the password.
        special_characters_regex = re.compile("""[!@#$%^*-_+=|\\\{\}\[\]`¬;:@"'<>,./?]()""")
        password_input = self.user_password_var.get()

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

    def show_password(self, *args):
        '''
        Allows the user to toggle the password to
        be shown in plaintext or hidden by asterisks.
        '''
        if self.password_entry["show"] == '*':
            self.password_entry["show"] = ''
            self.confirm_pw_entry["show"] = ''
        else:
            self.password_entry["show"] = '*'
            self.confirm_pw_entry["show"] = '*'

    def system_exit(self):
        '''
        Allow user to exit the system.
        '''
        root.destroy()
        sys.exit()


class MainApplication():
    '''
    Evaluates what pages to show to the user
    based on their account's access level,
    and user-specific information.
    '''
    def __init__(self, parent, email):
        '''
        Initialise the visual layout of the page
        and any related class instance varaibles.
        '''
        # Declare variables
        self.parent = parent
        self.email = email

        # root window configurations
        parent.configure(bg=MAIN_APP_BG)
        parent.title("Library System v"+VERSION)
        parent.option_add('*Font', 'System 12')
        parent.option_add('*Label.Font', 'System 12')
        parent.geometry(MAIN_GEOMETRY)
        parent.wm_state('zoomed')

        # Global Header
        global_frame = tk.Frame(parent, relief=tk.FLAT)
        global_frame.pack(fill=tk.BOTH, side=tk.TOP)

        global_label = tk.Label(global_frame, text='Library System v'+VERSION)
        global_label.pack(fill=tk.X, anchor=tk.N)

        # Logout button
        logout_button = ttk.Button(global_frame, text='Logout', command=self.logout)
        logout_button.pack(side=tk.RIGHT)

        self.main_notebook = ttk.Notebook(parent)
        self.main_notebook.pack(expand=True, fill=tk.BOTH)

        # Instantiate Classes (HP = Home Page, MBP = My Books Page, etc...)
        self.HP = Home(self.parent, self.main_notebook)
        if email != 'guest':
            # Only display these tabs, if the user has not used a guest login
            # as they are user-specific pages.
            self.AP = Account(self.parent, self.main_notebook, email)
            self.MBP = MyBooks(self.parent, self.main_notebook, email)

        # Display the library regardless of if its a guest account
        self.LP = Library(self.parent, self.main_notebook)

        # Needs 'Staff' powers to see this page.
        # Check if the user has staff privileges
        try:
            # Fetch the staff mode from the email address that was passed into the function.
            staff_mode_check = c.execute('SELECT staff_mode FROM Accounts WHERE email_address=?', (email,)).fetchall()
            staff_mode = [x[0] for x in staff_mode_check][0]
            if staff_mode == 1:
                self.BDP = BookDatabase(self.parent, self.main_notebook, email)
                self.SHP = StaffHelp(self.parent, self.main_notebook, email)
        except IndexError:
            # Continue with the construction of the
            # main application regardless of if the prior criteria
            # is not met.
            pass

        try:

            # Fetch the admin mode from the email address that was passed into the function.
            admin_mode_check = c.execute('SELECT admin_mode FROM Accounts WHERE email_address=?', (email,)).fetchall()
            admin_mode = [x[0] for x in admin_mode_check][0]

            if admin_mode == 1:
                self.AP = Admin(self.parent, self.main_notebook, email)
                self.AHP = AdminHelp(self.parent, self.main_notebook, email)
        except IndexError:
            pass

        self.OP = Options(self.parent, self.main_notebook)

        if email == 'guest':
            self.GHP = GuestHelp(self.parent, self.main_notebook)

        if email != 'guest':
            if admin_mode == 0 and staff_mode == 0:
                self.UHP = UserHelp(self.parent, self.main_notebook, email)

    def logout(self):
        '''
        Allow the user to logout from the system at any time, from any page.
        '''
        # Confirmation of logout.
        logout_confirmation = ms.askquestion('Logout', 'Are you sure you want to logout?', icon='warning')
        if logout_confirmation == 'yes':

            # Destroy all the widgets in the root window.
            for child in self.parent.winfo_children():
                child.destroy()

            # Launch the SignIn page to allow the user to login again.
            SignIn(self.parent)


if __name__ == "__main__":
    # Main driver of system

    # Launch root window
    root = tk.Tk()

    # Call the SignIn page and pass
    # the root window into the class.
    rlp = SignIn(root)

    # Run the window.
    root.mainloop()
