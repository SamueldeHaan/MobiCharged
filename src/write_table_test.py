#Write to table

import mysql.connector
import read_table_test

import re


mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "mobicharged",
    database = "mobicharged",
    )
    #print(mydb)
my_cursor = mydb.cursor()

#this is super jank i will fix it in the future! -EN
def check_user_input(user_input):
    #print(user_input)
    if (len(user_input)<4):
        return "ERROR: Input correct number of parameters"
    #check if parameters contain characters
    if(re.search('[a-zA-Z]', user_input[1]) or re.search('[a-zA-Z]', user_input[2]) or (re.search('[a-zA-Z]', user_input[3]))):
        return "ERROR: Please input correct datatypes"
    else:
        return user_input

def write_to_table(user_input):
    #print(user_input)
    #print(len(user_input))
    #print(type(user_input))
    error = 0
    input = 1
    #check for correct input parameters.
    if (len(user_input) <= 5): #hard-coded need to fix
        client_input = False
    else:
        input = user_input.split()
        client_input = True
        input = input[3:] #remove first 3 elements:host name,"-",ip address
        error = check_user_input(input)

    #insert into antenna_parameters table and 1st column of input_output table

    if ((error == input) or (client_input == False)):
        if client_input == True:
            try:
                my_cursor.execute("INSERT INTO Antenna_parameters (Antenna_Type,Length,Width,Thickness) VALUES (%s,%s,%s,%s)",(input[0],input[1],input[2],input[3]))
                mydb.commit()
            except: 
                mydb.rollback()
        else:# client_input == False:
            try:
                #antenna_parameters = read_table_test.read_table('antenna_parameters')
                antenna_parameters = read_table_test.most_recent('antenna_parameters')

                my_cursor.execute("INSERT INTO input_output (input,matlab_output) VALUES (%s, %s)",(antenna_parameters,user_input))
                mydb.commit()
                
                last_row = [antenna_parameters,user_input]
                print(last_row)
                return last_row

            except:
                mydb.rollback()
        #mydb.close()
    else:
        return error


