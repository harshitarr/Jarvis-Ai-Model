import sqlite3

con = sqlite3.connect("jarvis.db")

cursor = con.cursor()

query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100),path VARCHAR(1000))"
cursor.execute(query)


#query = "INSERT INTO sys_command VALUES (null,'word','C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.exe')"
#cursor.execute(query)
#con.commit()

#query = "DELETE FROM sys_command WHERE name = 'word'"
#cursor.execute(query)
#con.commit()

query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100),path VARCHAR(1000))"
cursor.execute(query)

#query = "INSERT INTO web_command VALUES (null,'youtube','https://youtube.com/')"
#cursor.execute(query)
#con.commit()

query = "DELETE FROM web_command WHERE name = 'linked in'"
cursor.execute(query)
con.commit()