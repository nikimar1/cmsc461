import logging
import mysql.connector
import pymongo
import urllib
from sqlalchemy import create_engine
import sqlalchemy
import pymysql
import pandas as pd
import numpy as np

###for logging mysql errors creating the database using sqlalchemy
logging.basicConfig(filename='./dbCreation.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)
###

#read csv with 1 year of property tax data to create our initial property database
data = pd.read_csv("./City_property_tax_data.csv")

#add null usernames since the initial data has no usernames associated with it
data['username']=np.nan

#convert dataframe to correct types
data['CityTax'] = data['CityTax'].str.replace(',', '')
data['StateTax'] = data['StateTax'].str.replace(',', '')
data['AmountDue'] = data['AmountDue'].str.replace(',', '')
data = data.astype({'CityTax': 'float','StateTax': 'float','AmountDue': 'float'})
data['AsOfDate'] = data['AsOfDate'].astype('datetime64[ns]') 
data['username'] = data['username'].astype('str') 

#convert res code to boolean since it is binary
#from now on, if it is a primary residence, it will be represented as 1 in mysql and my dataframe
boolConvertDict = {'PRINCIPAL RESIDENCE': True, 'NOT A PRINCIPAL RESIDENCE': False}
data['ResCode'] = data['ResCode'].map(boolConvertDict).astype('bool')

#put your own root password here
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password"
)

mycursor = mydb.cursor()

#create database if it does not exist. if for some reason you have a schema named nikitam, you will have to drop it to run my code
mycursor.execute("CREATE DATABASE IF NOT EXISTS nikitam;")

#allows for loading large database             
mycursor.execute("set global max_allowed_packet=67108864;")

mydb.commit()

mycursor.close()

mydb.close()

#put your own root password here
#password = urllib.parse.quote_plus("password")
         
sqlEngine       = create_engine('mysql+pymysql://root:password@127.0.0.1/NikitaM', pool_recycle=3600)

dbConnection    = sqlEngine.connect()

#Setting all fields to be 1 longer than the longest instance of each field in the original csv file. 
#Meanwhile username will be varchar limited to length of 20.
#found the longest field instances using the following template for mysql queries:
#
#To find the longest block:
#SELECT block FROM housingdata
#ORDER BY LENGTH(block) DESC LIMIT 1
#
#Note that though the longest property address was 33 chars, I decided to give some extra leeway for that variable and set it to varchar(50)
try:
    frame = data.to_sql("housingdata", dbConnection, if_exists='fail',
        dtype=
        {
            'Block': sqlalchemy.types.VARCHAR(length=6),
            'Lot':  sqlalchemy.types.VARCHAR(length=5),
            'Ward': sqlalchemy.types.Integer(),
            'Sect': sqlalchemy.types.Integer(),
            'PropertyAddress': sqlalchemy.types.VARCHAR(length=50),
            'LotSize': sqlalchemy.types.VARCHAR(length=18),
            'CityTax': sqlalchemy.types.Float(precision=3, asdecimal=True),
            'StateTax': sqlalchemy.types.Float(precision=3, asdecimal=True),
            'ResCode': sqlalchemy.types.Boolean,
            'AmountDue': sqlalchemy.types.Float(precision=3, asdecimal=True),
            'AsOfDate': sqlalchemy.DateTime(),
            'username': sqlalchemy.types.VARCHAR(length=20)
        } 
     
    )
     
#Will output errors to log file so you can try to fix them. the code worked for me but for you connection
#might time out if wait time is not the default. (default is 8 hours). Might have other issues with your mysql 
#settings or os that you might need to fix before my code works. the "dbCreation.log" file should help
except ValueError as vx:
    logger.error(vx)
    #print(vx)

except Exception as ex:   
    logger.error(ex)
    #print(ex)
    
else:

    print("\nTable 'housing data' created successfully.\n");   

finally:

    dbConnection.close()

#create admin mongodb database account with password "password"
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["testdb"]
mycol = mydb["users"]

tempdict = { "_id":"admin" ,"login": "admin", "password": "password"}

x = mycol.insert_one(tempdict)

print("mongodb admin account created successfully. its username is 'admin' and its password is 'password'\n")


#put your own root password here
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password"
)

mycursor = mydb.cursor()

#Add primary key to database. determined the values to be used for pkey by looking at what would make original database unique,
#Just in case, made primary key take 4 of these values though propertyaddress and lot with either block or sect were sufficient.
#What if a new user adds something that has the same block lot and property address but a different sect. I decided only this way was
#safe for identifying a property uniquely although in observed cases it is overkill by one extra variable. Note that I am not using the 
#date in the asofdate as a primary key because one can have multiple payments due on the same date for similar but not the same properties. 
mycursor.execute("Use nikitam; ALTER TABLE housingdata ADD CONSTRAINT addressBlockLotSect PRIMARY KEY (PropertyAddress,Lot,Block,Sect);")

mycursor.close()

mydb.close()

print("set primary key for housing data")
