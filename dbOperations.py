from pymongo import MongoClient, DESCENDING
from datetime import *

def insertDatas(rates, symbol):
   with MongoClient(port = 27017, serverSelectionTimeoutMS = 10000) as client:
      db = client.stocks
      db[symbol].insert_many(rates)

def getLastDay(symbol):
   with MongoClient(port = 27017, serverSelectionTimeoutMS = 10000) as client:
      db = client.stocks
      last_day_BD = db[symbol].find_one({},{'date': 1, 'close': 1, '_id': 0}, sort=[('date', DESCENDING)])
      return last_day_BD

def dropCol(symbol):
   with MongoClient(port = 27017, serverSelectionTimeoutMS = 10000) as client:
      db = client.stocks
      isDropped = db[symbol].drop()
      return isDropped

def getUTC(date):
    return date.replace(tzinfo=timezone.utc)