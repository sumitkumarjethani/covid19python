import sqlite3

conn = sqlite3.connect('covid.sqlite')
cur = conn.cursor()
print('This file will show only the last five days of every country.')

cur.execute('''SELECT id,name FROM Country''')
country_ids = cur.fetchall()
for country in country_ids:
    print('----------------------------------------------------------------------------')
    cur.execute('''SELECT cases,deaths,day,month,year FROM Daily_data WHERE id_country=?
                ORDER BY year DESC, month DESC, day DESC LIMIT 5''',(country[0],))
    rows = cur.fetchall()
    for row in rows:
        print(country[1],"cases:",row[0],"deaths:",row[1],"date:",str(row[2])+"/"+str(row[3])+"/"+str(row[4]))
        
    

