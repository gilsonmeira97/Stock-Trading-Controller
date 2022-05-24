from datetime import *
from pymongo import MongoClient, DESCENDING

def getConnection(fsync = False):
   client =  MongoClient(port = 27017, serverSelectionTimeoutMS = 10000, fsync = fsync, maxIdleTimeMS = 300000)
   db = client.stocks
   return client, db

def insertDatas(db, rates, symbol):
   db[symbol].insert_many(rates)

def getLastDay(db, symbol):
   last_day_BD = db[symbol].find_one({},{'date': 1, 'close': 1, '_id': 0}, sort=[('date', DESCENDING)])
   return last_day_BD

def dropCol(db, symbol):
   response = db.drop_collection(symbol)
   return response

def getUTC(date):
    return date.replace(tzinfo=timezone.utc)