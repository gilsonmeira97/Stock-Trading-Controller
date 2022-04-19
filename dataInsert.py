from pymongo import MongoClient

def insertDatas(rates, symbol):
   with MongoClient(port = 27017, serverSelectionTimeoutMS = 10000) as client:
      db = client.stocks
      db[symbol].insert_many(rates)

   