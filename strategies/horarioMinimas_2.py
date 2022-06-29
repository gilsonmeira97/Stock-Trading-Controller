import __sub__
from getRatesDatabase import *
from inputSymbols import getSymbols
import csv
from dbOperations import getConnection

client, db = getConnection()
nameFile = f"Extracted (Date Min) - {str(datetime.now().timestamp()).replace('.','')}"
symbols = getSymbols()
f_date_start = FirstDate(2021,6,15)
f_date_end = LastDate(2022,6,30)

def generateHours():
    time_h = 8
    time_m = 55
    dates = ['Ativo', 'Qtd_Registros']
    while time_h != 19:
        time_m += 5
        if (time_m == 60):
            time_h += 1
            time_m = 0
        dates.append(f"{time_h}:{time_m}")
    
    return dates

with open(f'extracteds/{nameFile}.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=generateHours())
    writer.writeheader()
    
    for i, symbol in enumerate(symbols):
        datas = getTimesMin(db, symbol, f_date_start, f_date_end)
        qty_datas = len(datas)

        if qty_datas <= 0: continue

        count_dates = {}
        count_dates['Ativo'] = symbol
        count_dates['Qtd_Registros'] = qty_datas

        for data in datas:
            time_min = data['time']
            str_date = f"{time_min.hour}:{time_min.minute}"

            if(str_date in count_dates):
                count_dates[str_date] += 1 
            else: 
                count_dates[str_date] = 1

        writer.writerow(count_dates)
        print('Concluído: {:.2f}%'.format((i+1) / len(symbols) * 100))

client.close()
print("Ready!")
