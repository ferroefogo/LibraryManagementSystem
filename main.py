#Main run file
import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox as ms
import bcrypt
import re
import sys
import secrets
import random
import linecache

from email_sys import Email
from home import Home
from library import Library
from options import Options
from guesthp import GuestHelp
from userhp import UserHelp
from email_sys import Email
from account import Account
from mybooks import MyBooks
from bookdatabase import BookDatabase
from staffhp import StaffHelp
from admin import Admin
from adminhp import AdminHelp
from forgotpw import ForgotPW

conn = sqlite3.connect('LibrarySystem.db')
c = conn.cursor()

#Fetch configurations of the widgets from the config file.
#re.sub filters the title of the variable value in the config file. e.g. WIDTH=225 becomes 225
#.strip() removes any potential whitespace that could cause issues.

PADX = re.sub('^.*?=', '', linecache.getline('config.txt',2))
PADY = re.sub('^.*?=', '', linecache.getline('config.txt',3))
MAIN_GEOMETRY = re.sub('^.*?=', '', linecache.getline('config.txt',4)).strip()
SMALL_GEOMETRY = re.sub('^.*?=','',linecache.getline('config.txt',5)).strip()
BG = re.sub('^.*?=', '', linecache.getline('config.txt',6)).strip()
DANGER_FG = re.sub('^.*?=', '', linecache.getline('config.txt',7)).strip()
MAIN_APP_BG = re.sub('^.*?=', '', linecache.getline('config.txt',9)).strip()
HEADER_FONT = re.sub('^.*?=', '', linecache.getline('config.txt',11)).strip()

