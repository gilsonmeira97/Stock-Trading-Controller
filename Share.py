class Share:
    def __init__(self, time, symbol, open, high, low, close, tick_volume, real_volume):
        self.time = time
        self.symbol = symbol
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.tick_volume  = tick_volume  
        self.real_volume = real_volume
    def __str__(self):
        return '%s %s %.2f %.2f' % (self.ticket, self.open, self.close, self.real_volume)
