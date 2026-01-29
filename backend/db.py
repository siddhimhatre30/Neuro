import csv
import sqlite3

conn = sqlite3.connect('neuro.db')
cursor = conn.cursor()

#query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
#cursor.execute(query)

#query = "INSERT INTO sys_command VALUES (null,'C drive', 'C:\\')"
#cursor.execute(query)
#conn.commit()
query = "CREATE TABLE IF NOT EXISTS file_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)

query = "INSERT INTO file_command VALUES (null,'screenshots', 'C:\\Users\\LENOVO\\OneDrive\\画像\\Screenshots')"
cursor.execute(query)
conn.commit()
#query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
#cursor.execute(query)

#query = "INSERT INTO web_command VALUES (null,'whatsapp', 'https://web.whatsapp.com/')"
#cursor.execute(query)
#conn.commit()

# testing module
#app_name = "android studio"
#cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
#results = cursor.fetchall()
#print(results[0][0])

# Create a table with the desired columns
#cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL,address VARCHAR(255) NULL)''')

# Specify the column indices you want to import (0-based index)
#desired_columns_indices = [0, 18]

# # Read data from CSV and insert into SQLite table for the desired columns
#with open('Contact.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         selected_data = [row[i] for i in desired_columns_indices]
#         cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# # Commit changes and close connection
#conn.commit()
#conn.close()

#query = 'Pranav'
#query = query.strip().lower()

#cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
#results = cursor.fetchall()
#print(results[0][0])

# Adding personal info table
#query = "CREATE TABLE IF NOT EXISTS info(name VARCHAR(100), designation VARCHAR(50),mobileno VARCHAR(40), email VARCHAR(200), city VARCHAR(300))"
#cursor.execute(query)

# Add Column in contacts table
#cursor.execute("ALTER TABLE contacts ADD COLUMN address VARCHAR(255)")