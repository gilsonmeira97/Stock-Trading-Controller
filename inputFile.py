from datetime import datetime
stocks = {}

class Stock:
    def __init__(self, date, ticket, name, open_price, max_price, min_price, avg_price, close_price, qty_exchange, qty_stocks, total_value):
        self.date = date
        self.ticket = ticket
        self.name = name
        self.open_price = open_price
        self.max_price = max_price
        self.min_price = min_price
        self.avg_price = avg_price
        self.close_price = close_price
        self.qty_exchange = qty_exchange
        self.qty_stocks = qty_stocks
        self.total_value = total_value
    def __str__(self):
        return '%s %s %.2f %.2f' % (self.ticket, self.date, self.open_price, self.close_price)

def convertToDecimal(input):
    return int(input)/100

def formatToDate(date):
    year = int(date[0:4])
    month = int(date[4:6])
    day = int(date[6:8])
    return datetime(year, month, day)

with open('COTAHIST_A2021.txt') as document:
    lines = document.readlines()
    for line in lines:
        id = line[0:2]
        if id == '01':
            date = formatToDate(line[2:10])  ## Data     
            ticket = (line[12:24]).rstrip()
            name = (line[27:39]).rstrip() ## Nome da campania
            open_price = convertToDecimal(line[56:69]) ## Preço Abertura
            max_price = convertToDecimal(line[69:82]) ## Preço Máximo
            min_price = convertToDecimal(line[82:95]) ## Preço Mínimo
            avg_price = convertToDecimal(line[95:108]) ## Preço Médio
            close_price = convertToDecimal(line[108:121]) ## Preço Fechamento
            qty_exchange = int(line[147:152]) ## Número de Negócios
            qty_stocks = int(line[152:170]) ## Quantidade de papeis
            total_value = convertToDecimal(line[170:188]) ## Volume de Negócios (R$)

            newStock = Stock(date, ticket, name, open_price, max_price, min_price, avg_price, close_price, qty_exchange, qty_stocks, total_value)

            if ticket not in stocks:
                stocks[ticket] = []
            stocks[ticket].append(newStock)
    pass