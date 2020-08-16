import sqlite3

conn = sqlite3.connect('covid.sqlite')
cur = conn.cursor()

cur.executescript('''
    DROP TABLE Country;
    DROP TABLE Continent;
    DROP TABLE Daily_data;
    ''')
conn.commit()

