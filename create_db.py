from sqlite3 import connect

conn = connect('LibrarySystem.db')
c = conn.cursor()


c.execute("""CREATE TABLE Accounts (
			user_id INTEGER PRIMARY KEY,
			email_address NVARCHAR(320) NOT NULL DEFAULT '',
			password VARCHAR(60) NOT NULL DEFAULT '',
			staff_mode INTEGER NOT NULL DEFAULT 0,
			admin_mode INTEGER NOT NULL DEFAULT 0
			)""")
conn.commit()


c.execute("""CREATE TABLE Books (
			bookID INTEGER PRIMARY KEY,
			title VARCHAR(100) NOT NULL DEFAULT '',
			author VARCHAR(100) NOT NULL DEFAULT '',
			genre VARCHAR(100) NOT NULL DEFAULT '',
			location char(1) NOT NULL DEFAULT '',
			issued INTEGER NOT NULL DEFAULT 0,
			FOREIGN KEY(genre) REFERENCES Genres(genre)
			)""")
conn.commit()

c.execute("""CREATE TABLE MyBooks (
			user_id INTEGER NOT NULL DEFAULT '',
			bookID INTEGER NOT NULL DEFAULT '',
			date_issued TIMESTAMP NOT NULL DEFAULT '',
			return_date TIMESTAMP NOT NULL DEFAULT '',
			FOREIGN KEY(bookID) REFERENCES Books(bookID),
			FOREIGN KEY(user_id) REFERENCES Accounts(user_id)
			)""")
conn.commit()

c.execute("""CREATE TABLE Genres (
			genre VARCHAR(100) NOT NULL DEFAULT '-EMPTY-'
			)""")
conn.commit()

c.execute("""CREATE TABLE NoAccountBookInfo (
			 bookID INTEGER PRIMARY KEY,
			 date_issued TIMESTAMP NOT NULL DEFAULT '',
			 return_date TIMESTAMP NOT NULL DEFAULT '',
			 FOREIGN KEY(bookID) REFERENCES Books(bookID)
			 )
		  """)

c.execute("INSERT INTO Genres VALUES('-EMPTY-')")
conn.commit()
