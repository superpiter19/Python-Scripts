import sqlite3

#MAIN
conn = sqlite3.connect('PiterBet.db')

c = conn.cursor()
conn.execute('pragma foreign_keys=ON')

# Create tables
c.execute('''CREATE TABLE TFederation
             (id INTEGER PRIMARY KEY AUTOINCREMENT,name text NOT NULL UNIQUE)''')

c.execute('''CREATE TABLE TCompetition
             (id INTEGER PRIMARY KEY AUTOINCREMENT,name text NOT NULL,countryID INTEGER NOT NULL,FOREIGN KEY(countryID) REFERENCES TFederation(id) )''')

c.execute('''CREATE TABLE TTeam
             (id INTEGER PRIMARY KEY AUTOINCREMENT,name text NOT NULL UNIQUE)''')

c.execute('''CREATE TABLE TMatch
             (id INTEGER PRIMARY KEY AUTOINCREMENT,localTeamID INTEGER NOT NULL,visitorTeamID INTEGER NOT NULL,competitionID INTEGER NOT NULL,
			 date INTEGER NOT NULL, goalsLocalTeam INTEGER NOT NULL,goalsVisitorTeam INTEGER NOT NULL,
			 FOREIGN KEY(localTeamID) REFERENCES TTeam(id),FOREIGN KEY(visitorTeamID) REFERENCES TTeam(id),FOREIGN KEY(competitionID) REFERENCES TCompetition(id) )''')
			 
c.execute('''CREATE UNIQUE INDEX idx_Match ON TMatch(localTeamID,visitorTeamID,date)''')

c.execute('''CREATE TABLE TZuluBet
             (id INTEGER PRIMARY KEY AUTOINCREMENT,matchID INTEGER NOT NULL,prob1 INTEGER NOT NULL,probX INTEGER NOT NULL,prob2 INTEGER NOT NULL,
			 odd1 REAL NOT NULL,oddX REAL NOT NULL,odd2 REAL NOT NULL,stake INTEGER,
			 FOREIGN KEY(matchID) REFERENCES TMatch(id))''')

conn.commit()

'''
# Insert a row of data
#c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
c.execute("INSERT INTO TFederation(name) VALUES ('Brasil')")
c.execute("INSERT INTO TFederation(name) VALUES ('España')")
c.execute("INSERT INTO TFederation(name) VALUES ('Francia')")
c.execute("INSERT INTO TFederation(name) VALUES ('Inglaterra')")
c.execute("INSERT INTO TFederation(name) VALUES ('UEFA')")
c.execute("INSERT INTO TFederation(name) VALUES ('FIFA')")


c.execute("INSERT INTO TCompetition(name,countryID) VALUES ('Premier League',4)")
c.execute("INSERT INTO TCompetition(name,countryID) VALUES ('Championship',4)")
c.execute("INSERT INTO TCompetition(name,countryID) VALUES ('1ª División',2)")
#c.execute("INSERT INTO TCompetition(name,countryID) VALUES ('Serie A',5)")
'''



# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()