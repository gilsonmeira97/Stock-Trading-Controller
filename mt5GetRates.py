from datetime import datetime
from mt5Connection import mt5
from inputSymbols import symbols_shares

date_start = datetime.today()
for symbol in symbols_shares:
    if symbol == "PETR3": rates = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M5, date_start, 500000)

#if rates is not None:
    #print(datetime.utcfromtimestamp(rates[4]['time']))