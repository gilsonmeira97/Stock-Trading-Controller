import __sub__
from getRatesDatabase import *
from inputSymbols import getSymbols
import csv
from dbOperations import getConnection

client, db = getConnection()
nameFile = f"Extracted Fechamento Negativo(Stop Loss) - {str(datetime.now().timestamp()).replace('.','')}"
symbols = getSymbols()
f_StopGain = 0.008
f_StopLoss = -0.016
f_MinVolume = 100000
f_MinOcurrences = 15
f_varReference = -0.025
f_date_start = FirstDate(2021,12,15)
f_date_end = LastDate(2022,12,30)

with open(f'extracteds/{nameFile}.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Ativo', 'Qtd Registros', 'Ocorrencias', 'Acertos', 'Erros', '% Acerto', 'G/L Total', "G/L Med.", 'Max. Loss', 'Max. Gain', 'Date Loss', 'Date Gain', 'Volume Min', 'Volume Med', 'Stop_loss'])
    
    for i, symbol in enumerate(symbols):
        data_result = getDayMinutes(db, symbol, f_date_start, f_date_end, f_MinVolume)
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
        date_loss = None
        date_gain = None
        max_ocilation = 0

        ### Inicio 1ª verificação
        for data in datas:
            open = data['open']
            close = data['close']
            high = data['high']
            ticks = data['ticks']
            dayOfWeek = data['date'].isoweekday()

            if (last_object != None):
                openClose = ((open / last_object['close']) - 1)

                if openClose >= f_StopGain:
                    var_test = openClose
                elif ((high / last_object['close']) - 1) >= f_StopGain:
                    var_test = f_StopGain
                else:
                    var_test = (close / last_object['close'] - 1)
                    
                if var_test > 0:
                    for tick in ticks:
                        variation_tick = (tick['low'] / last_object['close'] - 1)
                        max_ocilation =  variation_tick if variation_tick < max_ocilation else max_ocilation
                        
                        if (tick['high'] / last_object['close'] - 1) >= f_StopGain:
                            break
                        
                last_object = None

            if dayOfWeek != 5:
                last_object = data

        ### Inicio 2ª verificação

        last_object = None
        max_ocilation += 0.0005    

        for data in datas:
            open = data['open']
            close = data['close']
            high = data['high']
            ticks = data['ticks']
            dayOfWeek = data['date'].isoweekday()
            variation = None

            if (last_object != None):
                ocurrences += 1
                openClose = ((open / last_object['close']) - 1)

                for tick in ticks:
                    if openClose >= f_StopGain or openClose <= max_ocilation:
                        variation = openClose
                        break
                    elif ((tick['low'] / last_object['close']) - 1) <= max_ocilation:
                        variation = max_ocilation
                        break
                    elif ((tick['high'] / last_object['close']) - 1) >= f_StopGain:
                        variation = f_StopGain
                        break

                variation = close / last_object['close'] - 1 if variation is None else variation

                total_gain += variation

                if (variation <= 0):
                    erros += 1
                    if variation < maximum_loss:
                        maximum_loss = variation 
                        date_loss = data['date']
                else:
                    acertos += 1
                    if variation > maximum_gain:
                        maximum_gain = variation
                        date_gain = data['date']

                last_object = None

            if dayOfWeek != 5:
                last_object = data

        if (ocurrences > 0):
            avg_gain = total_gain / ocurrences
            percentual_acertos = acertos / ocurrences
        
        if (ocurrences >= f_MinOcurrences) and ((percentual_acertos > 0.65 and avg_gain > 0.003) or (percentual_acertos <= 0.25 and avg_gain < -0.003)):
            writer.writerow([symbol, qty_datas, ocurrences, acertos, erros, percentual_acertos, total_gain, avg_gain, maximum_loss, maximum_gain, date_loss, date_gain, data_result['min_volume'], data_result['avg_volume'], max_ocilation])
        print('Concluído: {:.2f}%'.format((i+1) / len(symbols) * 100))

client.close()
print("Ready!")
