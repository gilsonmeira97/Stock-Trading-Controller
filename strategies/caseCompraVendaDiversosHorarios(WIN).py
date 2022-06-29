import __sub__
from getRatesDatabase import *
from inputSymbols import getSymbols
import csv
from dbOperations import getConnection

client, db = getConnection()
nameFile = f"Extracted Teste WIN - {str(datetime.now().timestamp()).replace('.','')}"
symbols = {"WIN": "WIN$"} #getSymbols()
f_StopGain = 100
f_StopLoss = -65
f_MinVolume = 100000
f_MinOcurrences = 15
f_varReference = 0.005
f_date_start = FirstDate(2022,3,4)
f_date_end = LastDate(2022,5,24)

with open(f'extracteds/{nameFile}.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Ativo', 'Qtd Registros', 'Ocorrencias', 'Acertos', 'Erros', '% Acerto', 'G/L Total', "G/L Med.", 'Max. Loss', 'Max. Gain', 'Date Loss', 'Date Gain', 'Volume Min', 'Volume Med', 'Horario Inicio'])
    
    for i, symbol in enumerate(symbols):
        data_result = getDayMinutes(db, symbol, f_date_start, f_date_end, f_MinVolume)
        if len(data_result) <= 0: continue
        data_result = data_result[0]
        datas = data_result['ticks']
        qty_datas = len(datas)
        
        time_h = 8
        time_m = 55
        while time_h != 17:
            time_m += 5
            if (time_m == 60):
                time_h += 1
                time_m = 0

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

            for data in datas:
                open = data['open']
                close = data['close']
                high = data['high']
                ticks = data['ticks']
                dayOfWeek = data['date'].isoweekday()
                tick_reference = None

                if (dayOfWeek != 0):
                    variation = None
                    ocurrences += 1
                    dt_tick_loss = None
                    dt_tick_gain = None
                    
                    for tick in ticks:
                        tick_date = tick['date']
                        tick_high = tick['high']
                        tick_low = tick['low']

                        if tick_date.hour == time_h and tick_date.minute == time_m:
                            tick_reference = tick
                            continue
                        elif (tick_reference != None) and ( tick_low - tick_reference['close'] <= f_StopLoss):
                            variation = f_StopLoss
                            dt_tick_loss = tick_date
                            break
                        elif (tick_reference != None) and ( tick_high - tick_reference['close'] >= f_StopGain):
                            variation = f_StopGain
                            dt_tick_gain = tick_date
                            break

                    variation = (close - tick_reference['close']) if (variation is None) else variation                
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
            writer.writerow([symbol, qty_datas, ocurrences, acertos, erros, percentual_acertos, total_gain, avg_gain, maximum_loss, maximum_gain, date_loss, date_gain, data_result['min_volume'], data_result['avg_volume'], f'{time_h}:{time_m}'])
    print('Concluído: {:.2f}%'.format((i+1) / len(symbols) * 100))

client.close()
print("Ready!")
