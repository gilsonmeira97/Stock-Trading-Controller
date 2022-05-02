from datetime import datetime, timedelta
import sys
from mt5Connection import mt5
from inputSymbols import getSymbols
from dbOperations import getConnection, getLastDay, insertDatas, dropCol, getUTC
from Share import Share
from logManager import writeLog

reference = "PETR3"
symbols = getSymbols()
reference_date = getUTC(datetime.today())  # Data mais recente
client, db = getConnection()
last_day_MT5 = mt5.copy_rates_from(reference, mt5.TIMEFRAME_M5, reference_date, 1)

if (last_day_MT5 is None):
    sys.exit("MT5 - Falha ao receber ultima data.")

date_MT5 = getUTC(datetime.utcfromtimestamp(last_day_MT5[0]['time']))
file = open("logs/log_ErrosUpdate.txt", "a")

def newStock(symbol_db_name, symbol_mt5_name):
    count = 0
    group_rates = []
    rates = mt5.copy_rates_from(symbol_mt5_name, mt5.TIMEFRAME_M5, reference_date, 500000)
    if rates is None: 
        writeLog(file, f'MT5: Falha ao obter dados de {symbol_mt5_name} - (newStock)')
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
            insertDatas(group_rates, symbol_db_name, db)
            group_rates = []
            count = 0

    if len(group_rates) != 0:
        insertDatas(group_rates, symbol_db_name, db)

def updateStock(symbol_db_name, symbol_mt5_name, date_DB):
    count = 0
    group_rates = []
    date_start = date_DB + timedelta(minutes=1)
    rates = mt5.copy_rates_range(symbol_mt5_name, mt5.TIMEFRAME_M5, date_start, reference_date)

    if rates is None: 
        writeLog(file, f'MT5: Falha ao obter dados de {symbol_mt5_name} - (updateStock)')
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
            insertDatas(group_rates, symbol_db_name, db)
            group_rates = []
            count = 0

    if len(group_rates) != 0:
        insertDatas(group_rates, symbol_db_name, db)


def updateDB(symbol_db_name, last_day_DB, symbol_mt5_name):
    if(last_day_DB == None):
        newStock(symbol_db_name, symbol_mt5_name)
        return

    date_DB = getUTC(last_day_DB['date'])
    
    dividend_test = mt5.copy_rates_range(symbol_mt5_name, mt5.TIMEFRAME_M5, date_DB, date_DB)
    
    if dividend_test is None or len(dividend_test) == 0: 
        writeLog(file, f'MT5: Falha ao obter dados de {symbol_mt5_name} - (dividendTest)')
        return

    if(dividend_test[0]['close'] != last_day_DB['close'] ):
        writeLog(file, f'DB: Ajuste de dividendos em {symbol_mt5_name}')
        drop_res = dropCol(symbol_db_name, db)
        if 'ns' in drop_res: 
            newStock(symbol_db_name, symbol_mt5_name)
        return

    if (date_MT5 <= date_DB): return
    
    updateStock(symbol_db_name, symbol_mt5_name, date_DB)

print('Updating...')
writeLog(file, f'DB: Atualização da base de dados - (Update)')

for symbol_db_name, symbol_mt5_name  in symbols.items():
    updateDB( symbol_db_name, getLastDay(symbol_db_name, db), symbol_mt5_name)

file.close()
client.close()
print("Updated!")
