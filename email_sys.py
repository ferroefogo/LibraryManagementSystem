#Email class constructions
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
import sys


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
    def create_reminder_message(sender, to, subject, *args):
        """Create a reminder message.

        Returns:
            An object containing a base64url encoded message.
        """

        title_var = args[0]
        author_var = args[1]
        book_genre = args[2]
        date_issued = args[3]
        book_expected_return_date = args[4]

        CURRENT_DATE = (datetime.today().date()).strftime('%Y-%m-%d')

        string_book_title = "Title: "+title_var
        string_book_author = "Author: "+author_var
        string_book_genre = "Genre: "+book_genre
        string_book_date_issued = "Issue Date: "+str(date_issued)
        string_book_expected_return_date = "Expected Date of Return: "+str(book_expected_return_date)

        html = open("reminder_email.html")

        soup = BeautifulSoup(html, features="lxml")
        html.close()

        id_list = ['book_title','book_author','book_genre','book_issue_date','book_expected_return_date', 'current_date']
        field_list = [string_book_title,string_book_author,string_book_genre,string_book_date_issued,string_book_expected_return_date, CURRENT_DATE]

        for field in range(len(id_list)):
            current_id = id_list[field]
            target = soup.find(id=current_id)
            target_result = soup.find(id=current_id).find_all(text=True, recursive=False)
            target_text = str(target_result[0])
            current_field = field_list[field]

            for v in target:
                v.replace_with(v.replace(target_text, current_field))

            with open("reminder_email.html", "w") as file:
                file.write(str(soup))

        updated_html = open("reminder_email.html")

        message = MIMEText(updated_html.read(), 'html')

        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        s = message.as_string()
        b = base64.urlsafe_b64encode(s.encode('utf-8'))
        return {'raw': b.decode('utf-8')}

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
          An object containing a base64url encoded email.
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

    @staticmethod
    def create_issuing_message(sender, to, subject, *args):
        """Create an issuing message for an email
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

        id_list = ['book_title','book_author','book_genre','book_location','book_issue_date','book_expected_return_date']
        field_list = [string_book_title,string_book_author,string_book_genre,string_book_location,string_book_date_issued,string_book_expected_return_date]

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
        """Create an return message for an email
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

        id_list = ['book_title','book_author','book_genre','book_location','book_issue_date','book_expected_return_date','book_actual_return_date']
        field_list = [string_book_title,string_book_author,string_book_genre,string_book_location,string_book_date_issued,string_book_expected_return_date,string_book_actual_return_date]

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