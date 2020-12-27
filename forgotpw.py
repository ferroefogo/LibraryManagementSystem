#forgot password page

import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox as ms
import string
import secrets
import re
import linecache

from email_sys import Email


conn = sqlite3.connect('LibrarySystem.db')
c = conn.cursor()

PADX = re.sub('^.*?=', '', linecache.getline('config.txt',2))
PADY = re.sub('^.*?=', '', linecache.getline('config.txt',3))
SMALL_GEOMETRY = re.sub('^.*?=','',linecache.getline('config.txt',5)).strip()
BG = re.sub('^.*?=', '', linecache.getline('config.txt',6)).strip()
DANGER_FG = re.sub('^.*?=', '', linecache.getline('config.txt',7)).strip()
HEADER_FONT = re.sub('^.*?=', '', linecache.getline('config.txt',11)).strip()

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