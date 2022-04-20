from pymongo import MongoClient
import csv

ticket = 'PETR3'
qty = 100
client = MongoClient(port = 27017, serverSelectionTimeoutMS = 10000)
db = client.stocks
datas = db[ticket].find({}, {'date': 1, 'ticket': 1, 'close_price': 1, '_id': 0}).sort('date', -1).limit(qty)

with open('data_extracted.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    
    writer.writerow(["Data", "Papel", "Fechamento"])
    writer.writerow([33, 22, 3])
print("Extracted!")