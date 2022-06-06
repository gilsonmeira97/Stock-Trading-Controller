import __sub__
from getRatesDatabase import *
from inputSymbols import getSymbols
import csv
from dbOperations import getConnection

client, db = getConnection()
nameFile = f"Extracted Teste WIN - {str(datetime.now().timestamp()).replace('.','')}"
symbols = {"WIN": "WIN$"} #getSymbols()
f_StopGain = 100
f_StopMovel = 50
f_StopTarget = 150
f_StopLoss = -100
f_MinVolume = 100000
f_MinOcurrences = 15
f_varReference = 800
f_date_start = FirstDate(2022,3,5)
f_date_end = LastDate(2022,5,24)

with open(f'extracteds/{nameFile}.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Ativo', 'Qtd Registros', 'Ocorrencias', 'Acertos', 'Erros', '% Acerto', 'G/L Total', "G/L Med.", 'Max. Loss', 'Max. Gain', 'Date Loss', 'Date Gain', 'Volume Min', 'Volume Med'])
    
    for i, symbol in enumerate(symbols):
        data_result = getDayMinutes(db, symbol, f_date_start, f_date_end, f_MinVolume)
        if len(data_result) <= 0: continue
        data_result = data_result[0]
        datas = data_result['ticks']
        qty_datas = len(datas)

        ocurrences = 0
        date_loss = None
        date_gain = None
        total_gain = 0
        avg_gain = 0
        erros = 0
        acertos = 0
        percentual_acertos = 0
        maximum_loss = 0
        maximum_gain = 0
        day_reference = {'close': 300000}

        for data in datas:
            open = data['open']
            close = data['close']
            high = data['high']
            ticks = data['ticks']
            dayOfWeek = data['date'].isoweekday()
            tick_reference = {'start': None, 'st_movel': None}

            if (dayOfWeek != 0):
                variation = None
                dt_tick_loss = None
                dt_tick_gain = None
                
                for tick in ticks:
                    tick_date = tick['date']
                    tick_open = tick['open']
                    tick_close = tick['close']
                    tick_high = tick['high']
                    tick_low = tick['low']

                    if tick_date.hour == 9 and tick_date.minute == 10:
                        if (open - day_reference['close'] >= f_varReference) and (tick_close < open):
                            tick_reference['open'] = open
                            tick_reference['close'] = tick_close
                            ocurrences += 1
                            continue
                        else:
                            break
                    elif (tick_date.hour == 9 and tick_date.minute == 15):
                        tick_reference['start'] = tick_open
                        
                    if (tick_reference['start'] != None):
                        if(tick_low - tick_reference['start'] <= f_StopLoss) and (tick_reference['st_movel'] == None):
                            variation = f_StopLoss
                            dt_tick_loss = tick_date
                            break
                        elif (tick_high - tick_reference['start'] >= f_StopGain) and (tick_reference['st_movel'] == None):
                            tick_reference['st_movel'] = tick_reference['start'] + f_StopGain
                            continue
                        elif (tick_reference['st_movel'] != None) and (tick_low <= tick_reference['st_movel']):
                            variation = tick_reference['st_movel'] - tick_reference['start']
                            dt_tick_gain = tick_date
                            break
                        elif (tick_reference['st_movel'] != None) and (tick_low > tick_reference['st_movel']) and (tick_high - tick_reference['st_movel'] >= f_StopTarget):
                            tick_reference['st_movel'] += f_StopMovel
                            continue
                    
                    if (tick_reference['start'] != None) and (tick_date.hour == 16 and tick_date.minute == 25):
                        variation = tick_close - tick_reference['start']
                        dt_tick_loss = tick_date
                        dt_tick_gain = tick_date
                        break
                
                day_reference = data
                if (tick_reference['start'] == None): continue

                total_gain += variation

                if (variation <= 0):
                    erros += 1
                    if variation < maximum_loss:
                        maximum_loss = variation 
                        date_loss = dt_tick_loss
                else:
                    acertos += 1
                    if variation > maximum_gain:
                        maximum_gain = variation
                        date_gain = dt_tick_gain

            

        if (ocurrences > 0):
            avg_gain = total_gain / ocurrences
            percentual_acertos = acertos / ocurrences
        
        #if (ocurrences >= f_MinOcurrences) and ((percentual_acertos > 0.65 and avg_gain > 0.003) or (percentual_acertos <= 0.25 and avg_gain < -0.003)):
        writer.writerow([symbol, qty_datas, ocurrences, acertos, erros, percentual_acertos, total_gain, avg_gain, maximum_loss, maximum_gain, date_loss, date_gain, data_result['min_volume'], data_result['avg_volume']])
    print('Concluído: {:.2f}%'.format((i+1) / len(symbols) * 100))

client.close()
print("Ready!")
