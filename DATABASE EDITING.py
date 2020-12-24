#For editing to the database directly
import sqlite3
with sqlite3.connect('LibrarySystem.db') as db:
      c = db.cursor()


c.execute("UPDATE Accounts SET admin_mode=1 WHERE email_address=?",('marcoff2002@gmail.com',))
db.commit()