import re

regex = re.compile(r'([A-Z]{4})(\d{1,2}\b)')

def getSymbols():
    #Lista com nome das ações
    symbols_shares = {}
    with open('COTAHIST_Reference.txt') as document:
        lines = document.readlines()
        for line in lines:
            id = line[0:2]
            if id == '01':
                ticket = (line[12:24]).rstrip()
                
                #Adiciona somente as ações que batem com a regex
                if re.match(regex,ticket) != None and ticket not in symbols_shares:
                    symbols_shares[ticket] = ticket
    pass
    symbols_shares['WIN'] = 'WIN$'
    return symbols_shares
