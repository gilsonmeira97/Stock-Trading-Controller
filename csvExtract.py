import sys
from dbOperations import getConnection
from getRatesDatabase import FirstDate, LastDate, getDayRate
import csv

client, db = getConnection()
symbol = 'PETR3'
nameFile = f"Extracted (Daily) - {symbol}"
datas = getDayRate(db, symbol, FirstDate(2021,4,18), LastDate(2022,4,25), 0, -1)

if len(datas) <= 0:
    sys.exit('Nenhum dado encontrado no intervalo selecionado.')

print("Extracting...")

with open(f'extracteds/{nameFile}.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    
    writer.writerow(["Date", "OPEN", "HIGH", "LOW", "CLOSE", "VOL. R$"])
    for data in datas[0]['ticks']:
        writer.writerow([data['_id'], data['open'], data['high'], data['low'], data['close'], data['day_volume']])

client.close()
print("Extracted!")