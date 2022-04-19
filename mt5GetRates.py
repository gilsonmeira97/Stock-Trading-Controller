from datetime import datetime, timedelta
from mt5Connection import mt5
from inputSymbols import getSymbols
from dataInsert import insertData

symbols_shares = getSymbols()
yesterday_date = datetime.today() - timedelta(days=1)
date_start = datetime(yesterday_date.year, yesterday_date.month, yesterday_date.day, 23,59)
file = open("geraramErro.txt", "w")

for symbol in symbols_shares:
    rates = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M5, date_start, 500000)
    if rates is None: 
        file.write(f'{symbol}\n')
        continue
    for rate in rates:
        insertData(rate, symbol)
file.close()
print("Ready!")
