import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "mobicharged",
    database = "mobicharged",
)
#print(mydb)

#i will make this code neater in the future -EN

def most_recent(user_input):
    if ((user_input.lower()!='antenna_parameters') and (user_input.lower()!="input_output")):
           print("ERROR: Input correct specifier for table name;'antenna_parameters', 'input_output'")
    else:
        my_cursor = mydb.cursor()
        if (user_input.lower()=='input_output'):

            my_cursor.execute("select * from input_output")
        elif (user_input.lower()=='antenna_parameters'):
        #else:
            my_cursor.execute("select * from antenna_parameters")

        myresult = my_cursor.fetchall()

        return str(myresult[-1]) #return last row, this is a serious flaw when concurrency comes into play. We need to switch to pandas for easier

def read_table(user_input):
    #user_input = (input("Input which table to read from: \n i.e. ml_hyperparameters,output\n"))
    # if ((user_input.lower()!='ml_hyperparameters') and (user_input.lower()!="output")):
    #     print("ERROR: Input correct specifier for table name;'ml_hyperparameters' or 'output'")
    if ((user_input.lower()!='antenna_parameters') and (user_input.lower()!="input_output")):
       print("ERROR: Input correct specifier for table name;'antenna_parameters', 'input_output'")
    else:
        my_cursor = mydb.cursor()
        if (user_input.lower()=='input_output'):

            my_cursor.execute("select * from input_output")
        elif (user_input.lower()=='antenna_parameters'):
        #else:
            my_cursor.execute("select * from antenna_parameters")

        myresult = my_cursor.fetchall()

        #print(myresult)
        #return myresult

        y= []
        for x in myresult:
            y.append(str(x))
        return((y))
    #mydb.close()

#read_table()