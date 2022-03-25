from pymongo import MongoClient
from inputFile import *
from dbConnection import db

for ticket, stock in stocks.items():
   # List of data that will be persisted in the database
   selected = ["PETR3", "BBDC3", "PETR4", "ITSA4", "ITSA3", "CMIG3", "ITUB3"] 

   if ticket in selected: 
      last_dates = []
      for item in db[ticket].find({}, {'date': 1, '_id': 0}):
         last_dates.append(item['date'])
      for obj in stock:
         if obj.date not in last_dates:
            db[ticket].insert_one(vars(obj))

print("All Done!")