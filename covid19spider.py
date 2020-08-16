import urllib.request, urllib.parse, urllib.error
import json
import sqlite3
import datetime
import sys
import re

def main():
    conn = sqlite3.connect('covid.sqlite')
    cur = conn.cursor()
    
    cur.executescript('''
    CREATE TABLE IF NOT EXISTS Continent (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT UNIQUE NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS Country (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT UNIQUE NOT NULL,
        id_continent INTEGER NOT NULL,
        population_2019 INTEGER NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS Daily_data (
        id_country INTEGER NOT NULL,
        id_continent INTEGER NOT NULL,
    	day INTEGER NOT NULL,
        month INTEGER NOT NULL,
        year INTEGER NOT NULL,
    	cases INTEGER NOT NULL,
    	deaths INTEGER NOT NULL,
    	cumulative_number_per_100000 INTEGER NOT NULL,
    	PRIMARY KEY (id_continent,id_country,day,month,year)
    );
    
    INSERT OR IGNORE INTO Continent (name) VALUES ('Europe');
    INSERT OR IGNORE INTO Continent (name) VALUES ('America');
    INSERT OR IGNORE INTO Continent (name) VALUES ('Asia');
    INSERT OR IGNORE INTO Continent (name) VALUES ('Africa');
    INSERT OR IGNORE INTO Continent (name) VALUES ('Oceania');
    ''')
    
    conn.commit()
    
    print('Retrieving covid-19 data. Will take some seconds')
    try:    
        uh = urllib.request.urlopen('https://opendata.ecdc.europa.eu/covid19/casedistribution/json/')
    except:
        print("Unable to retrieve or parse web page")
        quit()
        
    try:
        data = uh.read().decode()
    except KeyboardInterrupt:
        print('Program interrupt by the user.')
        quit()
    
    js = json.loads(data)
    cur.execute('''SELECT * FROM Daily_data''')
    row = cur.fetchone()
    if row is None:
        print('STARTING TO INSERT IN THE DB:')
        retrieve_all_data(conn,cur,js)
    #We will suppose that the database has data and will try to put
    #the recent data (daily) if it is not in yet. 
    #The user can put a input date if he wants to retrieve some specific date data.
    #For example for spain on 15/08/2020 they put the 14/08/2020 data
    else:
        actual_date = datetime.datetime.now()
        format1 = "%d/%m/%Y"
        actual_date = actual_date.strftime(format1)
        if len(sys.argv) == 3 and sys.argv[1] == "-date" and sys.argv[2] != "":
            date = re.findall('[\d]{2}/[\d]{2}/[\d]{4}', sys.argv[2])
            if len(date) > 0:
                print('STARTING TO INSERT THE MENTIONED DATA IN THE DB:')
                retrieve_recent_data(conn, cur, js, date[0])
            else:
                print('STARTING TO INSERT THE RECENT DATA IN THE DB:')
                retrieve_recent_data(conn,cur,js,actual_date)
        else:
            print('STARTING TO INSERT THE RECENT DATA IN THE DB:')
            retrieve_recent_data(conn,cur,js,actual_date)

# Will put the recent date if it is not yet
def retrieve_recent_data(conn,cur,js,actual_date):
    print('Will only put the date:', actual_date)
    cur.execute('''SELECT id,id_continent,name FROM Country''')
    current_date = actual_date.split('/')
    country_ids = cur.fetchall()
    for country in country_ids:
        id_country = country[0]
        id_continent = country[1]
        name = country[2]
        cur.execute('''SELECT day,month,year FROM Daily_data WHERE id_country=?''',
                    (id_country,))
        dates = cur.fetchall()
        found = False
        for date in dates:
            if int(current_date[0]) == int(date[0]) and int(current_date[1]) == int(date[1]) and int(current_date[2]) == int(date[2]):
                found = True
                break
        if found: continue
        num = insert_recent_data(conn,cur,js,id_country,id_continent,name,actual_date)
        if num > 0:
            print(name,'updated in the DB with the recent data.')
        else:
            print(name,'already updated in the DB with the recent data.')

def insert_recent_data(conn,cur,js,id_country,id_continent,name,actual_date):
    for entry in js['records']:
        if entry['countriesAndTerritories'] != name: continue
        if entry['dateRep'] != actual_date: continue
        day = int(entry['day'])
        month = int(entry['month'])
        year = int(entry['year'])
        cases = entry['cases']
        deaths = entry['deaths']
        cumulative_number_per_100000 = entry['Cumulative_number_for_14_days_of_COVID-19_cases_per_100000']
        cur.execute('''
                    INSERT OR IGNORE INTO Daily_data (id_country,id_continent,
                    day,month,year,cases,deaths,cumulative_number_per_100000) 
                    VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)''', 
                    (id_country, id_continent, day, month, year,
                     cases, deaths, cumulative_number_per_100000))
        conn.commit()
        return 1
    return 0

# if there is no data in the sqlite file it will put all the data
def retrieve_all_data(conn,cur,js):
    last_name = None
    for entry in js['records']:
        name = entry['countriesAndTerritories']
        continent = entry['continentExp']
        if last_name is not None and last_name != name and continent != "Other":
            print (last_name,'inserted in DB.')
        if continent == "Other": continue
        population_2019 = entry['popData2019']
        cur.execute('''SELECT id FROM Continent WHERE name=?''',(continent,))
        id_continent = cur.fetchone()[0]
        cur.execute('''
                    INSERT OR IGNORE INTO Country (name,id_continent,population_2019) 
                    VALUES ( ?, ?, ?)''', ( name, id_continent, population_2019) )
        cur.execute('''SELECT id FROM Country WHERE name=?''',(name,))
        id_country = cur.fetchone()[0]
        day = int(entry['day'])
        month = int(entry['month'])
        year = int(entry['year'])
        cases = entry['cases']
        deaths = entry['deaths']
        cumulative_number_per_100000 = entry['Cumulative_number_for_14_days_of_COVID-19_cases_per_100000']
        cur.execute('''
                    INSERT OR IGNORE INTO Daily_data (id_country,id_continent,
                    day,month,year,cases,deaths,cumulative_number_per_100000) 
                    VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)''', 
                    ( id_country, id_continent, day, month, year, 
                     cases, deaths, cumulative_number_per_100000) )
        last_name = name
    print (last_name,'inserted in DB.')
    conn.commit()

main()