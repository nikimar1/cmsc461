#import modules
 
from tkinter import *
from pandastable import Table, TableModel
import pymongo
import mysql.connector
import pandas as pd
import numpy as np
#import tkinter as tktk

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["testdb"]
mycol = mydb["users"]

#global dataframe for output
tempFrame = pd.DataFrame()
 
# Designing window for registration
 
def register():

    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("300x250")
 
    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()
 
    Label(register_screen, text="Please enter details below", bg="blue").pack()
    Label(register_screen, text="").pack()
    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=10, height=1, bg="blue", command = register_user).pack()
 
 
# Designing window for login 
 
def login():

    #variable for successful login
    global globalUsername 

    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="").pack()
 
    global username_verify
    global password_verify
 
    username_verify = StringVar()
    password_verify = StringVar()
 
    global username_login_entry
    global password_login_entry
 
    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command = login_verify).pack()
 
# Implementing event on register button
 
def register_user():
 
    username_info = username.get()
    password_info = password.get()
 
    try:
        tempdict = { "_id":username_info ,"login": username_info, "password": password_info}

        x = mycol.insert_one(tempdict)
        
        register_sucess()
        #Label(login_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()
    except:
        #Label(login_screen, text="This account already exists", fg="red", font=("calibri", 11)).pack()
        register_fail()
        
    username_entry.delete(0, END)
    password_entry.delete(0, END)
    register_screen.destroy()
 

    
    #register_screen.destroy()
 
# Implementing event on login button 
 
def login_verify():
    #variable for successful login
    global globalUsername 
    username1 = username_verify.get()
    password1 = password_verify.get()
 
    query = mycol.find_one({"login": username1})
    if not query:
        user_not_found()
    else:
        if query.get('password') == password1:
            globalUsername= username1
            
            login_sucess()
        else:
            password_not_recognised()
            
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)
    login_screen.destroy()
 
# Designing popup for registration success
 
def register_sucess():
    global register_success_screen
    register_success_screen = Toplevel(main_screen)
    register_success_screen.title("Success")
    register_success_screen.geometry("150x100")
    Label(register_success_screen, text="Registration Success").pack()
    Button(register_success_screen, text="OK", command=delete_register_success).pack()
 
# Designing popup for login success

