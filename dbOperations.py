from datetime import *
from pymongo import MongoClient, DESCENDING
import pymongo

def getConnection(fsync = False):
   client =  MongoClient(port = 27017, serverSelectionTimeoutMS = 10000, fsync = fsync)
   db = client.stocks
   return client, db

def insertDatas(db, rates, symbol):
   db[symbol].insert_many(rates)
   '''
   try:

   except (pymongo.erros.AutoReconnect) as err:
      print(err)
   '''

def getLastDay(db, symbol):
   last_day_BD = db[symbol].find_one({},{'date': 1, 'close': 1, '_id': 0}, sort=[('date', DESCENDING)])
   return last_day_BD

def dropCol(db, symbol):
   response = db.drop_collection(symbol)
   return response

def getUTC(date):
    return date.replace(tzinfo=timezone.utc)