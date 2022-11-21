import mysql.connector

#run once to initially create tables
def create_tables():
    mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "mobicharged",
    database = "mobicharged",
    )
    
    my_cursor = mydb.cursor()
    my_cursor.execute("CREATE TABLE Antenna_parameters (ID INTEGER AUTO_INCREMENT PRIMARY KEY, Antenna_Type VARCHAR(255), Length FLOAT(10), Width Float(10), Thickness INTEGER(10))")
    my_cursor.execute("CREATE TABLE Input_Output (ID INTEGER AUTO_INCREMENT PRIMARY KEY, input VARCHAR(255), matlab_output VARCHAR(255))")

create_tables()