from datetime import datetime, timedelta
from time import time
from mt5Connection import mt5
from inputSymbols import getSymbols
from dataInsert import insertDatas
from Share import Share
from pymongo import MongoClient, DESCENDING

reference = "PETR3"
symbols_shares = getSymbols()
yesterday_date = datetime.today() - timedelta(days=1)
reference_date = datetime(yesterday_date.year, yesterday_date.month, yesterday_date.day, 23,59)  # Data mais recente
client = MongoClient(port = 27017, serverSelectionTimeoutMS = 10000)
db = client.stocks
last_day_BD = db[reference].find_one({},{'time': 1, '_id': 0}, sort=[('time', DESCENDING)])
last_day_MT5 = mt5.copy_rates_from(reference, mt5.TIMEFRAME_M5, reference_date, 1)
file = open("logErrosUpdate.txt", "w")

def updateDB():
    if (last_day_BD is []) or (last_day_MT5 is None): return
    
    date_BD = last_day_BD['time']
    date_MT5 = datetime.utcfromtimestamp(last_day_MT5[0]['time'])

    if (date_MT5 <= date_BD): return
    date_start = datetime(date_BD.year, date_BD.month, date_BD.day) + timedelta(days=1)
    temporary_symbols = {}
    erros = 0

    for symbol in symbols_shares:
        rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M5, date_start, reference_date)

        if rates is None: 
            erros += 1
            file.write(f'{symbol}\n')
            continue
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
        temporary_symbols[symbol] = group_rates

    if erros > 0: 
        print("Erros: {}".format(erros))
        return
    for group_rates in temporary_symbols.values():
        insertDatas(group_rates, symbol)
    

updateDB()
file.close()
print("Updated!")
