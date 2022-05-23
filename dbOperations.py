from datetime import *
from pymongo import MongoClient, DESCENDING

def getConnection(fsync = False):
   client =  MongoClient(port = 27017, serverSelectionTimeoutMS = 10000, fsync = fsync, maxIdleTimeMS = 300000)
   return client

def insertDatas(rates, symbol):
   client = getConnection()
   with client:
      db = client.stocks
      db[symbol].insert_many(rates)

def getLastDay(symbol):
   client = getConnection()
   with client:
      db = client.stocks
      last_day_BD = db[symbol].find_one({},{'date': 1, 'close': 1, '_id': 0}, sort=[('date', DESCENDING)])
      return last_day_BD

def dropCol(symbol):
   client = getConnection()
   with client:
      db = client.stocks
      response = db.drop_collection(symbol)
      return response

def getUTC(date):
    return date.replace(tzinfo=timezone.utc)