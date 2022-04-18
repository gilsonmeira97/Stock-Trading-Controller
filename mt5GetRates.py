from datetime import datetime
from mt5Connection import mt5
from inputSymbols import symbols_shares
from dataInsert import insertData

date_start = datetime.today()
for symbol in symbols_shares:
    if symbol == "PETR3": 
        rates = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M5, date_start, 500000)
        for rate in rates:
            insertData(rate, symbol)

print("Ready!")
