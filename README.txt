-Y2 Project-
===Library Management System===
+/**
+CONTENTS
+---------
+1. Introduction
+2. Requirements
+3. Configuration/Testing
+4. API Connection
+5. Regards
+----------------
+1. Introduction
+----------------
+ The Library Management System allows multiple access levels of users to utilise a system that is tailored to their needs.
+ A staff member will be able to issue/return/add/remove books, as well as add/remove books from the system.
+ An admin will be able to view and manipulate accounts in the system, as well as view analytical statistics regarding the performance
+ of the system with its users.
+----------------
+2. Requirements
+----------------
+ Must be ran on python 3.x
+ The program requires the following 
+ list of external modules to function:
+                  - sqlite3
+                  - bcrypt
+                  - re
+                  - linecache
+                  - numpy
+                  - matplotlib
+                  - collections
+                  - tkcalendar
+                  - dateutil
+                  - email
+                  - googleapiclient
+                  - google-auth
+                  - google-auth-oauthlib
+                  - beautifulsoup4
+ All that is externally required from the main.py that is ran is all of its contributing files within the folder, such as the .db file.
+-------------------------
+3. Configuration/Testing
+-------------------------
+ Those who might want to test the database, or look to see how it was made can open the create_db.py
+ file in IDLE mode to show the database creation code.
+
+ To create a new fresh database, the standard LibrarySystem.db that comes with the system can be deleted, and the create_db.py
+ file must be ran.
+
+ The config.txt file is required to save the settings required for the construction of the GUI.
+
+ The .html files are design formats for the information that will be sent by the system, via email.
+
+ The mean_avg_storage.txt is required to store values related to the analytical statistics for the admins.
+-------------------------
+4. API Connection
+ The Google API is used to send the emails using an outside, previously setup gmail account by me, specifically meant for this.
+ The credentials.json and token.pickle are related to the API to store the Google Project credentials, so that the system is able to connect
+ and manipulate the gmail account mentioned previously. Under normal circumstances, these two files would be hidden from public view to avoid
+ hackers using the client secret and other information, mainly from the credentials.json, to access the gmail account and manipulate the account
+ for nefarious deeds;however, the systems source code will remain in a private setting, therefore it can be shown.
+-----------
+5. Regards
+-----------
+ Made by Marco Fernandes
+ Developed for Books4All Broadfield Library
+ On Python 3.7.4
+-------------------------