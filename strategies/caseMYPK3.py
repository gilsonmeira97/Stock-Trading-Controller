import __sub__
from getRatesDatabase import *
from inputSymbols import getSymbols
import csv
from dbOperations import getConnection

client, db = getConnection()
nameFile = f"Extracted (Case MYPK3) - {str(datetime.now().timestamp()).replace('.','')}"
symbols = getSymbols()
f_StopGain = 0.006
f_StopLoss = -0.013
f_MinVolume = 100000
f_MinOcurrences = 15
f_varReference = -0.015
f_date_start = FirstDate(2021,12,15)
f_date_end = LastDate(2022,12,30)

with open(f'extracteds/{nameFile}.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Ativo', 'Qtd Registros', 'Ocorrencias', 'Acertos', 'Erros', '% Acerto', 'G/L Total', "G/L Med.", 'Max. Loss', 'Max. Gain', 'Date Loss', 'Date Gain', 'Volume Min', 'Volume Med'])
    
    for i, symbol in enumerate(symbols):
        data_result = getDayMinutes(db, symbol, f_date_start, f_date_end, f_MinVolume)
        if len(data_result) <= 0: continue
        data_result = data_result[0]
        datas = data_result['ticks']
        qty_datas = len(datas)
        day_reference = {'close': 0, 'open': 0, 'day_volume': 0}
        ocurrences = 0
        total_gain = 0
        avg_gain = 0
        erros = 0
        acertos = 0
        percentual_acertos = 0
        maximum_loss = 0
        maximum_gain = 0
        date_loss = None
        date_gain = None
        day_reference = {'close': 0, 'open': 0, 'day_volume': 0}

        for data in datas:
            open = data['open']
            close = data['close']
            high = data['high']
            low = data['low']
            ticks = data['ticks']
            dayOfWeek = data['date'].isoweekday()
            target_price = day_reference['close'] * (1 + f_varReference)

            if (dayOfWeek != 5) and (low <= target_price):
                ocurrences += 1
                variation = None
                is_entry = False

                for tick in ticks:
                    tick_open = tick['open']
                    tick_high = tick['high']
                    tick_low = tick['low']
                    tick_close = tick['close']

                    if is_entry is False and (tick_low <= target_price):
                        target_price = tick_open if tick_open < target_price else target_price
                        is_entry = True
                        continue
                    elif is_entry and tick_high / target_price - 1 >= f_StopGain :
                        variation = f_StopGain
                        break

                variation = (close / target_price - 1)  if (variation is None) else variation
                
                total_gain += variation

                if (variation < 0):
                    erros += 1
                    if variation < maximum_loss:
                        maximum_loss = variation 
                        date_loss = data['date']
                else:
                    acertos += 1
                    if variation > maximum_gain:
                        maximum_gain = variation
                        date_gain = data['date']

            day_reference = data

        if (ocurrences > 0):
            avg_gain = total_gain / ocurrences
            percentual_acertos = acertos / ocurrences
        
        if (ocurrences >= f_MinOcurrences) and ((percentual_acertos > 0.65 and avg_gain > 0.003) or (percentual_acertos <= 0.25 and avg_gain < -0.003)):
            writer.writerow([symbol, qty_datas, ocurrences, acertos, erros, percentual_acertos, total_gain, avg_gain, maximum_loss, maximum_gain, date_loss, date_gain, data_result['min_volume'], data_result['avg_volume']])
        print('Concluído: {:.2f}%'.format((i+1) / len(symbols) * 100))

client.close()
print("Ready!")
