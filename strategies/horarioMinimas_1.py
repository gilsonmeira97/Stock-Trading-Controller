import __sub__
from getRatesDatabase import *
from inputSymbols import getSymbols
import csv

nameFile = f"Extracted (Date Min) - {str(datetime.now().timestamp()).replace('.','')}"
symbols = getSymbols()
f_date_start = FirstDate(2021,4,18)
f_date_end = LastDate(2022,4,20)

with open(f'extracteds/{nameFile}.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Ativo', 'Qtd Registros', 'Horario Minima', 'Ocorrencias'])
    
    for i, symbol in enumerate(symbols):
        datas = getTimesMin(symbol, f_date_start, f_date_end)
        qty_datas = len(datas)

        if qty_datas <= 0: continue

        count_dates = {}

        for data in datas:
            time_min = data['time']
            str_date = f"{time_min.hour}:{time_min.minute}"

            if(str_date in count_dates):
                count_dates[str_date] += 1 
            else: 
                count_dates[str_date] = 1
            
        tmp_i = list(count_dates.keys())[0]
        tmp_v = list(count_dates.values())[0]

        for ind, val in count_dates.items():
            if val > tmp_v:
                tmp_i = ind
                tmp_v = val

        writer.writerow([symbol, qty_datas, tmp_i, tmp_v])
        print('Concluído: {:.2f}%'.format((i+1) / len(symbols) * 100))

print("Ready!")