def login_sucess():
    global login_success_screen
    login_success_screen = Toplevel(main_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("150x100")
    Label(login_success_screen, text="Login Success").pack()
    Button(login_success_screen, text="OK", command=delete_login_success).pack()
 
# Designing popup for invalid registration

def register_fail():
    global register_fail_screen
    register_fail_screen = Toplevel(main_screen)
    register_fail_screen.title("Failure")
    register_fail_screen.geometry("150x100")
    Label(register_fail_screen, text="That account already exists").pack()
    Button(register_fail_screen, text="OK", command=delete_register_fail).pack()
 
# Designing popup for incorrect password

def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(main_screen)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()
 
# Designing popup for user not found
 
def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(main_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()
 
# Deleting popups
 
def delete_login_success():
    login_success_screen.destroy()
    global logged_in_screen
    logged_in_screen = Toplevel(main_screen)
    logged_in_screen.title("Logged in as: " +globalUsername)
    logged_in_screen.geometry("400x200")
    if globalUsername == "admin":
        Button(logged_in_screen, text="Find entry", command=find_entryAdmin).pack()
        Button(logged_in_screen, text="Add entry", command=add_entryAdmin).pack()
        #decided not to implement. beyond scope of course anyway due to very complicated gui
        #Button(logged_in_screen, text="Modify entry", command=modify_entryAdmin).pack()   
        Button(logged_in_screen, text="Find average property tax", command=averageTaxAdmin).pack()
        
    else:
        Button(logged_in_screen, text="Find entry", command=find_entryNonAdmin).pack()
        Button(logged_in_screen, text="Add entry", command=add_entryNonAdmin).pack()
        Button(logged_in_screen, text="Find average property tax", command=averageTaxNonAdmin).pack()
 
def delete_register_success():
    register_success_screen.destroy()
    #register_screen.destroy()

def delete_register_fail():
    register_fail_screen.destroy()
    #register_screen.destroy()
 
def delete_password_not_recognised():
    password_not_recog_screen.destroy()
 
 
def delete_user_not_found_screen():
    user_not_found_screen.destroy()

#commands for sql queries from buttons    
def find_entryNonAdmin():
    #print('find_entryNonAdmin')
    #logged_in_screen.destroy()
    
    #create screen for entering search terms
    global search_screen
    search_screen = Toplevel(main_screen)
    search_screen.title("Search as: "+ globalUsername)
    search_screen.geometry("1200x600")
 
    global block
    global block_entry
    block = StringVar()
    
    global lot
    global lot_entry
    lot = StringVar()
    
    global ward
    global ward_entry
    ward = StringVar()
    
    global sect
    global sect_entry
    sect = StringVar()
 
    global propertyAddress
    global propertyAddress_entry
    propertyAddress = StringVar()
    
    global lotSize
    global lotSize_entry
    lotSize = StringVar()
    
    global cityTax
    global cityTax_entry
    cityTax = StringVar()
    
    global stateTax
    global stateTax_entry
    stateTax = StringVar()
 
    global resCode
    global resCode_entry
    resCode = StringVar()
 
    global amountDue
    global amountDue_entry
    amountDue = StringVar()
 
    global asOfDate
    global asOfDate_entry
    asOfDate = StringVar()
 
    Label(search_screen, text="Please enter parameters for entries you wish to find below.\n" + \
            "Failure to comply with correct entry formats will result in your search query failing or getting no results.\n" +\
            "Blank entries will be ignored as search parameters. "+ \
            "However, single or multiple space entries will be considered as spaces and not ignored.", bg="blue").pack()
 
    #Label(search_screen, text="Please enter parameters for entries you wish to find below."+\
    #    "Note that the Block, Lot, Sect, and Address make up the primary key and must be unique when combined.", bg="blue").pack()
    
    Label(search_screen, text="").pack()
    block_lable = Label(search_screen, text="Block * ")
    block_lable.pack()
    block_entry = Entry(search_screen, textvariable=block)
    block_entry.pack()
    
    lot_lable = Label(search_screen, text="Lot * ")
    lot_lable.pack()
    lot_entry = Entry(search_screen, textvariable=lot)
    lot_entry.pack()
    
    ward_lable = Label(search_screen, text="Ward * ")
    ward_lable.pack()
    ward_entry = Entry(search_screen, textvariable=ward)
    ward_entry.pack()
    
    sect_lable = Label(search_screen, text="Sect * ")
    sect_lable.pack()
    sect_entry = Entry(search_screen, textvariable=sect)
    sect_entry.pack()
    
    propertyAddress_lable = Label(search_screen, text=" Property Address * ")
    propertyAddress_lable.pack()
    propertyAddress_entry = Entry(search_screen, textvariable= propertyAddress)
    propertyAddress_entry.pack()
    
    lotSize_lable = Label(search_screen, text=" Lot Size * ")
    lotSize_lable.pack()
    lotSize_entry = Entry(search_screen, textvariable= lotSize)
    lotSize_entry.pack()
    
    cityTax_lable = Label(search_screen, text="City Tax * ")
    cityTax_lable.pack()
    cityTax_entry = Entry(search_screen, textvariable= cityTax)
    cityTax_entry.pack()
    
    stateTax_lable = Label(search_screen, text="State Tax * ")
    stateTax_lable.pack()
    stateTax_entry = Entry(search_screen, textvariable= stateTax)
    stateTax_entry.pack()
    
    resCode_lable = Label(search_screen, text="Res Code (should be 1 for primary 0 for not) * ")
    resCode_lable.pack()
    resCode_entry = Entry(search_screen, textvariable= resCode)
    resCode_entry.pack()
    
    amountDue_lable = Label(search_screen, text="Amount Due * ")
    amountDue_lable.pack()
    amountDue_entry = Entry(search_screen, textvariable= amountDue)
    amountDue_entry.pack()
    
    asOfDate_lable = Label(search_screen, text="As of date (should be in yyyy-mm-dd hh:mm:ss format) * ")
    asOfDate_lable.pack()
    asOfDate_entry = Entry(search_screen, textvariable= asOfDate)
    asOfDate_entry.pack()
   
    Button(search_screen, text="Search", width=10, height=1, bg="blue", command = searchResultNonAdmin).pack()
    
def find_entryAdmin():
    #print('find_entryAdmin')
    #logged_in_screen.destroy()
    
      #create screen for entering search terms
    global search_screen
    search_screen = Toplevel(main_screen)
    search_screen.title("Search as: "+ globalUsername)
    search_screen.geometry("1200x600")
 
    global block
    global block_entry
    block = StringVar()
    
    global lot
    global lot_entry
    lot = StringVar()
    
    global ward
    global ward_entry
    ward = StringVar()
    
    global sect
    global sect_entry
    sect = StringVar()
 
    global propertyAddress
    global propertyAddress_entry
    propertyAddress = StringVar()
    
    global lotSize
    global lotSize_entry
    lotSize = StringVar()
    
    global cityTax
    global cityTax_entry
    cityTax = StringVar()
    
    global stateTax
    global stateTax_entry
    stateTax = StringVar()
 
    global resCode
    global resCode_entry
    resCode = StringVar()
 
    global amountDue
    global amountDue_entry
    amountDue = StringVar()
 
    global asOfDate
    global asOfDate_entry
    asOfDate = StringVar()
    
    global username
    global username_entry
    username = StringVar()
 
    Label(search_screen, text="Please enter parameters for entries you wish to find below.\n" + \
            "Failure to comply with correct entry formats will result in your search query failing or getting no results.\n" +\
            "Blank entries will be ignored as search parameters. "+ \
            "However, single or multiple space entries will be considered as spaces and not ignored.", bg="blue").pack()
 
    #Label(search_screen, text="Please enter parameters for entries you wish to find below."+\
    #    "Note that the Block, Lot, Sect, and Address make up the primary key and must be unique when combined.", bg="blue").pack()
    
    Label(search_screen, text="").pack()
    block_lable = Label(search_screen, text="Block * ")
    block_lable.pack()
    block_entry = Entry(search_screen, textvariable=block)
    block_entry.pack()
    
    lot_lable = Label(search_screen, text="Lot * ")
    lot_lable.pack()
    lot_entry = Entry(search_screen, textvariable=lot)
    lot_entry.pack()
    
    ward_lable = Label(search_screen, text="Ward * ")
    ward_lable.pack()
    ward_entry = Entry(search_screen, textvariable=ward)
    ward_entry.pack()
    
    sect_lable = Label(search_screen, text="Sect * ")
    sect_lable.pack()
    sect_entry = Entry(search_screen, textvariable=sect)
    sect_entry.pack()
    
    propertyAddress_lable = Label(search_screen, text=" Property Address * ")
    propertyAddress_lable.pack()
    propertyAddress_entry = Entry(search_screen, textvariable= propertyAddress)
    propertyAddress_entry.pack()
    
    lotSize_lable = Label(search_screen, text=" Lot Size * ")
    lotSize_lable.pack()
    lotSize_entry = Entry(search_screen, textvariable= lotSize)
    lotSize_entry.pack()
    
    cityTax_lable = Label(search_screen, text="City Tax * ")
    cityTax_lable.pack()
    cityTax_entry = Entry(search_screen, textvariable= cityTax)
    cityTax_entry.pack()
    
    stateTax_lable = Label(search_screen, text="State Tax * ")
    stateTax_lable.pack()
    stateTax_entry = Entry(search_screen, textvariable= stateTax)
    stateTax_entry.pack()
    
    resCode_lable = Label(search_screen, text="Res Code (should be 1 for primary 0 for not) * ")
    resCode_lable.pack()
    resCode_entry = Entry(search_screen, textvariable= resCode)
    resCode_entry.pack()
    
    amountDue_lable = Label(search_screen, text="Amount Due * ")
    amountDue_lable.pack()
    amountDue_entry = Entry(search_screen, textvariable= amountDue)
    amountDue_entry.pack()
    
    asOfDate_lable = Label(search_screen, text="As of date (should be in yyyy-mm-dd hh:mm:ss format) * ")
    asOfDate_lable.pack()
    asOfDate_entry = Entry(search_screen, textvariable= asOfDate)
    asOfDate_entry.pack()
    
    username_lable = Label(search_screen, text="username * ")
    username_lable.pack()
    username_entry = Entry(search_screen, textvariable= username)
    username_entry.pack()
   
    Button(search_screen, text="Search", width=10, height=1, bg="blue", command = searchResultAdmin).pack()
    
def add_entryAdmin():
    #print('add_entryAdmin')
    #logged_in_screen.destroy()
    
    #create screen for entering search terms
    global search_screen
    search_screen = Toplevel(main_screen)
    search_screen.title("Add entry as: "+ globalUsername)
    search_screen.geometry("1200x600")
 
    global block
    global block_entry
    block = StringVar()
    
    global lot
    global lot_entry
    lot = StringVar()
    
    global ward
    global ward_entry
    ward = StringVar()
    
    global sect
    global sect_entry
    sect = StringVar()
 
    global propertyAddress
    global propertyAddress_entry
    propertyAddress = StringVar()
    
    global lotSize
    global lotSize_entry
    lotSize = StringVar()
    
    global cityTax
    global cityTax_entry
    cityTax = StringVar()
    
    global stateTax
    global stateTax_entry
    stateTax = StringVar()
 
    global resCode
    global resCode_entry
    resCode = StringVar()
 
    global amountDue
    global amountDue_entry
    amountDue = StringVar()
 
    global asOfDate
    global asOfDate_entry
    asOfDate = StringVar()
    
    global username
    global username_entry
    username = StringVar()
 
    #Label(search_screen, text="Please enter parameters for entries you wish to find below.\n" + \
    #        "Failure to comply with correct entry formats will result in your search query failing or getting no results.\n" +\
    #        "Blank entries will be ignored as search parameters. "+ \
    #        "However, single or multiple space entries will be considered as spaces and not ignored.", bg="blue").pack()
 
    Label(search_screen, text="Please enter parameters for entries you wish to add below. "+\
        "Note that the Block, Lot, Sect, and Address make up the primary key and must be unique when combined.", bg="blue").pack()
    
    Label(search_screen, text="").pack()
    block_lable = Label(search_screen, text="Block * ")
    block_lable.pack()
    block_entry = Entry(search_screen, textvariable=block)
    block_entry.pack()
    
    lot_lable = Label(search_screen, text="Lot * ")
    lot_lable.pack()
    lot_entry = Entry(search_screen, textvariable=lot)
    lot_entry.pack()
    
    ward_lable = Label(search_screen, text="Ward * ")
    ward_lable.pack()
    ward_entry = Entry(search_screen, textvariable=ward)
    ward_entry.pack()
    
    sect_lable = Label(search_screen, text="Sect * ")
    sect_lable.pack()
    sect_entry = Entry(search_screen, textvariable=sect)
    sect_entry.pack()
    
    propertyAddress_lable = Label(search_screen, text=" Property Address * ")
    propertyAddress_lable.pack()
    propertyAddress_entry = Entry(search_screen, textvariable= propertyAddress)
    propertyAddress_entry.pack()
    
    lotSize_lable = Label(search_screen, text=" Lot Size * ")
    lotSize_lable.pack()
    lotSize_entry = Entry(search_screen, textvariable= lotSize)
    lotSize_entry.pack()
    
    cityTax_lable = Label(search_screen, text="City Tax * ")
    cityTax_lable.pack()
    cityTax_entry = Entry(search_screen, textvariable= cityTax)
    cityTax_entry.pack()
    
    stateTax_lable = Label(search_screen, text="State Tax * ")
    stateTax_lable.pack()
    stateTax_entry = Entry(search_screen, textvariable= stateTax)
    stateTax_entry.pack()
    
    resCode_lable = Label(search_screen, text="Res Code (should be 1 for primary 0 for not) * ")
    resCode_lable.pack()
    resCode_entry = Entry(search_screen, textvariable= resCode)
    resCode_entry.pack()
    
    amountDue_lable = Label(search_screen, text="Amount Due * ")
    amountDue_lable.pack()
    amountDue_entry = Entry(search_screen, textvariable= amountDue)
    amountDue_entry.pack()
    
    asOfDate_lable = Label(search_screen, text="As of date (should be in yyyy-mm-dd hh:mm:ss format) * ")
    asOfDate_lable.pack()
    asOfDate_entry = Entry(search_screen, textvariable= asOfDate)
    asOfDate_entry.pack()
    
    username_lable = Label(search_screen, text="username * ")
    username_lable.pack()
    username_entry = Entry(search_screen, textvariable= username)
    username_entry.pack()
   
    Button(search_screen, text="Add Entry", width=10, height=1, bg="blue", command = addEntryAdmin).pack()
    
def add_entryNonAdmin():
    #print('add_entryNonAdmin')
    #logged_in_screen.destroy()
    
    #create screen for entering search terms
    global search_screen
    search_screen = Toplevel(main_screen)
    search_screen.title("Add entry as: "+ globalUsername)
    search_screen.geometry("1200x600")
 
    global block
    global block_entry
    block = StringVar()
    
    global lot
    global lot_entry
    lot = StringVar()
    
    global ward
    global ward_entry
    ward = StringVar()
    
    global sect
    global sect_entry
    sect = StringVar()
 
    global propertyAddress
    global propertyAddress_entry
    propertyAddress = StringVar()
    
    global lotSize
    global lotSize_entry
    lotSize = StringVar()
    
    global cityTax
    global cityTax_entry
    cityTax = StringVar()
    
    global stateTax
    global stateTax_entry
    stateTax = StringVar()
 
    global resCode
    global resCode_entry
    resCode = StringVar()
 
    global amountDue
    global amountDue_entry
    amountDue = StringVar()
 
    global asOfDate
    global asOfDate_entry
    asOfDate = StringVar()
    
    #global username
    #global username_entry
    #username = StringVar()
 
    #Label(search_screen, text="Please enter parameters for entries you wish to find below.\n" + \
    #        "Failure to comply with correct entry formats will result in your search query failing or getting no results.\n" +\
    #        "Blank entries will be ignored as search parameters. "+ \
    #        "However, single or multiple space entries will be considered as spaces and not ignored.", bg="blue").pack()
 
    Label(search_screen, text="Please enter parameters for entries you wish to add below. "+\
        "Note that the Block, Lot, Sect, and Address make up the primary key and must be unique when combined.", bg="blue").pack()
    
    Label(search_screen, text="").pack()
    block_lable = Label(search_screen, text="Block * ")
    block_lable.pack()
    block_entry = Entry(search_screen, textvariable=block)
    block_entry.pack()
    
    lot_lable = Label(search_screen, text="Lot * ")
    lot_lable.pack()
    lot_entry = Entry(search_screen, textvariable=lot)
    lot_entry.pack()
    
    ward_lable = Label(search_screen, text="Ward * ")
    ward_lable.pack()
    ward_entry = Entry(search_screen, textvariable=ward)
    ward_entry.pack()
    
    sect_lable = Label(search_screen, text="Sect * ")
    sect_lable.pack()
    sect_entry = Entry(search_screen, textvariable=sect)
    sect_entry.pack()
    
    propertyAddress_lable = Label(search_screen, text=" Property Address * ")
    propertyAddress_lable.pack()
    propertyAddress_entry = Entry(search_screen, textvariable= propertyAddress)
    propertyAddress_entry.pack()
    
    lotSize_lable = Label(search_screen, text=" Lot Size * ")
    lotSize_lable.pack()
    lotSize_entry = Entry(search_screen, textvariable= lotSize)
    lotSize_entry.pack()
    
    cityTax_lable = Label(search_screen, text="City Tax * ")
    cityTax_lable.pack()
    cityTax_entry = Entry(search_screen, textvariable= cityTax)
    cityTax_entry.pack()
    
    stateTax_lable = Label(search_screen, text="State Tax * ")
    stateTax_lable.pack()
    stateTax_entry = Entry(search_screen, textvariable= stateTax)
    stateTax_entry.pack()
    
    resCode_lable = Label(search_screen, text="Res Code (should be 1 for primary 0 for not) * ")
    resCode_lable.pack()
    resCode_entry = Entry(search_screen, textvariable= resCode)
    resCode_entry.pack()
    
    amountDue_lable = Label(search_screen, text="Amount Due * ")
    amountDue_lable.pack()
    amountDue_entry = Entry(search_screen, textvariable= amountDue)
    amountDue_entry.pack()
    
    asOfDate_lable = Label(search_screen, text="As of date (should be in yyyy-mm-dd hh:mm:ss format) * ")
    asOfDate_lable.pack()
    asOfDate_entry = Entry(search_screen, textvariable= asOfDate)
    asOfDate_entry.pack()
    
    #username_lable = Label(search_screen, text="username * ")
    #username_lable.pack()
    #username_entry = Entry(search_screen, textvariable= username)
    #username_entry.pack()
   
    Button(search_screen, text="Add Entry", width=10, height=1, bg="blue", command = addEntryNonAdmin).pack()
 
##decided not to implement. beyond scope of project requirements 
#def modify_entryAdmin():
    #print('modify_entryAdmin')
#    logged_in_screen.destroy()
    
def searchResultAdmin():

    #dictionary stores user input
    searchDict ={
        'Block': block.get(),
        'Lot': lot.get(),
        'Ward':ward.get(),
        'Sect':sect.get(),
        'PropertyAddress':propertyAddress.get(),
        'LotSize':lotSize.get(),
        'CityTax':cityTax.get(),
        'StateTax':stateTax.get(),
        'ResCode':resCode.get(),
        'AmountDue':amountDue.get(),
        'AsOfDate':asOfDate.get(),
        'username':username.get()
    }
    
    #string for querying mysql
    sqlString = "Select * From housingdata"
    
    #now parse which entries are non blank and add them to query
    for key, value in searchDict.items():
        #if value is not null/ totally blank
        if value:
            if sqlString[-25:] == "Select * From housingdata":
                sqlString+= " Where " 
            else:
                sqlString+= " And "
            sqlString+=key + " = '" + value+"'" 
    sqlString+=";"
    
    #print(sqlString)
    
    #put your own root password here
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password"
    )
    
    mycursor = mydb.cursor()
    

    mycursor.execute("Use nikitam;")
    mycursor.close()
    
    search_screen.destroy()
    
    try:
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute(sqlString)
    except Exception as e:
        resultsScreen = Toplevel(main_screen)
        Label(resultsScreen, text="Error with your selection. Consult commandline interface to see error stacktrace" , font=("Calibri", 15)).pack()
        resultsScreen.title("Error")
        resultsScreen.geometry("700x350")
        print(e)
    
    else:
    
        global tempFrame
        
        if mycursor.rowcount > 0:
            #dataTemp = mycursor.fetchall()
            tempFrame = pd.DataFrame(mycursor.fetchall())
            tempFrame.columns = ['index','Block','Lot','Ward','Sect','PropertyAddress','LotSize','CityTax','StateTax','ResCode',\
            'AmountDue','AsOfDate','username']
        
        #print(tempFrame) 
        
        mycursor.close()
        
        mydb.close()
        
        #global resultsScreen
        resultsScreen = Toplevel(main_screen)
        resultsScreen.geometry("1250x650+0+0")
        resultsScreen.title("Results")
        resultsScreen.configure(background="black")

        f = Frame(resultsScreen)
        f.pack(fill=BOTH,expand=1)

        pt = Table(f, dataframe=tempFrame, showtoolbar=True, showstatusbar=True)
        pt.show()
    
def searchResultNonAdmin():

    #dictionary stores user input
    searchDict ={
        'Block': block.get(),
        'Lot': lot.get(),
        'Ward':ward.get(),
        'Sect':sect.get(),
        'PropertyAddress':propertyAddress.get(),
        'LotSize':lotSize.get(),
        'CityTax':cityTax.get(),
        'StateTax':stateTax.get(),
        'ResCode':resCode.get(),
        'AmountDue':amountDue.get(),
        'AsOfDate':asOfDate.get(),
        'username':globalUsername
    }
    
    #string for querying mysql
    sqlString = "Select * From housingdata"
    
    #now parse which entries are non blank and add them to query
    for key, value in searchDict.items():
        #if value is not null/ totally blank
        if value:
            if sqlString[-25:] == "Select * From housingdata":
                sqlString+= " Where " 
            else:
                sqlString+= " And "
            sqlString+=key + " = '" + value+"'" 
    sqlString+=";"
    
    #print(sqlString)
    
    #put your own root password here
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password"
    )
    
    mycursor = mydb.cursor()
    

    mycursor.execute("Use nikitam;")
    mycursor.close()

    search_screen.destroy()
    
    try:
    
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute(sqlString)
    
    except Exception as e:
        resultsScreen = Toplevel(main_screen)
        Label(resultsScreen, text="Error with your selection. Consult commandline interface to see error stacktrace", font=("Calibri", 15)).pack()
        resultsScreen.title("Error")
        resultsScreen.geometry("700x350")
        print(e)
    
    else:
        global tempFrame
        
        if mycursor.rowcount > 0:
            #dataTemp = mycursor.fetchall()
            tempFrame = pd.DataFrame(mycursor.fetchall())
            tempFrame.columns = ['index','Block','Lot','Ward','Sect','PropertyAddress','LotSize','CityTax','StateTax','ResCode',\
            'AmountDue','AsOfDate','username']
        
        #print(tempFrame) 
        
        mycursor.close()
        
        mydb.close()
        
        #global resultsScreen
        resultsScreen = Toplevel(main_screen)
        resultsScreen.geometry("1250x650+0+0")
        resultsScreen.title("Results")
        resultsScreen.configure(background="black")

        f = Frame(resultsScreen)
        f.pack(fill=BOTH,expand=1)

        pt = Table(f, dataframe=tempFrame, showtoolbar=True, showstatusbar=True)
        pt.show()
    
