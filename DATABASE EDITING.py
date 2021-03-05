#For editing to the database directly
import sqlite3
with sqlite3.connect('LibrarySystem.db') as db:
      c = db.cursor()



c.execute("INSERT INTO Books VALUES(1, 'TheOne', 'Me', 'Tutorial', 'T', 0)")
db.commit()