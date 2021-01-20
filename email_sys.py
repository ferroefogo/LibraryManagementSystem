# Email class constructions

# Imports
import base64
import logging
import os
import os.path
import pickle
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient import errors
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
from datetime import datetime


class Email():
    '''
    Provides an established connection to the Google API to
    connect the organisation email to the system, so that
    various formats of emails can be sent to the user.
    '''
    def __init__(self):
        '''
        Logs the message ID and returns it.
        '''
        logging.basicConfig(
                        format="[%(levelname)s] %(message)s",
                        level=logging.INFO
                    )

    @staticmethod
    # static method allows the function to not be required to initialise the instance to be used.
    def get_service():
        """
        Gets an authorized Gmail API service instance.
        Returns:
            An authorized Gmail API service instance.
        """

        # The scopes alert the user of what the system will be doing with their address
        # Upon registration, the user will be required to authorise their account, and therefore
        # these scopes will be shown to let the user know what information the system will use.

        # The scope describes that the system will only read the email address itself
        # and send emails to said address.
        SCOPES = [
            'https://www.googleapis.com/auth/gmail.readonly',
            'https://www.googleapis.com/auth/gmail.send',
        ]

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

        # Check if token.pickle exists in the current file.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                # Load the user credentials to the system.
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                # Request another token, if it happens to be expired.
                creds.refresh(Request())
            else:
                # Pass the credentials and scopes to the authorisation process.
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                # Establish connection flow process.
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        # Construct a resource for interacting with the API
        # Pass in the credentials established previously.
        service = build('gmail', 'v1', credentials=creds)
        return service

    @staticmethod
    def send_message(service, sender, message):
        '''
        Pass in the system email address and
        constructed message (which includes the target address, service, and any other extra information that must be packed into the message)
        to send the email.

        This function is called seperately when sending an email, and must have an established API connection
        and a previously created message to be passed into this function.
        '''
        try:
            # Send the message to the target user given in the message variable.
            sent_message = (service.users().messages().send(userId='me', body=message).execute())
            logging.info('Message Id: %s', sent_message['id'])
            return sent_message
        except errors.HttpError as error:
            # Catches any connection issue and logs it back to the user.
            logging.error('An HTTP error occurred: %s', error)

    @staticmethod
    def create_admin_acc_removal_message(sender, to, subject, *args):
        """
        Create a message to be sent when the user deletes their account.
        Returns:
          An object containing a base64url encoded email object.
        """
        date_of_change = str(datetime.today().date().strftime('%d/%m/%Y'))
        string_update = "As of "+date_of_change+" your account has been removed from our systems."

        html = open("admin_delete_acc_email.html")

        soup = BeautifulSoup(html, features="lxml")
        html.close()
        target = soup.find(id='date_of_change')
        target_result = soup.find(id='date_of_change').find_all(text=True, recursive=False)
        target_text = str(target_result[0])

        for v in target:
            v.replace_with(v.replace(target_text, string_update))

        with open("admin_delete_acc_email.html", "w") as file:
            file.write(str(soup))

        updated_html = open("admin_delete_acc_email.html")

        message = MIMEText(updated_html.read(), 'html')

        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        s = message.as_string()
        b = base64.urlsafe_b64encode(s.encode('utf-8'))
        return {'raw': b.decode('utf-8')}

    @staticmethod
    def create_admin_update_acc_message(sender, to, subject, *args):
        """
        Create a message to be sent when an admin updates a target account.
        Returns:
          An object containing a base64url encoded email object.
        """
        # Extract the variables from the *args list passed in.
        staff_mode = str(args[0])
        admin_mode = str(args[1])

        if staff_mode == 1:
            staff_access = 'Enabled'
        else:
            staff_mode = 'Disabled'
        if admin_mode == 1:
            admin_access = 'Enabled'
        else:
            admin_access = 'Disabled'

        # Current date datetime object in YYYY-MM-DD.
        CURRENT_DATE = str((datetime.today().date()).strftime('%d/%m/%Y'))
        string_current_date = "As of "+CURRENT_DATE+" your account permissions have been updated."

        # Format the information into a string that will be placed on the HTML file.
        string_staff_mode = "Staff Access:: "+staff_access
        string_admin_mode = "Admin Access:: "+admin_access

        # Open the already formatted HTML email file.
        html = open("admin_update_acc_email.html")

        # Use BeautifulSoup to search through the HTML file
        # to find the correct place to substitute in the
        # variables that should be displayed in this
        # email.
        soup = BeautifulSoup(html, features="lxml")
        # Close the file.
        html.close()

        # ID list containing all the HTML <span> tag IDs
        # that will be searched for, so that their label
        # text can be changed to match the variables
        # above, such as admin_mode.
        id_list = ['date_of_change', 'admin_mode', 'staff_mode']

        # string variables assigned earlier are placed in a list to be iterated through.
        field_list = [string_current_date, string_admin_mode, string_staff_mode]

        # Iterate over the ID list with the field variable.
        for field in range(len(id_list)):

            # The current iteration will be the first element in the ID list.
            current_id = id_list[field]

            # target variable attempts to find and store
            # the correct id of the span tag in the HTML file
            target = soup.find(id=current_id)

            # Return all the text within any of the tags with the id=current_id.
            # The target_result variable stores all the text returned in a list,
            # where each element is a different string within a different tag.
            target_result = soup.find(id=current_id).find_all(text=True, recursive=False)

            # Fetch the first element in the list of target_result,
            # because there is only one HTML tag with this ID (e.g. book_title)
            target_text = str(target_result[0])

            # Store the string variable from the field_list of the current `field` iteration
            current_field = field_list[field]

            # Replace each character in the HTML tag with the string variable we want to put in.
            for v in target:
                v.replace_with(v.replace(target_text, current_field))

            # Open the HTML file and write the changes to the file.
            with open("admin_update_acc_email.html", "w") as file:
                file.write(str(soup))

        # The file is opened and the message is read from the HTML file
        # to be passed into the send_message function to be sent.
        updated_html = open("admin_update_acc_email.html")
        message = MIMEText(updated_html.read(), 'html')

        # Establish:
        #   - The target email address (to)
        #   - The system email address (from)
        #   - The subject of the message (subject)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject

        # Convert the entire message into a string format (s)
        s = message.as_string()

        # Encode the string formatted variable (s) into a byte string
        # which can then be converted into a base 64 urlsafe byte string
        b = base64.urlsafe_b64encode(s.encode('utf-8'))

        # Returns the raw decoded (b) byte string that will be passed into the
        # send_message function, so that it can send the email.
        return {'raw': b.decode('utf-8')}

    @staticmethod
    def create_acc_deletion_message(sender, to, subject, *args):
        """
        Create a message to be sent when the user deletes their account.
        Returns:
          An object containing a base64url encoded email object.
        """
        date_of_change = str(datetime.today().date().strftime('%d/%m/%Y'))
        string_update = "As of "+date_of_change+" your account has been removed from our systems."

        html = open("delete_acc_email.html")

        soup = BeautifulSoup(html, features="lxml")
        html.close()
        target = soup.find(id='date_of_change')
        target_result = soup.find(id='date_of_change').find_all(text=True, recursive=False)
        target_text = str(target_result[0])

        for v in target:
            v.replace_with(v.replace(target_text, string_update))

        with open("delete_acc_email.html", "w") as file:
            file.write(str(soup))

        updated_html = open("delete_acc_email.html")

        message = MIMEText(updated_html.read(), 'html')

        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        s = message.as_string()
        b = base64.urlsafe_b64encode(s.encode('utf-8'))
        return {'raw': b.decode('utf-8')}

    @staticmethod
    def create_pw_change_message(sender, to, subject, *args):
        """
        Create a message to be sent when the user changes their password
        Returns:
          An object containing a base64url encoded email object.
        """
        date_of_change = str(datetime.today().date().strftime('%d/%m/%Y'))
        string_update = "As of "+date_of_change+" your password has been updated."

        html = open("change_pw_email.html")

        soup = BeautifulSoup(html, features="lxml")
        html.close()
        target = soup.find(id='date_of_change')
        target_result = soup.find(id='date_of_change').find_all(text=True, recursive=False)
        target_text = str(target_result[0])

        for v in target:
            v.replace_with(v.replace(target_text, string_update))

        with open("change_pw_email.html", "w") as file:
            file.write(str(soup))

        updated_html = open("change_pw_email.html")

        message = MIMEText(updated_html.read(), 'html')

        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        s = message.as_string()
        b = base64.urlsafe_b64encode(s.encode('utf-8'))
        return {'raw': b.decode('utf-8')}

    @staticmethod
    def create_reminder_message(sender, to, subject, *args):
        '''
        Create a reminder message.

        Returns:
            An object containing a base64url encoded message.
        '''

        # Extract the variables from the *args list passed in.
        title_var = args[0]
        author_var = args[1]
        book_genre = args[2]
        date_issued = args[3]
        book_expected_return_date = args[4]

        # Current date datetime object in YYYY-MM-DD.
        CURRENT_DATE = (datetime.today().date()).strftime('%d/%m/%Y')

        # Format the information into a string that will be placed on the HTML file.
        string_book_title = "Title: "+title_var
        string_book_author = "Author: "+author_var
        string_book_genre = "Genre: "+book_genre
        string_book_date_issued = "Issue Date: "+str(date_issued)
        string_book_expected_return_date = "Expected Date of Return: "+str(book_expected_return_date)

        # Open the already formatted HTML email file.
        html = open("reminder_email.html")

        # Use BeautifulSoup to search through the HTML file
        # to find the correct place to substitute in the
        # variables that should be displayed in this
        # email.
        soup = BeautifulSoup(html, features="lxml")
        # Close the file.
        html.close()

        # ID list containing all the HTML <span> tag IDs
        # that will be searched for, so that their label
        # text can be changed to match the variables
        # above, such as title_var or author_var.
        id_list = ['book_title', 'book_author', 'book_genre', 'book_issue_date', 'book_expected_return_date', 'current_date']

        # string variables assigned earlier are placed in a list to be iterated through.
        field_list = [string_book_title, string_book_author, string_book_genre, string_book_date_issued, string_book_expected_return_date, CURRENT_DATE]

        # Iterate over the ID list with the field variable.
        for field in range(len(id_list)):

            # The current iteration will be the first element in the ID list.
            current_id = id_list[field]

            # target variable attempts to find and store
            # the correct id of the span tag in the HTML file
            target = soup.find(id=current_id)

            # Return all the text within any of the tags with the id=current_id.
            # The target_result variable stores all the text returned in a list,
            # where each element is a different string within a different tag.
            target_result = soup.find(id=current_id).find_all(text=True, recursive=False)

            # Fetch the first element in the list of target_result,
            # because there is only one HTML tag with this ID (e.g. book_title)
            target_text = str(target_result[0])

            # Store the string variable from the field_list of the current `field` iteration
            current_field = field_list[field]

            # Replace each character in the HTML tag with the string variable we want to put in.
            for v in target:
                v.replace_with(v.replace(target_text, current_field))

            # Open the HTML file and write the changes to the file.
            with open("reminder_email.html", "w") as file:
                file.write(str(soup))

        # The file is opened and the message is read from the HTML file
        # to be passed into the send_message function to be sent.
        updated_html = open("reminder_email.html")
        message = MIMEText(updated_html.read(), 'html')

        # Establish:
        #   - The target email address (to)
        #   - The system email address (from)
        #   - The subject of the message (subject)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject

        # Convert the entire message into a string format (s)
        s = message.as_string()

        # Encode the string formatted variable (s) into a byte string
        # which can then be converted into a base 64 urlsafe byte string
        b = base64.urlsafe_b64encode(s.encode('utf-8'))

        # Returns the raw decoded (b) byte string that will be passed into the
        # send_message function, so that it can send the email.
        return {'raw': b.decode('utf-8')}

    @staticmethod
    def create_verification_message(sender, to, subject, verification_code):
        """
        Create a verification message.
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
            v.replace_with(v.replace(target_text, verification_code))

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
        """
        Create a forgot password message for an email.
        Returns:
          An object containing a base64url encoded email.
        """
        html = open("forgot_password_email.html")

        soup = BeautifulSoup(html, features="lxml")
        html.close()
        target = soup.find(id='random_password')
        target_result = soup.find(id='random_password').find_all(text=True, recursive=False)
        target_text = str(target_result[0])

        for v in target:
            v.replace_with(v.replace(target_text, gen_random_password))

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

    @staticmethod
    def create_issuing_message(sender, to, subject, *args):
        """
        Create an issuing message for an email
        Returns:
            An object containing a base64url encoded email.
        """
        title_var = args[0]
        author_var = args[1]
        book_genre = args[2]
        book_location = args[3]
        date_issued = args[4]
        book_expected_return_date = args[5]

        string_book_title = "Title: "+title_var
        string_book_author = "Author: "+author_var
        string_book_genre = "Genre: "+book_genre
        string_book_location = "Location: "+book_location
        string_book_date_issued = "Issue Date: "+str(date_issued)
        string_book_expected_return_date = "Expected Date of Return: "+str(book_expected_return_date)

        html = open("issuing_email.html")

        soup = BeautifulSoup(html, features="lxml")
        html.close()

        id_list = ['book_title', 'book_author', 'book_genre', 'book_location', 'book_issue_date', 'book_expected_return_date']
        field_list = [string_book_title, string_book_author, string_book_genre, string_book_location, string_book_date_issued, string_book_expected_return_date]

        for field in range(len(id_list)):
            current_id = id_list[field]
            target = soup.find(id=current_id)
            target_result = soup.find(id=current_id).find_all(text=True, recursive=False)
            target_text = str(target_result[0])
            current_field = field_list[field]

            for v in target:
                v.replace_with(v.replace(target_text, current_field))

            with open("issuing_email.html", "w") as file:
                file.write(str(soup))

        updated_html = open("issuing_email.html")

        message = MIMEText(updated_html.read(), 'html')

        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        s = message.as_string()
        b = base64.urlsafe_b64encode(s.encode('utf-8'))
        return {'raw': b.decode('utf-8')}

    @staticmethod
    def create_return_message(sender, to, subject, *args):
        """
        Create an return message for an email
        Returns:
            An object containing a base64url encoded email.
        """
        title_var = args[0]
        author_var = args[1]
        book_genre = args[2]
        book_location = args[3]
        date_issued = args[4]
        book_expected_return_date = args[5]
        book_actual_return_date = args[6]

        string_book_title = "Title: "+title_var
        string_book_author = "Author: "+author_var
        string_book_genre = "Genre: "+book_genre
        string_book_location = "Location: "+book_location
        string_book_date_issued = "Issue Date: "+str(date_issued)
        string_book_expected_return_date = "Expected Date of Return: "+str(book_expected_return_date)
        string_book_actual_return_date = "Actual Date of Return: "+str(book_actual_return_date)

        html = open("return_email.html")

        soup = BeautifulSoup(html, features="lxml")
        html.close()

        id_list = ['book_title', 'book_author', 'book_genre', 'book_location', 'book_issue_date', 'book_expected_return_date', 'book_actual_return_date']
        field_list = [string_book_title, string_book_author, string_book_genre, string_book_location, string_book_date_issued, string_book_expected_return_date, string_book_actual_return_date]

        for field in range(len(id_list)):
            current_id = id_list[field]
            target = soup.find(id=current_id)
            target_result = soup.find(id=current_id).find_all(text=True, recursive=False)
            target_text = str(target_result[0])
            current_field = field_list[field]

            for v in target:
                v.replace_with(v.replace(target_text, current_field))

            with open("return_email.html", "w") as file:
                file.write(str(soup))

        updated_html = open("return_email.html")

        message = MIMEText(updated_html.read(), 'html')

        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        s = message.as_string()
        b = base64.urlsafe_b64encode(s.encode('utf-8'))
        return {'raw': b.decode('utf-8')}