def addEntryAdmin():
    
    #dictionary stores user input
    searchDict ={
        'Block': block.get(),
        'Lot': lot.get(),
        'Ward':ward.get(),
        'Sect':sect.get(),
        'PropertyAddress':propertyAddress.get(),
        'LotSize':lotSize.get(),
        'CityTax':cityTax.get(),
        'StateTax':stateTax.get(),
        'ResCode':resCode.get(),
        'AmountDue':amountDue.get(),
        'AsOfDate':asOfDate.get(),
        'username':username.get()
    }
    
    #string for querying mysql
    sqlString = "insert into housingdata(Block,Lot,Ward,Sect,"\
        "PropertyAddress,LotSize,CityTax,StateTax,ResCode,"\
        "AmountDue,AsOfDate,username)"\
        "VALUES("
    
    #now parse which entries are non blank and add them to query
    for key, value in searchDict.items():
        #if value is not null/ totally blank
        if value:
            valueMod =""
            
            #"switch" statement for adding quotes to varchars
            
            if key == 'Block':
                valueMod = "'"+ value+"'"
        
            elif key == 'Lot': 
                valueMod = "'"+ value+"'"
        
            elif key == 'Ward':
                valueMod = value
            
            elif key == 'Sect':
                valueMod = value     
        
            elif key == 'PropertyAddress':
                valueMod = "'"+ value+"'"
      
            elif key == 'LotSize':
                valueMod = "'"+ value+"'"
                       
            elif key == 'CityTax':
                valueMod = value
                        
            elif key == 'StateTax':
                valueMod=value
                       
            elif key == 'ResCode':
                valueMod = value
                       
            elif key == 'AmountDue':
                valueMod=value
                         
            elif key == 'AsOfDate':
                valueMod = "'"+ value+"'"
                            
            elif key == 'username':
                valueMod = "'"+ value+"'"            
                
            #append modified value which has quotes appended as necessary from above "switch" statement"
            sqlString+=valueMod
        else:
            #if no value entered use null. don't need to append quotes
            sqlString+="NULL"
            
            #add comma until the end
        if not key == 'username':
            sqlString+=","
    
    #add closed parentheses and semi colon
    sqlString+=");"
    
    #print(sqlString)
    
    #put your own root password here
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password"
    )
    
    mycursor = mydb.cursor()
    
    mycursor.execute("Use nikitam;")
    mycursor.close()
    
    search_screen.destroy()
    
    try:
        mycursor = mydb.cursor()
        mycursor.execute(sqlString)
        mydb.commit()
    except Exception as e:
        resultsScreen = Toplevel(main_screen)
        Label(resultsScreen,text="Error with your insertion. Consult commandline interface to see error stacktrace" , font=("Calibri", 15)).pack()
        resultsScreen.title("Error")
        resultsScreen.geometry("700x350")
        print(e)
        
    else:
        resultsScreen = Toplevel(main_screen)
        resultsScreen.title("Success")
        resultsScreen.geometry("700x350")
        Label(resultsScreen, text="Added entry successfuly" , font=("Calibri", 15)).pack()
        
