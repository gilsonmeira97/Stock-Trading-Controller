from datetime import datetime, timedelta
import sys
from time import time
from mt5Connection import mt5
from inputSymbols import getSymbols
from dataInsert import insertDatas
from Share import Share
from pymongo import MongoClient, DESCENDING

reference = "PETR3"
symbols = getSymbols()
yesterday_date = datetime.today() - timedelta(days=1)
reference_date = datetime(yesterday_date.year, yesterday_date.month, yesterday_date.day, 23,59)  # Data mais recente
client = MongoClient(port = 27017, serverSelectionTimeoutMS = 10000)
db = client.stocks
last_day_MT5 = mt5.copy_rates_from(reference, mt5.TIMEFRAME_M5, reference_date, 1)
file = open("log_ErrosUpdate.txt", "w")

if (last_day_MT5 is None):
    file.close()
    sys.exit("Falha ao receber ultima data MT5.")

date_MT5 = datetime.utcfromtimestamp(last_day_MT5[0]['time'])

def updateDB(symbol, last_day_BD):
    if(last_day_BD == None):
        rates = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M5, date_start, 500000)
        if rates is None: 
            file.write(f'MT5: Falha ao obter dados de {symbol}\n')
            return
        count = 0
        group_rates = []

        for rate in rates:
            group_rates.append(
                vars(
                    Share(
                        rate['time'], rate["open"], rate["high"], 
                        rate["low"], rate["close"], rate["tick_volume"], 
                        rate["real_volume"]
                    )
                )
            )
            count += 1

            if count == 10000:
                insertDatas(group_rates, symbol)
                group_rates = []
                count = 0

        if len(group_rates) != 0:
            insertDatas(group_rates, symbol)
        
        return

    date_BD = last_day_BD['time']

    if (date_MT5 <= date_BD): return

    count = 0
    group_rates = []
    date_start = datetime(date_BD.year, date_BD.month, date_BD.day) + timedelta(days=1)
    rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M5, date_start, reference_date)

    if rates is None: 
        file.write(f'MT5: Falha ao obter dados de {symbol}\n')
        return
        
    for rate in rates:
        group_rates.append(
            vars(
                Share(
                    rate['time'], rate["open"], rate["high"], 
                    rate["low"], rate["close"], rate["tick_volume"], 
                    rate["real_volume"]
                )
            )
        )
        count += 1

        if count == 10000:
            insertDatas(group_rates, symbol)
            group_rates = []
            count = 0

    if len(group_rates) != 0:
        insertDatas(group_rates, symbol)

for i, symbol in enumerate(symbols):
    last_day_BD = db[symbol].find_one({},{'time': 1, '_id': 0}, sort=[('time', DESCENDING)])
    updateDB(symbol, last_day_BD)
    print("Concluído: {:.2f}".format((i + 1) / len(symbols) * 100))


file.close()
print("Updated!")
