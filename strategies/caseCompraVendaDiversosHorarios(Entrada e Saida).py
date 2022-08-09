import __sub__
from getRatesDatabase import *
from inputSymbols import getSymbols
import csv
from dbOperations import getConnection

client, db = getConnection()
nameFile = f"Extracted Diversos horários(Entrada e Saída) - {str(datetime.now().timestamp()).replace('.','')}"
symbols = getSymbols()
f_StopGain = 0.005
f_StopLoss = 0
f_MinVolume = 100000
f_MinOcurrences = 15
f_varReference = 0.005
f_date_start = FirstDate(2021,12,15)
f_date_end = LastDate(2022,12,30)

def verifyDate(date, reference = [3]):
    if date in reference:
        return True
    return False

with open(f'extracteds/{nameFile}.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Ativo', 'Qtd Registros', 'Ocorrencias', 'Acertos', 'Erros', '% Acerto', 'G/L Total', "G/L Med.", 'Max. Loss', 'Max. Gain', 'Date Loss', 'Date Gain', 'Volume Min', 'Volume Med', 'Entrada', 'Saída'])
    
    for i, symbol in enumerate(symbols):
        data_result = getDayMinutes(db, symbol, f_date_start, f_date_end, f_MinVolume)
        if len(data_result) <= 0: continue
        data_result = data_result[0]
        datas = data_result['ticks']
        qty_datas = len(datas)
        
        time_h = 9
        time_m = 55
        while not (time_h == 16 and time_m == 50) :
            time_m += 5
            if (time_m == 60):
                time_h += 1
                time_m = 0

            _time_h = time_h
            _time_m = time_m
            while not (_time_h == 16 and _time_m == 50) :
                _time_m += 5
                if (_time_m == 60):
                    _time_h += 1
                    _time_m = 0
            
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
                    date_data = data['date']
                    dayOfWeek = data['date'].isoweekday()
                    f_tick_reference = None

                    if verifyDate(dayOfWeek):
                        variation = None
                        
                        for tick in ticks:
                            tick_date = tick['date']
                            tick_high = tick['high']
                            tick_close = tick['close']
                            tick_low = tick['low']

                            if f_tick_reference is None and tick_date.hour == time_h and tick_date.minute == time_m:
                                f_tick_reference = tick
                                continue
                            elif f_tick_reference is not None and tick_date.hour == _time_h and tick_date.minute == _time_m:
                                variation = tick_close / f_tick_reference['close'] - 1
                                break
                        
                        if f_tick_reference is None:
                            continue
                        
                        ocurrences += 1
                        variation = (close / f_tick_reference['close'] - 1) if (variation is None) else variation                
                        total_gain += variation

                        if (variation <= 0):
                            erros += 1
                            if variation < maximum_loss:
                                maximum_loss = variation 
                                date_loss = date_data
                        else:
                            acertos += 1
                            if variation > maximum_gain:
                                maximum_gain = variation
                                date_gain = date_data

                if (ocurrences > 0):
                    avg_gain = total_gain / ocurrences
                    percentual_acertos = acertos / ocurrences
                
                if (ocurrences >= f_MinOcurrences) and ((percentual_acertos > 0.65 and avg_gain > 0.003) or (percentual_acertos <= 0.25 and avg_gain < -0.003)):
                    writer.writerow([symbol, qty_datas, ocurrences, acertos, erros, percentual_acertos, total_gain, avg_gain, maximum_loss, maximum_gain, date_loss, date_gain, data_result['min_volume'], data_result['avg_volume'], f'{time_h}:{time_m}', f'{_time_h}:{_time_m}'])
        print('Concluído: {:.2f}%'.format((i+1) / len(symbols) * 100))

client.close()
print("Ready!")