def addEntryNonAdmin():
    
    #dictionary stores user input
    searchDict ={
        'Block': block.get(),
        'Lot': lot.get(),
        'Ward':ward.get(),
        'Sect':sect.get(),
        'PropertyAddress':propertyAddress.get(),
        'LotSize':lotSize.get(),
        'CityTax':cityTax.get(),
        'StateTax':stateTax.get(),
        'ResCode':resCode.get(),
        'AmountDue':amountDue.get(),
        'AsOfDate':asOfDate.get(),
        'username':globalUsername
    }
    
    #string for querying mysql
    sqlString = "insert into housingdata(Block,Lot,Ward,Sect,"\
        "PropertyAddress,LotSize,CityTax,StateTax,ResCode,"\
        "AmountDue,AsOfDate,username)"\
        "VALUES("
    
    #now parse which entries are non blank and add them to query
    for key, value in searchDict.items():
        #if value is not null/ totally blank
        if value:
            valueMod =""
            
            #"switch" statement for adding quotes to varchars
            
            if key == 'Block':
                valueMod = "'"+ value+"'"
        
            elif key == 'Lot': 
                valueMod = "'"+ value+"'"
        
            elif key == 'Ward':
                valueMod = value
            
            elif key == 'Sect':
                valueMod = value     
        
            elif key == 'PropertyAddress':
                valueMod = "'"+ value+"'"
      
            elif key == 'LotSize':
                valueMod = "'"+ value+"'"
                       
            elif key == 'CityTax':
                valueMod = value
                        
            elif key == 'StateTax':
                valueMod=value
                       
            elif key == 'ResCode':
                valueMod = value
                       
            elif key == 'AmountDue':
                valueMod=value
                         
            elif key == 'AsOfDate':
                valueMod = "'"+ value+"'"
                            
            elif key == 'username':
                valueMod = "'"+ value+"'"            
                
            #append modified value which has quotes appended as necessary from above "switch" statement"
            sqlString+=valueMod
        else:
            #if no value entered use null. don't need to append quotes
            sqlString+="NULL"
            
            #add comma until the end
        if not key == 'username':
            sqlString+=","
    
    #add closed parentheses and semi colon
    sqlString+=");"
    
    #print(sqlString)
    
    #put your own root password here
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password"
    )
    
    mycursor = mydb.cursor()
    
    mycursor.execute("Use nikitam;")
    mycursor.close()
    
    search_screen.destroy()
    
    try:
        mycursor = mydb.cursor()
        mycursor.execute(sqlString)
        mydb.commit()
    except Exception as e:
        resultsScreen = Toplevel(main_screen)
        Label(resultsScreen,text="Error with your insertion. Consult commandline interface to see error stacktrace" , font=("Calibri", 15)).pack()
        resultsScreen.title("Error")
        resultsScreen.geometry("700x350")
        print(e)
        
    else:
        resultsScreen = Toplevel(main_screen)
        resultsScreen.title("Success")
        resultsScreen.geometry("700x350")
        Label(resultsScreen, text="Added entry successfuly" , font=("Calibri", 15)).pack()

