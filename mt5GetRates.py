from datetime import datetime, timedelta

from mt5Connection import mt5
from inputSymbols import getSymbols
from dataInsert import insertDatas
from Share import Share

symbols_shares = getSymbols()
yesterday_date = datetime.today() - timedelta(days=1)
date_start = datetime(yesterday_date.year, yesterday_date.month, yesterday_date.day, 23,59)
file = open("geraramErro.txt", "w")

for symbol in symbols_shares:
    rates = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M5, date_start, 500000)
    if rates is None: 
        file.write(f'{symbol}\n')
        continue
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

file.close()
print("Ready!")
