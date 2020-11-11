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
import random

    
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

def send_message(service, sender, message):
    try:
      sent_message = (service.users().messages().send(userId='me', body=message)
               .execute())
      logging.info('Message Id: %s', sent_message['id'])
      return sent_message
    except errors.HttpError as error:
      logging.error('An HTTP error occurred: %s', error)

def create_message(sender, to, subject, verification_code):
    html = open("verification_email.html")

    
    from bs4 import BeautifulSoup
    import re
 
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

if __name__ == '__main__':
    logging.basicConfig(
        format="[%(levelname)s] %(message)s",
        level=logging.INFO
    )
    verification_code = ''
    i=0
    while i<6:
        random_integer = random.SystemRandom().randint(0,9)
        i+=1
        verification_code += str(random_integer)

    try:
        service = get_service()
        message = create_message("from@gmail.com", "marcoff2002@hotmail.com", "Books4All Verification Code", verification_code)
        send_message(service, "from@gmail.com", message)

    except Exception as e:
        logging.error(e)
        raise