def averageTaxAdmin():
    
    #create screen for entering search terms
    global search_screen
    search_screen = Toplevel(main_screen)
    search_screen.title("Calculate average tax as: "+ globalUsername)
    search_screen.geometry("600x400")
    
    global username
    global username_entry
    username = StringVar()
 
    #Label(search_screen, text="Please enter parameters for entries you wish to find below.\n" + \
    #        "Failure to comply with correct entry formats will result in your search query failing or getting no results.\n" +\
    #        "Blank entries will be ignored as search parameters. "+ \
    #        "However, single or multiple space entries will be considered as spaces and not ignored.", bg="blue").pack()
 
    Label(search_screen, text="Enter username to find average tax for this user", bg="blue").pack()
    
    Label(search_screen, text="").pack()
    username_lable = Label(search_screen, text="Username * ")
    username_lable.pack()
    username_entry = Entry(search_screen, textvariable=username)
    username_entry.pack()
    
    Button(search_screen, text="Calculate tax", width=10, height=1, bg="blue", command = averageTaxAdminCalc).pack()

def averageTaxAdminCalc():
    usernameTemp = username.get()

    sqlString = "select avg (AmountDue) from housingdata where username = '%s';"%(usernameTemp)
    
    #put your own root password here
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password"
    )
    
    search_screen.destroy()
    
    mycursor = mydb.cursor()
    
    mycursor.execute("use nikitam")

    try:
    
        global tempFrame
        mycursor.execute(sqlString)
        #mydb.commit()

    except Exception as e:
        resultsScreen = Toplevel(main_screen)
        Label(resultsScreen,text="Error with your tax calc. consult stacktrace in command line window" , font=("Calibri", 15)).pack()
        resultsScreen.title("Error")
        resultsScreen.geometry("700x350")
        print(e)
        
    else:
    
        resultsScreen = Toplevel(main_screen)
        Label(resultsScreen,text="Successful tax calc. Your average is:" , font=("Calibri", 15)).pack()
        resultsScreen.title("Successful tax calc for user: " +globalUsername)
        resultsScreen.geometry("700x350")
        

        for row in mycursor:
            Label(resultsScreen,text=row , font=("Calibri", 15)).pack()

