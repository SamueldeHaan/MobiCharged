#Write to table

import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "mobicharged",
    database = "mobicharged",
)
print(mydb)
my_cursor = mydb.cursor()

#TEST VARIABLES AND COMMANDS
MA = "RCNN";
LR = 0.2;
EE = 5;
P3 = "0";
P1 = P2 = "3"

#my_cursor.execute("INSERT INTO ml_hyperparameters (Model_Architecture, Learning_Rate, Epochs, Param3) VALUES (%s,%s,%s,%s)",(MA,LR,EE,P3))
#my_cursor.execute("INSERT INTO output (param1,param2,param3) VALUES (%s,%s,%s)",(P1,P2,P3))
#mydb.commit()

#input = ["ml_hyperparameters",P1,P2,P3,P4] #format = [table name, data]
#We can change to allow 0 = ml_hyperparameters, 1 = output for easier formatting

#input = ["ml_hyperparameters",MA,LR,EE,P3]
#input = ["output",P1,P2,P3]



def write_to_table(user_input):
    print("test")
    input = user_input
    table = input[0]
    if (table == "ml_hyperparameters"):
        try:
            print("test1")
            my_cursor.execute("INSERT INTO ml_hyperparameters (Model_Architecture, Learning_Rate, Epochs, Param3) VALUES (%s,%s,%s,%s)",(input[1],input[2],input[3],input[4]))
            mydb.commit()
        except: 
            mydb.rollback()
    elif (table == "output"):
        try:
            print("test2")

            my_cursor.execute("INSERT INTO output (param1,param2,param3) VALUES (%s,%s,%s)",(input[1],input[2],input[3]))
            mydb.commit()
        except: 
            mydb.rollback()
    else:
        print("Incorrect input format, specify table name in first element of input")
    

#take user input, make sure tha the list is of correct length;

raw_input = (input("Input the data to be entered into database seperated by a space \nExample Format: ml_hyperparameters RCNN 0.2 5 0], output 1 1 3]\n"))
user_input = raw_input.split()
print(user_input, type(user_input))
x=1 

if ((user_input[0].lower()!='ml_hyperparameters') and (user_input[0]!="output")):
    x=0
    print("ERROR: Input correct specifier for table name;'ml_hyperparameters' or 'output'")
if (user_input[0]=="ml_hyperparameters") and (len(user_input)<5):
    x=0
    print("ERROR: Input correct number of parameters")
if (user_input[0]=="output") and (len(user_input)<4):
    x=0
    print("ERROR: Input correct number of parameters")

if (x==1):
    write_to_table(user_input)
mydb.close()

