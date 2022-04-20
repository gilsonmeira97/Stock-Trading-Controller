from getRatesDatabase import *
from inputSymbols import getSymbols
import csv

symbols = getSymbols()
f_MaxLoss = -0.04


with open('data_extracted.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Ativo', 'Qtd Registros', 'Ocorrencias', 'Acertos', 'Erros', '% Acerto', 'G/L Total', "G/L Med.", 'Max. Loss', 'Max. Gain', 'Volume Min', 'Volume Med'])
    
    for i, symbol in enumerate(symbols):
        datas = getDayRate(symbol,FirstDate(2021,4,18), LastDate(2022,4,20))
        qty_datas = 0
        last_object = None
        ocurrences = 0
        total_gain = 0
        avg_gain = 0
        erros = 0
        acertos = 0
        percentual_acertos = 0
        avg_volume = 0
        min_volume = 100**6
        maximum_loss = 0
        maximum_gain = 0
        for data in datas:
            qty_datas += 1
            volume = data['day_volume']
            open = data['open']
            close = data['close']
            high = data['high']
            min_volume = volume if volume < min_volume else min_volume
            avg_volume += volume

            if (last_object == None) and (close < open):
                last_object = data
            elif (last_object != None) and ((open / last_object['close'] - 1) <= -0.003):
                ocurrences += 1
                if ( ((high / open - 1) * -1) > f_MaxLoss):
                    variation = (close / open - 1) * -1
                else:
                    variation = f_MaxLoss
                total_gain += variation

                if (variation <= 0):
                    erros += 1
                    maximum_loss = variation if variation < maximum_loss else maximum_loss
                else:
                    acertos += 1
                    maximum_gain = variation if variation > maximum_gain else maximum_gain

                last_object = None
            elif (last_object != None):
                last_object = None

        if (qty_datas > 0) and (ocurrences > 0):
            avg_volume = avg_volume / qty_datas
            avg_gain = total_gain / ocurrences
            percentual_acertos = acertos / ocurrences
        
        if (ocurrences >= 15) and ((percentual_acertos > 0.65 and avg_gain > 0.003) or (percentual_acertos <= 0.25 and avg_gain < -0.003)) and min_volume >= 100000:
            writer.writerow([symbol, qty_datas, ocurrences, acertos, erros, percentual_acertos, total_gain, avg_gain, maximum_loss, maximum_gain, min_volume, avg_volume])
        print('Concluído: %.2f%' % ((i+1) / len(symbols)))
print("Ready!")
