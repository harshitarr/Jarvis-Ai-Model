import csv
import sqlite3

con = sqlite3.connect("jarvis.db")

cursor = con.cursor()

query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100),path VARCHAR(1000))"
cursor.execute(query)


# query = "INSERT INTO sys_command VALUES (null,'spotify','')"
# cursor.execute(query)
# con.commit()

# query = "DELETE FROM sys_command WHERE name = 'spotify'"
# cursor.execute(query)
# con.commit()

# query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100),path VARCHAR(1000))"
# cursor.execute(query)

# query = "INSERT INTO web_command VALUES (null,'linkedin','https://linkedin.com/')"
# cursor.execute(query)
# con.commit()

#query = "DELETE FROM web_command WHERE name = 'linked in'"
#cursor.execute(query)
#con.commit()

#Create a table with the desired columns
#cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')

desired_columns_indices = [0, 20]  # these are actually the column number in the excel sheet 0 index - column A in excel sheet

# Read data from CSV and insert into SQLite table for the desired columns
with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        selected_data = [row[i] for i in desired_columns_indices]
        cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# Commit changes and close connection
con.commit()
con.close()

#to delete the entier contact table
# con = sqlite3.connect('jarvis.db')  # Replace with your DB filename
# cursor = con.cursor()

# # Delete all records
# cursor.execute("DELETE FROM contacts;")

# # Commit and close
# con.commit()
# con.close()

# to insert single contact values into the db
# query = "INSERT INTO contacts VALUES (null,'pawan', '1234567890', 'null')"
# cursor.execute(query)
# con.commit()

# query = 'Selfish'
# query = query.strip().lower()

# # Open connection
# con = sqlite3.connect('jarvis.db')  # Replace with your DB file
# cursor = con.cursor()

# # Execute the query
# cursor.execute(
#     "SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?",
#     ('%' + query + '%', query + '%')
# )
# results = cursor.fetchall()

# # Print result safely
# if results:
#     print(results[0][0])
# else:
#     print("No contact found.")

# # Close connection
# con.close()