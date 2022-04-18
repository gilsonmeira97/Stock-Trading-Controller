from pymongo import MongoClient
from dbConnection import db
from Share import *

   # List of data that will be persisted in the database
   
#      last_dates[]
#      for item in db[symbol].find({}, {'date': 1, '_id': 0}):
#         last_dates.append(item['date'])
#      for obj in stock:
#         if obj.date not in last_dates:
#            db[ticket].insert_one(vars(obj))
def insertData(rate, symbol):
   newShare = Share(
      rate['time'], rate["open"], rate["high"], 
      rate["low"], rate["close"], rate["tick_volume"], 
      rate["real_volume"]
      )
   db[symbol].insert_one(vars(newShare))
