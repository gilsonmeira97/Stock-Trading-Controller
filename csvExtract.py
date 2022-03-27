from dbConnection import db
import csv
import datetime

ticket = 'PETR3'
qty = 100
datas = db[ticket].find({}, {'date': 1, 'ticket': 1, 'close_price': 1, '_id': 0}).sort('date', -1).limit(qty)

with open('data_extracted.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    
    writer.writerow(["Data", "Papel", "Fechamento"])
    for data in datas:
        writer.writerow([data['date'].date, data['ticket'], data['close_price']])
print("Extracted!")