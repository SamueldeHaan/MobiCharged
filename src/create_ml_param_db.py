import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "mobicharged",
    database = "ML_parameters",
)
print(mydb)
#my_cursor = mydb.cursor()
#my_cursor.execute("CREATE DATABASE ML_parameters")

my_cursor = mydb.cursor()
print(mydb)

#my_cursor.execute("CREATE TABLE users (name VARCHAR(255), email VARCHAR(255), age INTEGER(10), user_id INTEGER AUTO_INCREMENT PRIMARY KEY)")

my_cursor.execute("SHOW DATABASES")

for table in my_cursor:
    print(table[0])
