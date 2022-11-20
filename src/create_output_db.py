import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "mobicharged",
    database = "mobicharged",
)
print(mydb)
my_cursor = mydb.cursor()
#my_cursor.execute("CREATE DATABASE Mobicharged")

my_cursor.execute("CREATE TABLE ML_Hyperparameters (Model_ID INTEGER AUTO_INCREMENT PRIMARY KEY, Model_Architecture VARCHAR(255), learning_rate FLOAT(10), Epochs INTEGER(10), param3 INTEGER(10))")
#my_cursor.execute("CREATE TABLE Output (param1 VARCHAR(255), param2 FLOAT(10), param3 INTEGER(10), param4 INTEGER AUTO_INCREMENT PRIMARY KEY)")

my_cursor.execute("SHOW DATABASES")
for table in my_cursor:
    print(table[0])