class SignIn():
    def __init__(self, parent):
        self.parent = parent
        sign_in_notebook = ttk.Notebook(self.parent)
        sign_in_notebook.pack(expand=True, fill=tk.BOTH)

        login = Login(parent, sign_in_notebook)
        register = Register(parent, sign_in_notebook)
        forgot_pw = ForgotPW(parent, sign_in_notebook)



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

        header = tk.Label(header_frame, text='Login', font=HEADER_FONT)
        header.pack(side=tk.TOP)

        #Login Container
        login_container = tk.Frame(login_page, bg=BG)
        login_container.pack(padx=PADX, pady=PADY)

        #Email Container
        email_container = tk.Frame(login_container, bg=BG)
        email_container.pack(expand=True)

        email_label = tk.Label(email_container, text='    Email:   ', bg=BG)
        email_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.user_email_var = tk.StringVar()
        self.user_email_var.set('')
        self.email_entry = ttk.Entry(email_container, textvariable=self.user_email_var, font='System 6',)
        self.email_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)
        self.email_entry.focus()


        #Password Container
        password_container = tk.Frame(login_container, bg=BG)
        password_container.pack(expand=True)

        password_label = tk.Label(password_container, text=' Password:', bg=BG)
        password_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.user_password_var = tk.StringVar()
        self.user_password_var.set('')
        self.password_entry = ttk.Entry(password_container, textvariable=self.user_password_var,
                                                font='System 6', show='*')
        self.password_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        #Login Button Container
        button_container = tk.Frame(login_container, bg=BG)
        button_container.pack(expand=True)

        login_button = ttk.Button(button_container, text='Login', command=lambda:self.login())
        guest_button = ttk.Button(button_container, text='Guest Login', command=lambda:self.guest_login())
        exit_button = ttk.Button(button_container, text='Exit', command=lambda:self.system_exit())

        login_button.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)
        guest_button.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)
        exit_button.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        self.email_entry.bind("<Return>", self.login)
        self.password_entry.bind("<Return>", self.login)

    def login(self, *args):
        login_email = self.user_email_var.get()
        login_password = self.user_password_var.get()

        # CHECK DETAILS AGAINST DATABASE DETAILS
        if login_password == '' and login_email  == '':
             ms.showwarning('Warning','Enter your email address and password')
        else:
            try:
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
            except TypeError:
                ms.showerror('Error','Incorrect password/email')            


    def guest_login(self):
        ms.showinfo('Success','Successfully logged in')
        for child in self.parent.winfo_children():
            child.destroy()

            MainApplication(self.parent, 'guest')

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

        header = tk.Label(header_frame, text='Register', font=HEADER_FONT)
        header.pack(side=tk.TOP)

        #Register Container
        register_container = tk.Frame(register_page, bg=BG)
        register_container.pack(padx=PADX, pady=PADY)

        #Email Container
        email_container = tk.Frame(register_container, bg=BG)
        email_container.pack(expand=True)

        email_label = tk.Label(email_container, text='    Email:   ', bg=BG)
        email_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.user_email_var = tk.StringVar()
        self.user_email_var.set('')
        self.email_entry = ttk.Entry(email_container, textvariable=self.user_email_var,
                                                font='System 6')
        self.email_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        #Password Container
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



        #Confirm Password Container
        confirm_pw_container = tk.Frame(register_container, bg=BG)
        confirm_pw_container.pack(expand=True)

        confirm_pw_label = tk.Label(confirm_pw_container, text='Confirm\n Password:', bg=BG)
        confirm_pw_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.confirm_pw_var = tk.StringVar()
        self.confirm_pw_var.set('')
        self.confirm_pw_entry = ttk.Entry(confirm_pw_container, textvariable=self.confirm_pw_var,
                                                font='System 6', show='*')
        self.confirm_pw_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        #Register Button Container
        button_container = tk.Frame(register_container, bg=BG)
        button_container.pack(expand=True)

        register_button = ttk.Button(button_container, text='Register', command=lambda:self.register())
        exit_button = ttk.Button(button_container, text='Exit', command=lambda:self.system_exit())
        show_password_button = ttk.Button(button_container, text='Show Password', command=lambda:self.show_password())

        register_button.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)
        exit_button.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)
        show_password_button.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        self.email_entry.bind("<Return>", self.register)
        self.password_entry.bind("<Return>", self.register)
        self.confirm_pw_entry.bind("<Return>", self.register)

        #Password Strength measure container
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
        # delete if statement and replace with database check for user's input credentials
        #validity checks for entry field + logic
        self.reg_email = self.user_email_var.get()

        #Accepted email standard.
        email_regex = '^\S+@\S+$'

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
                    self.accountVerification.geometry(SMALL_GEOMETRY)
                    self.accountVerification.resizable(False, False)


                    main_frame = tk.Frame(self.accountVerification, relief=tk.FLAT)
                    main_frame.pack(fill=tk.BOTH, side=tk.TOP)

                    main_label = tk.Label(main_frame, text='Library System v1.0')
                    main_label.pack(fill=tk.X, anchor=tk.N)

                    header_frame = tk.Frame(self.accountVerification)
                    header_frame.pack(fill=tk.X, side=tk.TOP)

                    header = tk.Label(header_frame, text='Account Verification', font=HEADER_FONT)
                    header.pack(side=tk.TOP)

                    header_description = tk.Label(header_frame, text='A 6 digit verification code has been sent to\n'+self.reg_email+'\n Please enter the 6 digit code into the entry field below.', font='System 8')
                    header_description.pack(side=tk.TOP)

                    self.timer = tk.Label(header_frame, text='')
                    self.timer.pack(side=tk.TOP)

                    self.time_remaining = 0
                    self.countdown(60)

                    #Codes Full Container
                    code_container = tk.Frame(self.accountVerification, bg=BG)
                    code_container.pack(padx=PADX, pady=PADY)

                    #Code Entry Field Container
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

                    #Buttons Container
                    button_container = tk.Frame(code_container, bg=BG)
                    button_container.pack(expand=True)

                    check_code_button = ttk.Button(button_container, text='Check Verification Code', command=lambda:self.check_code(self.verification_code_var.get()))
                    resend_code_button = ttk.Button(button_container, text='Resend Verification Code', command=lambda:self.resend_code(self.verification_code_var.get()))

                    check_code_button.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)
                    resend_code_button.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)
                    

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
            # insert = 'INSERT INTO Accounts(email_address,password,user_id,staff_mode,admin_mode) VALUES(?,?,?,?,?)'
            # c.execute(insert,[(self.reg_email),(self.db_hashed_pw),("1"),("1"),("1")])
            # db.commit()

            select_highest_val = c.execute('SELECT MAX(user_id) + 1 FROM Accounts').fetchall()
            highest_val = [x[0] for x in select_highest_val][0]

            insert = 'INSERT INTO Accounts(email_address,password,user_id) VALUES(?,?,?)'
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

        header = tk.Label(header_frame, text='Forgot Password?', font=HEADER_FONT)
        header.pack(side=tk.TOP)

        #Credentials Container
        credentials_container = tk.Frame(forgot_pw_page, bg=BG)
        credentials_container.pack(padx=PADX, pady=PADY)

        #Email Container
        email_container = tk.Frame(credentials_container, bg=BG)
        email_container.pack(expand=True)

        email_label = tk.Label(email_container, text='    Email:   ', bg=BG)
        email_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        self.user_email_var = tk.StringVar()
        self.user_email_var.set('')
        self.email_entry = ttk.Entry(email_container, textvariable=self.user_email_var,
                                                font='System 6')
        self.email_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        #Send Request Button Container
        button_container = tk.Frame(credentials_container, bg=BG)
        button_container.pack(expand=True)

        send_request_button = ttk.Button(button_container, text='Send Request', command=lambda:self.send_request())
        exit_button = ttk.Button(button_container, text='Exit', command=lambda:self.system_exit())

        send_request_button.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)
        exit_button.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

        self.email_entry.bind("<Return>", self.send_request)

    def send_request(self, *args):
        #Accepted email standard internarionally.
        input_email = self.user_email_var.get()
        email_regex = '^\S+@\S+$'
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
            self.forgotPassword.geometry(SMALL_GEOMETRY)
            self.forgotPassword.resizable(False, False)


            main_frame = tk.Frame(self.forgotPassword, relief=tk.FLAT)
            main_frame.pack(fill=tk.BOTH, side=tk.TOP)

            main_label = tk.Label(main_frame, text='Library System v1.0')
            main_label.pack(fill=tk.X, anchor=tk.N)

            header_frame = tk.Frame(self.forgotPassword)
            header_frame.pack(fill=tk.X, side=tk.TOP)

            header = tk.Label(header_frame, text='Forgot Password', font=HEADER_FONT)
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
            passwords_container = tk.Frame(self.forgotPassword, bg=BG)
            passwords_container.pack(padx=PADX, pady=PADY)

            #Generated Password Entry Field Container
            generated_password_container = tk.Frame(passwords_container, bg=BG)
            generated_password_container.pack(expand=True)

            generated_password_label = tk.Label(generated_password_container, text='    Generated Password:   ', bg=BG)
            generated_password_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)


            self.generated_password_var = tk.StringVar()
            self.generated_password_var.set('')
            self.generated_password_entry = ttk.Entry(generated_password_container, textvariable=self.generated_password_var,font='System 6')
            self.generated_password_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

            #Password Container
            new_password_container = tk.Frame(passwords_container, bg=BG)
            new_password_container.pack(expand=True)

            new_password_label = tk.Label(new_password_container, text=' New Password:', bg=BG)
            new_password_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

            self.new_password_var = tk.StringVar()
            self.new_password_var.set('')
            self.new_password_var.trace("w", self.password_strength)

            self.new_password_entry = ttk.Entry(new_password_container, textvariable=self.new_password_var,
                                                    font='System 6', show='*')
            self.new_password_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

            #Confirm Password Container
            confirm_pw_container = tk.Frame(passwords_container, bg=BG)
            confirm_pw_container.pack(expand=True)

            confirm_pw_label = tk.Label(confirm_pw_container, text='Confirm\n New Password:', bg=BG)
            confirm_pw_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

            self.confirm_pw_var = tk.StringVar()
            self.confirm_pw_var.set('')
            self.confirm_pw_entry = ttk.Entry(confirm_pw_container, textvariable=self.confirm_pw_var,
                                                    font='System 6', show='*')
            self.confirm_pw_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)

            #Password Strength measure container
            self.password_strength_container_1 = tk.Frame(passwords_container, bg=BG)
            self.password_strength_container_1.pack(expand=True)

            self.password_strength_label_1 = tk.Label(self.password_strength_container_1, text='Password must be a minimum of 8 characters.',
                                                    bg=BG, fg=DANGER_FG)
            self.password_strength_label_1.pack(anchor=tk.E, side=tk.RIGHT, padx=PADX, pady=PADY)


            self.password_strength_container_2 = tk.Frame(passwords_container, bg=BG)
            self.password_strength_container_2.pack(expand=True)

            self.password_strength_label_2 = tk.Label(self.password_strength_container_2, text="""Besides letters, include at least a number or symbol shown below \n)([!@#$%^*-_+=|\\\{\}\[\]`¬;:@"'<>,./?]""",
                                                    bg=BG, fg=DANGER_FG)
            self.password_strength_label_2.pack(anchor=tk.E, side=tk.RIGHT, padx=PADX, pady=PADY)


            #Buttons Container
            button_container = tk.Frame(passwords_container, bg=BG)
            button_container.pack(expand=True)

            update_password_button = ttk.Button(button_container, text='Update Password', command=lambda:self.update_password())
            show_password_button = ttk.Button(button_container, text='Show Password', command=lambda:self.show_password())
            resend_password_button = ttk.Button(button_container, text='Resend Password', command=lambda:self.resend_password())

            update_password_button.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)
            show_password_button.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)
            resend_password_button.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)


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



