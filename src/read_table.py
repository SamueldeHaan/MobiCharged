import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "mobicharged",
    database = "mobicharged",
)
#print(mydb)
def read_table():
    user_input = (input("Input which table to read from: \n i.e. ml_hyperparameters,output\n"))
    if ((user_input.lower()!='ml_hyperparameters') and (user_input.lower()!="output")):
        print("ERROR: Input correct specifier for table name;'ml_hyperparameters' or 'output'")
    else:
        my_cursor = mydb.cursor()
        if (user_input.lower()=='ml_hyperparameters'):
            my_cursor.execute("select * from ml_hyperparameters")
        elif (user_input.lower()=='output'):
            my_cursor.execute("select * from output")
        #my_cursor.execute("select * from output")
        myresult = my_cursor.fetchall()
        for x in myresult:
            print(x)
    mydb.close()

read_table()