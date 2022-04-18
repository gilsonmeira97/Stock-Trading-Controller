from datetime import datetime

class Share:
    def __init__(self, time, open, high, low, close, tick_volume, real_volume):
        self.time = datetime.utcfromtimestamp(time)
        self.open = float(open)
        self.high = float(high)
        self.low = float(low)
        self.close = float(close)
        self.tick_volume  = int(tick_volume)
        self.real_volume = int(real_volume)
    def __str__(self):
        return '%s %.2f %.2f %i' % (self.time, self.open, self.close, self.real_volume)
