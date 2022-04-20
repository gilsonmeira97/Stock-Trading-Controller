from getRatesDatabase import *
from inputSymbols import getSymbols
import csv

symbols = getSymbols()

with open('data_extracted.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Ativo', 'Ocorrencias', 'Acertos', 'Erros', 'Performance', 'Percentual Acerto', 'Maximum_Loss', 'Maximum_Gain'])
    
    for symbol in symbols:
        datas = getDayRate(symbol,FirstDate(2021,4,18), LastDate(2022,4,20))
        last_object = None
        ocurrences = 0
        performance = 0
        erros = 0
        acertos = 0
        percentual_acertos = 0
        maximum_loss = 0
        maximum_gain = 0
        for data in datas:
            if (last_object == None) and (data['close'] < data['open']):
                last_object = data
            elif (last_object != None) and ((data['open'] / last_object['close'] - 1) <= -0.003):
                ocurrences += 1
                variation = (data['close'] / data['open'] - 1) * -100
                performance += variation
                if (variation <= 0):
                    erros += 1
                    maximum_loss = variation if variation < maximum_loss else maximum_loss
                else:
                    acertos += 1
                    maximum_gain = variation if variation > maximum_gain else maximum_gain
                last_object = None
            elif (last_object != None):
                last_object = None
        percentual_acertos = (acertos / ocurrences) * 100 if ocurrences > 0 else 0   
        writer.writerow([symbol, ocurrences, acertos, erros, performance, percentual_acertos, maximum_loss, maximum_gain])

print("Ready!")
