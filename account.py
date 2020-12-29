#Account Page

#Imports
import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox as ms
import bcrypt
import sys
import re
import linecache

#File Import
from email_sys import Email



#Connect to database
with sqlite3.connect('LibrarySystem.db') as db:
    c = db.cursor()

#File Configurations
PADX = re.sub('^.*?=', '', linecache.getline('config.txt',2))
PADY = re.sub('^.*?=', '', linecache.getline('config.txt',3))
BG = re.sub('^.*?=', '', linecache.getline('config.txt',6)).strip()
DANGER_FG = re.sub('^.*?=', '', linecache.getline('config.txt',7)).strip()
LINK_FG = re.sub('^.*?=', '', linecache.getline('config.txt',8)).strip()
FONT = re.sub('^.*?=', '', linecache.getline('config.txt',10)).strip()
HEADER_FONT = re.sub('^.*?=', '', linecache.getline('config.txt',11)).strip()

class Account():
    '''
    Access Level: USER
    Functions: Display user-specific information regarding the currently logged in user.
    '''
    def __init__(self, root, notebook, current_user_email):
        '''
        Used for the initialisation of the visual aspect of the system.
        '''
        #Class Variables
        self.user_email = current_user_email

        #Notebook Page Addition
        account_page = tk.Frame(notebook)
        notebook.add(account_page, text='Account')

        #Account Header
        header_frame = tk.Frame(account_page)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        header = tk.Label(header_frame, text='Account', font=HEADER_FONT)
        header.pack(side=tk.TOP)

        # Account Details Frame
        details_container = tk.Frame(account_page, bg=BG)
        details_container.pack(side=tk.LEFT, anchor=tk.N)

        container_header = tk.Label(details_container, text='Account Details', font=FONT, bg=BG)
        container_header.pack(anchor=tk.W, padx=PADX, pady=PADY)


        #Change password Container
        self.change_password_container = tk.Frame(account_page, bg=BG)
        self.container_change_password_header = tk.Label(self.change_password_container, text='Change Password', font=FONT, bg=BG)
        

        #Current password entry
        self.current_pw_container = tk.Frame(self.change_password_container, bg=BG)
        self.current_pw_label = tk.Label(self.current_pw_container, text='Current Password:',bg=BG)
        

        self.current_pw_var = tk.StringVar()
        self.current_pw_entry = ttk.Entry(self.current_pw_container, textvariable=self.current_pw_var, show='*')
        

        #New password entry
        self.new_pw_container = tk.Frame(self.change_password_container, bg=BG)
        self.new_pw_label = tk.Label(self.new_pw_container, text='New Password:',bg=BG)
        

        self.new_pw_var = tk.StringVar()
        self.new_pw_entry = ttk.Entry(self.new_pw_container, textvariable=self.new_pw_var, show='*')


        #New password confirmation entry
        self.new_pw_confirm_container = tk.Frame(self.change_password_container, bg=BG)
        self.new_pw_confirm_label = tk.Label(self.new_pw_confirm_container, text='Confirm New Password:',bg=BG)
        

        self.new_pw_confirm_var = tk.StringVar()
        self.new_pw_confirm_entry = ttk.Entry(self.new_pw_confirm_container, textvariable=self.new_pw_confirm_var, show='*')
        

        #Change password button
        self.change_password_button_container = tk.Frame(self.change_password_container, bg=BG)
        self.change_password_button = ttk.Button(self.change_password_button_container, text='Change Password', command=lambda:self.change_password())


        #Delete Account Container
        self.delete_account_container = tk.Frame(account_page, bg=BG)
        self.container_delete_account_header = tk.Label(self.delete_account_container, text='Delete Account', font=FONT, bg=BG)


        #Password entry
        self.pw_container = tk.Frame(self.delete_account_container, bg=BG)
        self.pw_label = tk.Label(self.pw_container, text='Password:',bg=BG)
        

        self.pw_var = tk.StringVar()
        self.pw_entry = ttk.Entry(self.pw_container, textvariable=self.pw_var, show='*')
        

        #New password entry
        self.confirm_pw_container = tk.Frame(self.delete_account_container, bg=BG)
        self.confirm_pw_label = tk.Label(self.confirm_pw_container, text='Confirm Password:',bg=BG)
        

        self.confirm_pw_var = tk.StringVar()
        self.confirm_pw_entry = ttk.Entry(self.confirm_pw_container, textvariable=self.confirm_pw_var, show='*')


        #Delete account button
        self.delete_account_button_container = tk.Frame(self.delete_account_container, bg=BG)
        self.delete_account_button = ttk.Button(self.delete_account_button_container, text='Delete Account', command=lambda:self.deletion_confirmation())


        email_container = tk.Frame(details_container, bg=BG)
        email_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)

        email_label = tk.Label(email_container, text='   Email:   {}'.format(self.user_email), padx=PADX, pady=PADY)
        email_label.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

        change_password_label = tk.Label(details_container, text='Change Password?', cursor="hand2",
                                                bg=BG, fg=LINK_FG)
        change_password_label.pack(anchor=tk.W, padx=PADX, pady=PADY)
        change_password_label.bind("<Button-1>", lambda e: self.change_password_container_func())

        delete_account_label = tk.Label(details_container, text='Delete Account?', cursor="hand2",
                                                bg=BG, fg=DANGER_FG)
        delete_account_label.pack(anchor=tk.W, padx=PADX, pady=PADY)
        delete_account_label.bind("<Button-1>", lambda e: self.delete_account_container_func())

    def change_password(self, *args):
        '''
        Functions: Change the user password in the database.
        '''
        change_password_confirmation = ms.askquestion('Change Password', 'Are you sure you want to change password?')
        if change_password_confirmation == 'yes':

            #Fetch entry field variables.
            current_pw = self.current_pw_var.get()
            new_pw = self.new_pw_var.get()
            confirm_new_pw = self.confirm_pw_var.get()

            #Check if the new password field matches the confirm password field
            if new_pw != confirm_new_pw:
                ms.showerror('Error','New password and confirm password fields do not match.')
            elif new_pw == confirm_new_pw:
                #Check if the current password entered matches the one stored in the database
                #Hash the password to check against the database one
                db_current_pw_fetch = c.execute('SELECT password FROM Accounts WHERE email_address = ?', (self.user_email,))
                db_current_pw = c.fetchone()[0]

                #Password stored in database
                db_current_pw_encode = db_current_pw.encode('utf-8')

                #Password user has just typed in, converted into bytes literal to be checked using the bcrypt hash check function.
                bytes_current_pw = bytes(current_pw, 'utf-8')
                
                if bcrypt.checkpw(bytes_current_pw, db_current_pw_encode):
                    #Encrypt+Salt New PW
                    hashable_new_pw = bytes(new_pw, 'utf-8')
                    hashed_new_pw = bcrypt.hashpw(hashable_new_pw, bcrypt.gensalt())

                    #Convert into base64string
                    db_hashed_pw = hashed_new_pw.decode("utf-8")

                    #Update password in database to fit the new password and its hash
                    db_new_pw_update = c.execute('UPDATE Accounts SET password=? WHERE email_address=?',(db_hashed_pw, self.user_email))
                    db.commit()

                    ms.showinfo('Success','Password has updated!')

                    #Set all fields to be empty
                    self.current_pw_var.set('')
                    self.new_pw_var.set('')
                    self.confirm_pw_var.set('')
                else:
                    ms.showerror('Error','Current password does not match.')

    def deletion_confirmation(self, *args):
        '''
        Functions: Delete the user account from the database.
        '''
        account_deletion_confirmation = ms.askquestion('Account Deletion', 'Are you sure you want to delete your account?\n\nYou will not be able to recover any information saved on this account.\nAll personal information associated to this account will be deleted permanently.')
        if account_deletion_confirmation == 'yes':
            #Unlink any books connected to this account and make them available.
            #Must also delete the user from the MyBooks table.

            db_check_linked_books_fetch = c.execute('SELECT bookID FROM MyBooks WHERE user_id=(SELECT user_id FROM Accounts WHERE email_address=?)',(self.user_email,)).fetchall()
            db_check_linked_books = [x[0] for x in db_check_linked_books_fetch]
            if len(db_check_linked_books) != 0:
                #Must unlink the books and delete the MyBooks user_id entry.
                for i in range(len(db_check_linked_books)):
                    update_book_status = c.execute('UPDATE Books SET issued=0 WHERE bookID=?',(db_check_linked_books[i],))

                #Delete MyBooks row of this user.
                remove_mybooks = c.execute('DELETE FROM MyBooks WHERE user_id=?',(user_id,))
                db.commit()
            
            #Delete the account row where the current email address is signed in under.
            delete_account = c.execute("DELETE FROM Accounts WHERE email_address = ?",(self.user_email,))
            db.commit()

            ms.showinfo('Success','Account Deleted')

            #exit system upon account deletion
            ms.showinfo('Deletion Notice','The system will now shutdown upon deletion')
            sys.exit()


    def change_password_container_func(self, *args):
        #If the user has pressed the button after the widgets were already packed, unpack them.
        if self.change_password_container.winfo_ismapped() == True:
            #Iterates over each widget in the password change frame, hiding each one from view.
            for child in self.change_password_container.winfo_children():
                child.pack_forget()
            self.change_password_container.pack_forget()
        else:
            #Pack all the widgets upon the user pressing the button, only if the widgets are not currently packed.
            #Must be done manually because each widget requires a specific parameters to sit in the frame correctly.
            self.change_password_container.pack(side=tk.LEFT, anchor=tk.N)
            self.container_change_password_header.pack(anchor=tk.W, padx=PADX, pady=PADY)
            self.current_pw_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)
            self.current_pw_label.pack(side=tk.LEFT, anchor=tk.W, fill=tk.X, padx=PADX, pady=PADY)
            self.current_pw_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)
            self.new_pw_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)
            self.new_pw_label.pack(side=tk.LEFT, anchor=tk.W, fill=tk.X, padx=PADX, pady=PADY)
            self.new_pw_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)
            self.new_pw_confirm_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)
            self.new_pw_confirm_label.pack(side=tk.LEFT, anchor=tk.W, fill=tk.X, padx=PADX, pady=PADY)
            self.new_pw_confirm_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)
            self.change_password_button_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)
            self.change_password_button.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)

    def delete_account_container_func(self, *args):
        #If the user has pressed the button after the widgets were already packed, unpack them.
        if self.delete_account_container.winfo_ismapped() == True:
            #Iterates over each widget in the password change frame, hiding each one from view.
            for child in self.delete_account_container.winfo_children():
                child.pack_forget()
            self.delete_account_container.pack_forget()
        else:
            #Pack all the widgets to show the panel upon pressing the delete_account box in account details, only if the widgets are not currently packed.
            #Must be done manually because each widget requires a specific parameters to sit in the frame correctly.
            self.delete_account_container.pack(side=tk.LEFT, anchor=tk.N)
            self.container_delete_account_header.pack(anchor=tk.W, padx=PADX, pady=PADY)
            self.pw_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)
            self.pw_label.pack(side=tk.LEFT, anchor=tk.W, fill=tk.X, padx=PADX, pady=PADY)
            self.pw_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)
            self.confirm_pw_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)
            self.confirm_pw_label.pack(side=tk.LEFT, anchor=tk.W, fill=tk.X, padx=PADX, pady=PADY)
            self.confirm_pw_entry.pack(side=tk.RIGHT, anchor=tk.E, padx=PADX, pady=PADY)
            self.delete_account_button_container.pack(anchor=tk.W, fill=tk.X, expand=True, side=tk.TOP)
            self.delete_account_button.pack(side=tk.LEFT, anchor=tk.W, padx=PADX, pady=PADY)