def averageTaxNonAdmin():
    
    #create screen for entering search terms
    global search_screen
    search_screen = Toplevel(main_screen)
    search_screen.title("Calculate average tax as: "+ globalUsername)
    search_screen.geometry("600x400")
    
    #global username
    #global username_entry
    #username = StringVar()
 
    #Label(search_screen, text="Please enter parameters for entries you wish to find below.\n" + \
    #        "Failure to comply with correct entry formats will result in your search query failing or getting no results.\n" +\
    #        "Blank entries will be ignored as search parameters. "+ \
    #        "However, single or multiple space entries will be considered as spaces and not ignored.", bg="blue").pack()
 
    Label(search_screen, text="Enter username to find average tax for this user", bg="blue").pack()
    
    #Label(search_screen, text="").pack()
    #username_lable = Label(search_screen, text="Username * ")
    #username_lable.pack()
    #username_entry = Entry(search_screen, textvariable=username)
    #username_entry.pack()
    
    Button(search_screen, text="Calculate tax", width=10, height=1, bg="blue", command = averageTaxNonAdminCalc).pack()

def averageTaxNonAdminCalc():

    sqlString = "select avg (AmountDue) from housingdata where username = '%s';"%(globalUsername)
    
    #put your own root password here
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password"
    )
    
    search_screen.destroy()
    
    mycursor = mydb.cursor()
    
    mycursor.execute("use nikitam")

    try:
    
        global tempFrame
        mycursor.execute(sqlString)
        #mydb.commit()

    except Exception as e:
        resultsScreen = Toplevel(main_screen)
        Label(resultsScreen,text="Error with your tax calc. consult stacktrace in command line window" , font=("Calibri", 15)).pack()
        resultsScreen.title("Error")
        resultsScreen.geometry("700x350")
        print(e)
        
    else:
    
        resultsScreen = Toplevel(main_screen)
        Label(resultsScreen,text="Successful tax calc. Your average is:" , font=("Calibri", 15)).pack()
        resultsScreen.title("Successful tax calc for user: " +globalUsername)
        resultsScreen.geometry("700x350")
        

        for row in mycursor:
            Label(resultsScreen,text=row , font=("Calibri", 15)).pack()

    
# Designing Main(first) window
 
def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Account Login")
    Label(text="Select Your Choice", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", command = login).pack()
    Label(text="").pack()
    Button(text="Register", height="2", width="30", command=register).pack()
 
    main_screen.mainloop()
 

 
main_account_screen()