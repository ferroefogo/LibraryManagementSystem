# For editing to the database directly
import sqlite3
with sqlite3.connect('LibrarySystem.db') as db:
      c = db.cursor()
user_id=2
check_admin = c.execute("UPDATE Accounts SET admin_mode=0, staff_mode=1 WHERE user_id=?", (user_id,))
db.commit()
print(check_admin)