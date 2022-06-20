import re

def getSymbols():
    #Lista com nome das ações
    symbols_shares = {}
    with open('COTAHIST_Reference.txt') as document:
        lines = document.readlines()
        for line in lines:
            id = line[0:2]
            cod = line[10:12]

            # Cod 02 = Lote padrão, Cod 08 = Recuperação Judicial (Consultar Layout B3)
            if id == '01' and cod in ['02', '08']:
                ticket = (line[12:24]).rstrip()
                symbols_shares[ticket] = ticket
    pass
    symbols_shares['WIN'] = 'WIN$'
    return symbols_shares