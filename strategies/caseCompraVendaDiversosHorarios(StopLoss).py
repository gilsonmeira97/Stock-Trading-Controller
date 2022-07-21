import __sub__
from getRatesDatabase import *
from inputSymbols import getSymbols
import csv
from dbOperations import getConnection

client, db = getConnection()
nameFile = f"Extracted Diversos horários(Todos - StopLoss) - {str(datetime.now().timestamp()).replace('.','')}"
symbols = getSymbols()
f_StopGain = 0.009
f_StopLoss = 0
f_MinVolume = 100000
f_MinOcurrences = 15
f_varReference = 0.005
f_date_start = FirstDate(2021,12,15)
f_date_end = LastDate(2022,12,30)

def verifyDate(date, reference = [4]):
    if date in reference:
        return True
    return False

with open(f'extracteds/{nameFile}.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Ativo', 'Qtd Registros', 'Ocorrencias', 'Acertos', 'Erros', '% Acerto', 'G/L Total', "G/L Med.", 'Max. Loss', 'Max. Gain', 'Date Loss', 'Date Gain', 'Volume Min', 'Volume Med', 'Horario Inicio', 'StopLoss'])
    
    for i, symbol in enumerate(symbols):
        data_result = getDayMinutes(db, symbol, f_date_start, f_date_end, f_MinVolume)
        if len(data_result) <= 0: continue
        data_result = data_result[0]
        datas = data_result['ticks']
        qty_datas = len(datas)
        
        time_h = 9
        time_m = 55
        while not (time_h == 16 and time_m == 55) :
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
            max_ocilation = 0

            ### Inicio 1ª verificação
            for data in datas:
                open = data['open']
                close = data['close']
                ticks = data['ticks']
                dayOfWeek = data['date'].isoweekday()
                tick_reference = None
                var_test = None
                last_low = 0

                if verifyDate(dayOfWeek):
                    for tick in ticks:
                        tick_date = tick['date']
                        tick_high = tick['high']
                        tick_low = tick['low']
                        tick_close = tick['close']
                        
                        if (tick_reference != None):
                            var_low = tick_low / tick_reference - 1
                            last_low = var_low if var_low < last_low else last_low

                        if tick_date.hour == time_h and tick_date.minute == time_m:
                            tick_reference = tick_close
                            continue
                        elif (tick_reference != None) and ( (tick_high / tick_reference - 1) >= f_StopGain):
                            var_test = f_StopGain
                            break

                    if tick_reference is None:
                        continue

                    var_test = (close / tick_reference - 1) if (var_test is None) else var_test
                    
                    if var_test > 0:
                        max_ocilation =  last_low if last_low < max_ocilation else max_ocilation

            ### Inicio 2ª verificação

            max_ocilation -= 0.0005    
            
            for data in datas:
                close = data['close']
                high = data['high']
                ticks = data['ticks']
                dayOfWeek = data['date'].isoweekday()
                tick_reference = None

                if verifyDate(dayOfWeek):
                    variation = None
                    
                    for tick in ticks:
                        tick_date = tick['date']
                        tick_high = tick['high']
                        tick_low = tick['low']

                        if tick_date.hour == time_h and tick_date.minute == time_m:
                            tick_reference = tick['close']
                            continue
                        elif (tick_reference != None) and ((tick_low / tick_reference - 1) <= max_ocilation):
                            variation = max_ocilation
                            break
                        elif (tick_reference != None) and ((tick_high / tick_reference - 1) >= f_StopGain):
                            variation = f_StopGain
                            break
                    
                    if tick_reference is None:
                        continue
                    
                    ocurrences += 1
                    variation = (close / tick_reference - 1) if (variation is None) else variation                
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

            if (ocurrences > 0):
                avg_gain = total_gain / ocurrences
                percentual_acertos = acertos / ocurrences
            
            if (ocurrences >= f_MinOcurrences) and ((percentual_acertos > 0.65 and avg_gain > 0.003) or (percentual_acertos <= 0.25 and avg_gain < -0.003)):
                writer.writerow([symbol, qty_datas, ocurrences, acertos, erros, percentual_acertos, total_gain, avg_gain, maximum_loss, maximum_gain, date_loss, date_gain, data_result['min_volume'], data_result['avg_volume'], f'{time_h}:{time_m}', max_ocilation])
        print('Concluído: {:.2f}%'.format((i+1) / len(symbols) * 100))

client.close()
print("Ready!")
