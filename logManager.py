from datetime import datetime

def writeLog(file, message):
    file.write(f'{datetime.now()}\n')
    file.write(f'{message}\n\n')