import __sub__
from dbOperations import getConnection
from getRatesDatabase import *
from inputSymbols import getSymbols
import csv

client, db = getConnection()
nameFile = f"Extracted Sexta-Segunda-Terca - {str(datetime.now().timestamp()).replace('.','')}"
symbols = getSymbols()
f_StopGain = 0.016
f_StopLoss = -0.016
f_MinVolume = 100000
f_MinOcurrences = 15
f_varReference = -0.025
f_date_start = FirstDate(2021,5,1)
f_date_end = LastDate(2022,5,30)

with open(f'extracteds/{nameFile}.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Ativo', 'Qtd Registros', 'Ocorrencias', 'Acertos', 'Erros', '% Acerto', 'G/L Total', "G/L Med.", 'Max. Loss', 'Max. Gain', 'Volume Min', 'Volume Med'])
    
    for i, symbol in enumerate(symbols):
        data_result = getDaysOfWeek(symbol, db, f_date_start, f_date_end, [1, 2, 3, 4, 5], f_MinVolume)
        if len(data_result) <= 0: continue
        data_result = data_result[0]
        datas = data_result['ticks']
        qty_datas = len(datas)
        last_object = None
        last_friday = None
        ocurrences = 0
        total_gain = 0
        avg_gain = 0
        erros = 0
        acertos = 0
        percentual_acertos = 0
        maximum_loss = 0
        maximum_gain = 0

        for data in datas:
            open = data['open']
            close = data['close']
            dayOfWeek = data['date'].isoweekday()
            if (dayOfWeek in [3, 4, 5]):
                last_friday = data
            elif (dayOfWeek == 1):
                last_object = data
            elif (last_object != None) and (last_friday != None) and (dayOfWeek == 2) and (last_friday['close'] / last_friday['open'] - 1) > f_varReference and (last_friday['date'] < last_object['date']):
                ocurrences += 1
                variation = (open / last_object['close'] - 1)

                total_gain += variation

                if (variation <= 0):
                    erros += 1
                    maximum_loss = variation if variation < maximum_loss else maximum_loss
                else:
                    acertos += 1
                    maximum_gain = variation if variation > maximum_gain else maximum_gain

                last_object = None

        if (ocurrences > 0):
            avg_gain = total_gain / ocurrences
            percentual_acertos = acertos / ocurrences
        
        if (ocurrences >= f_MinOcurrences) and ((percentual_acertos > 0.65 and avg_gain > 0.003) or (percentual_acertos <= 0.25 and avg_gain < -0.003)):
            writer.writerow([symbol, qty_datas, ocurrences, acertos, erros, percentual_acertos, total_gain, avg_gain, maximum_loss, maximum_gain, data_result['min_volume'], data_result['avg_volume']])
        print('Concluído: {:.2f}%'.format((i+1) / len(symbols) * 100))

client.close()
print("Ready!")
