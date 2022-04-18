from pymongo import MongoClient
from mt5GetRates import *
from dbConnection import db
from Share import *

   # List of data that will be persisted in the database
   

#      for item in db[ticket].find({}, {'date': 1, '_id': 0}):
#         last_dates.append(item['date'])
#      for obj in stock:
#         if obj.date not in last_dates:
#            db[ticket].insert_one(vars(obj))
def registerData(share, symbol):
   newShare = Share(
      share['time'], symbol, share["open"], 
      share["high"], share["low"], share["close"], 
      share["tick_volume"], share["real_volume"]
      )
   
print("All Done!")
