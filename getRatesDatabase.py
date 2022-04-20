from pymongo import MongoClient
from datetime import datetime

ticket = 'PETR3'
def FirstDate(year: int, month: int, day: int):
    first_date = datetime(year, month, day)
    return first_date

def LastDate(year: int, month: int, day: int):
    last_date = datetime(year, month, day, 23, 59)
    return last_date

def DateTime(hour: int, minute: int):
    time = datetime(1, 1, 1, hour, minute)
    return time

# Retorna as cotações de um intervalo de dia e horas
def getRatesInterval(ticket, first_date: FirstDate, last_date: LastDate, start_interval: DateTime, end_interval: DateTime, order = 1):
    client = MongoClient(port = 27017, serverSelectionTimeoutMS = 10000)
    db = client.stocks
    datas = db[ticket].aggregate([
        {'$match':
            {
            '$and': [
                {'time':
                {
                    '$gte': first_date,
                    '$lte': last_date
                }
                }
            ],
            '$expr': { "$and": [ { "$and": [{"$gte": [{ "$hour": "$time" }, start_interval.hour ] }, {"$gte": [{ "$minute": "$time" }, start_interval.minute ] }]}, { "$and": [{"$lte": [{ "$hour": "$time" }, end_interval.hour ]}, {"$lte": [{ "$minute": "$time" }, end_interval.minute ]}] } ] }
            }
        },{
            '$project': {
            'date': {
                '$dateToString': {
                'date': '$time',
                'format': '%Y-%m-%d'
                }
            },
            'tick': { 
                "time": '$time',
                "open": '$open',
                "close": '$close',
                "high": '$high',
                "low": '$low',
                "tick_volume": '$tick_volume',
                "real_volume": '$real_volume'
            }
            }
        },
        {
            '$sort': {
            'tick.time': 1
            }
        },
        {
            '$group': { 
                '_id': '$date', 
                "ticks" : {
                    "$push" : "$tick",
                }
            }
        },
        {
            '$sort': {
            '_id': order
            }
        }  
    ])
    return datas

# Retorna duas cotações por dia
def getTwoRates(ticket, first_date: FirstDate, last_date: LastDate, start_interval: DateTime, end_interval: DateTime, order = 1):
    client = MongoClient(port = 27017, serverSelectionTimeoutMS = 10000)
    db = client.stocks
    datas = db[ticket].aggregate([
        {'$match':
            {
            '$and': [
                {'time':
                {
                    '$gte': first_date,
                    '$lte': last_date
                }
                }
            ],
            '$expr': { "$or": [ { "$and": [{"$eq": [{ "$hour": "$time" }, start_interval.hour ] }, {"$eq": [{ "$minute": "$time" }, start_interval.minute ] }]}, { "$and": [{"$eq": [{ "$hour": "$time" }, end_interval.hour ]}, {"$eq": [{ "$minute": "$time" }, end_interval.minute ]}] } ] }
            }
        },{
            '$project': {
            'date': {
                '$dateToString': {
                'date': '$time',
                'format': '%Y-%m-%d'
                }
            },
            'tick': { 
                "time": '$time',
                "open": '$open',
                "close": '$close',
                "high": '$high',
                "low": '$low',
                "tick_volume": '$tick_volume',
                "real_volume": '$real_volume'
            }
            }
        },
        {
            '$sort': {
            'tick.time': 1
            }
        },
        {
            '$group': { 
                '_id': '$date', 
                "ticks" : {
                    "$push" : "$tick"
                }
            }
        },
        {
            '$sort': {
            '_id': order
            }
        }  
    ])
    return datas

# Retorna as informações diarias (OHCL)
def getDayRate(ticket, first_date: FirstDate, last_date: LastDate, order = 1):
    client = MongoClient(port = 27017, serverSelectionTimeoutMS = 10000)
    db = client.stocks
    datas = db[ticket].aggregate([
        {
            "$match": {
                "time": {
                    '$gte': first_date,
                    '$lte': last_date
                }
            }
        },
        {
            "$sort": {
            "time": 1
        }
        },
        {
            '$project': {
                
                'date': {
                    "$dateToString": {
                    "date": '$time',
                    "format": '%Y-%m-%d'
                    }
                },
                "time": "$time",
                "tick": {
                    "time": '$time',
                    "open": '$open',
                    "close": '$close',
                    "high": '$high',
                    "low": '$low',
                    "tick_volume": '$tick_volume',
                    "real_volume": '$real_volume'
                }
            }
        },
        {
        "$group": {
            "_id": "$date",
            "open":{
                "$first": "$tick.open"
            },
            "close": {
                "$last": "$tick.close"
            },
            "high": {
                "$max": "$tick.high"
            },
            "low": {
                "$min": "$tick.low"
            },
            "day_volume": {
                "$sum": "$tick.real_volume"
            }
        }
        },
        {
            "$sort": {
            "_id": order
            }
        }
    ])
    return datas
