import sys
from pymongo import MongoClient
from getRatesDatabase import FirstDate, LastDate, getDayRate
import csv

symbol = 'PETR3'
nameFile = f"Extract (Daily) - {symbol}"
client = MongoClient(port = 27017, serverSelectionTimeoutMS = 10000)
db = client.stocks
datas = getDayRate(symbol,FirstDate(2022,4,18), LastDate(2022,4,20))

if len(datas) <= 0:
    sys.exit('Nenhum dado encontrado no intervalo selecionado.')

print("Extracting...")

with open(f'C:\\Users\\Gilson\\Projects\\Extraidos\\{nameFile}.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    
    writer.writerow(["Date", "OPEN", "HIGH", "LOW", "CLOSE", "VOL. R$"])
    for data in datas[0]['ticks']:
        writer.writerow([data['_id'], data['open'], data['high'], data['low'], data['close'], data['day_volume']])

print("Extracted!")