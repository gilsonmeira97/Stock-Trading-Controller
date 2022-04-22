from pymongo import MongoClient, DESCENDING

def insertDatas(rates, symbol):
   with MongoClient(port = 27017, serverSelectionTimeoutMS = 10000) as client:
      db = client.stocks
      db[symbol].insert_many(rates)

def getLastDay(symbol):
   with MongoClient(port = 27017, serverSelectionTimeoutMS = 10000) as client:
      db = client.stocks
      last_day_BD = db[symbol].find_one({},{'time': 1, '_id': 0}, sort=[('time', DESCENDING)])
      return last_day_BD