class MainApplication():
    def __init__(self, parent, email):
        # Declare variables
        self.parent = parent
        self.email = email


        parent.configure(bg=MAIN_APP_BG)
        parent.title("Library System v1.0")
        parent.option_add('*Font', 'System 12')
        parent.option_add('*Label.Font', 'System 12')
        parent.geometry(MAIN_GEOMETRY)


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
        if email != 'guest':
            self.AP = Account(self.parent, self.main_notebook, email)
            self.MBP = MyBooks(self.parent, self.main_notebook, email)
        self.LP = Library(self.parent, self.main_notebook)

        # Needs 'Staff' powers to see this page, put behind an if statement.
        #check if the user has staff privileges
        try:
            staff_mode_check = c.execute('SELECT staff_mode FROM Accounts WHERE email_address=?',(email,)).fetchall()
            staff_mode = [x[0] for x in staff_mode_check][0]
            if staff_mode == 1:
                self.BDP = BookDatabase(self.parent, self.main_notebook, email)
                self.SHP = StaffHelp(self.parent, self.main_notebook, email)

        except IndexError:
            pass

        try:
            admin_mode_check = c.execute('SELECT admin_mode FROM Accounts WHERE email_address=?',(email,)).fetchall()
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
        logout_confirmation = ms.askquestion('Logout', 'Are you sure you want to logout?', icon='warning')
        if logout_confirmation == 'yes':
            for child in self.parent.winfo_children():
                child.destroy()
            SignIn(self.parent)


if __name__ == "__main__":
    root = tk.Tk()
    rlp = SignIn(root)
    root.mainloop()

