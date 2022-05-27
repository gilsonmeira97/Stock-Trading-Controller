import __sub__
from getRatesDatabase import *
from inputSymbols import getSymbols
import csv
from dbOperations import getConnection

client, db = getConnection()
nameFile = f"Extracted Venda_Candle_Alta - {str(datetime.now().timestamp()).replace('.','')}"
symbols = getSymbols()
f_StopGain = 0.006
f_StopLoss = -0.013
f_MinVolume = 100000
f_MinOcurrences = 15
f_varReference = 0.005
f_date_start = FirstDate(2021,1,1)
f_date_end = LastDate(2022,6,30)

with open(f'extracteds/{nameFile}.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Ativo', 'Qtd Registros', 'Ocorrencias', 'Acertos', 'Erros', '% Acerto', 'G/L Total', "G/L Med.", 'Max. Loss', 'Max. Gain', 'Date Loss', 'Date Gain', 'Volume Min', 'Volume Med', 'Stop Loss'])
    
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
        max_ocilation = 0
        date_loss = None
        maximum_gain = 0
        date_gain = None

        ### Inicio 1ª verificação
        for data in datas:
            open = data['open']
            close = data['close']
            high = data['high']
            dayOfWeek = data['date'].isoweekday()

            if (day_reference['close'] > day_reference['open']) and ((open / day_reference['close'] - 1) >= f_varReference) and (dayOfWeek != 5):
                if close < open:
                    max_var = (high / open - 1) * -1
                    max_ocilation = max_var if max_var < max_ocilation else max_ocilation

            day_reference = data

        ### Inicio 2ª verificação
        day_reference = {'close': 0, 'open': 0, 'day_volume': 0}

        for data in datas:
            open = data['open']
            close = data['close']
            high = data['high']
            ticks = data['ticks']
            dayOfWeek = data['date'].isoweekday()

            if (day_reference['close'] > day_reference['open']) and ((open / day_reference['close'] - 1) >= f_varReference) and (dayOfWeek != 5):
                ocurrences += 1
                variation = None
                isStopMovel = False
                for tick in ticks:
                    if ((tick['high'] / open - 1) * -1) < max_ocilation and not isStopMovel:
                        variation = max_ocilation
                        break
                    elif ((tick['low'] / open - 1) * -1) >= f_StopGain and not isStopMovel:
                        variation = f_StopGain
                        isStopMovel = True
                        continue
                    elif (isStopMovel) and ((tick['high'] / open - 1) * -1) > variation:
                        variation = ((tick['close'] / open - 1) * -1)
                        continue
                    elif (isStopMovel) and ((tick['high'] / open - 1) * -1) <= variation:
                        break

                variation = ((close / open - 1) * -1) if (variation is None) else variation
                
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

            day_reference = data

        if (ocurrences > 0):
            avg_gain = total_gain / ocurrences
            percentual_acertos = acertos / ocurrences
        
        if (ocurrences >= f_MinOcurrences) and ((percentual_acertos > 0.65 and avg_gain > 0.003) or (percentual_acertos <= 0.25 and avg_gain < -0.003)):
            writer.writerow([symbol, qty_datas, ocurrences, acertos, erros, percentual_acertos, total_gain, avg_gain, maximum_loss, maximum_gain, date_loss, date_gain, data_result['min_volume'], data_result['avg_volume'], max_ocilation])
        print('Concluído: {:.2f}%'.format((i+1) / len(symbols) * 100))

client.close()
print("Ready!")
