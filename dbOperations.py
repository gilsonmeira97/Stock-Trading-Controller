from datetime import *
from pymongo import MongoClient, DESCENDING

def getConnection(fsync = False):
    client =  MongoClient(port = 27017, serverSelectionTimeoutMS = 10000, fsync = fsync)
    db = client.stocks
    return client, db

def insertDatas(rates, symbol, db):
   db[symbol].insert_many(rates)

def getLastDay(symbol, db):
   last_day_BD = db[symbol].find_one({},{'date': 1, 'close': 1, '_id': 0}, sort=[('date', DESCENDING)])
   return last_day_BD

def dropCol(symbol, db):
   response = db.drop_collection(symbol)
   return response

def getUTC(date):
    return date.replace(tzinfo=timezone.utc)