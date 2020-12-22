#Account Page

import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox as ms
import bcrypt
import sys

from email_sys import Email




conn = sqlite3.connect('LibrarySystem.db')
c = conn.cursor()

width=225
padx=8
pady=5

geometry = '1500x1500'
bg='gray90'
font='System 18'

class Account():
    #USER ACCESS
    #Display logged in user information.
    def __init__(self, root, notebook, current_user_email):
        self.user_email= current_user_email

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


        #Password entry
        self.pw_container = tk.Frame(self.delete_account_container, bg=bg)
        self.pw_label = tk.Label(self.pw_container, text='Password:',bg=bg)
        

        self.pw_var = tk.StringVar()
        self.pw_entry = ttk.Entry(self.pw_container, textvariable=self.pw_var, show='*')
        

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

        email_label = tk.Label(email_container, text='   Email:   {}'.format(self.user_email), padx=padx, pady=pady)
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

            #Check if the current password entered matches the one stored in the database

            #Hash the password to check against the database one
            db_current_pw_fetch = c.execute('SELECT password FROM Accounts WHERE email_address = ?', (self.user_email,))
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
            with sqlite3.connect('LibrarySystem.db') as db:
                c = db.cursor()
            delete_account = c.execute("DELETE FROM Accounts WHERE email_address = ?",(self.user_email,))
            db.commit()
            ms.showinfo('Success','Account Deleted')

            #exit system upon account deletion
            ms.showinfo('Deletion Notice','The system will now shutdown upon deletion')
            sys.exit()


    def change_password_container_func(self, *args):
        #If the user has pressed the button after the widgets were already packed, unpack them.
        if self.change_password_container.winfo_ismapped() == True:
            #May be able to just use a for loop that iterates over child widget using winfo_children().
            self.change_password_container.pack_forget()
            self.container_change_password_header.pack_forget()
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
            self.pw_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)
            self.pw_label.pack(side=tk.LEFT, anchor=tk.W, fill=tk.X, padx=padx, pady=pady)
            self.pw_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)
            self.confirm_pw_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)
            self.confirm_pw_label.pack(side=tk.LEFT, anchor=tk.W, fill=tk.X, padx=padx, pady=pady)
            self.confirm_pw_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=padx, pady=pady)
            self.delete_account_button_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)
            self.delete_account_button.pack(side=tk.LEFT, anchor=tk.W, padx=padx, pady=pady)