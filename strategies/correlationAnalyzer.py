import numpy as np
from pymongo import MongoClient

def percentageCalculate(datas):
    datas_list = list(datas)
    percent_list = []
    for i in range(0, len(datas_list) - 1):
        actual_price = datas_list[i]['close_price']
        next_price = datas_list[i + 1]['close_price']
        percent = (actual_price / next_price - 1) * 100
        percent_list.append(round(percent, 2))
    return percent_list

def analyze_pairs(pairOne, pairTwo, qty):
    client = MongoClient(port = 27017, serverSelectionTimeoutMS = 10000)
    db = client.stocks
    pairOneDatas = db[pairOne].find({}, {'close_price': 1, '_id': 0}).sort('date', -1).limit(qty)
    pairTwoDatas = db[pairTwo].find({}, {'close_price': 1, '_id': 0}).sort('date', -1).limit(qty)
    pairOneDatas = percentageCalculate(pairOneDatas)
    pairTwoDatas = percentageCalculate(pairTwoDatas)
    correlation = np.corrcoef(pairOneDatas,pairTwoDatas)[0,1]
    print(round(correlation, 3))

analyze_pairs('PETR3', 'PETR4', 46)
