from dbConnection import db
from datetime import datetime

#ticket = 'AZUL4'
#fist_date = datetime(2021,4,13)
#last_date = datetime(2022,4,14,23,59)
#start_interval = datetime(1,1,1,11,15)
#end_interval = datetime(1,1,1,13,20)

# Retorna as cotações de um intervalo de dia e horas
def getRatesInterval(ticket, first_date, last_date, start_interval, end_interval):
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
            '_id': -1
            }
        }  
        ])
    return datas

# Retorna duas cotações por dia
def getTwoRates(ticket, first_date, last_date, start_interval, end_interval):
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
            '_id': -1
            }
        }  
    ])
    return datas