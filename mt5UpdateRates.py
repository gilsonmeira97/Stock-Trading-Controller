from datetime import datetime, timedelta
import sys
from time import time
from mt5Connection import mt5
from inputSymbols import getSymbols
from dataInsert import getLastDay, insertDatas
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

def updateDB(symbol_db_name, last_day_DB, symbol_mt5_name):
    count = 0
    group_rates = []
    
    if(last_day_DB == None):
        rates = mt5.copy_rates_from(symbol_mt5_name, mt5.TIMEFRAME_M5, reference_date, 500000)
        if rates is None: 
            file.write(f'MT5: Falha ao obter dados de {symbol_mt5_name}\n')
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
                insertDatas(group_rates, symbol_db_name)
                group_rates = []
                count = 0

        if len(group_rates) != 0:
            insertDatas(group_rates, symbol_db_name)
        
        return

    date_DB = last_day_DB['time']
    date_start = datetime(date_DB.year, date_DB.month, date_DB.day) + timedelta(days=1)

    if (date_MT5 <= date_DB): return

    rates = mt5.copy_rates_range(symbol_mt5_name, mt5.TIMEFRAME_M5, date_start, reference_date)

    if rates is None: 
        file.write(f'MT5: Falha ao obter dados de {symbol_mt5_name}\n')
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
            insertDatas(group_rates, symbol_db_name)
            group_rates = []
            count = 0

    if len(group_rates) != 0:
        insertDatas(group_rates, symbol_db_name)

for symbol_db_name, symbol_mt5_name  in symbols.items():
    updateDB( symbol_db_name, getLastDay(symbol_db_name), symbol_mt5_name)

file.close()
print("Updated!")
