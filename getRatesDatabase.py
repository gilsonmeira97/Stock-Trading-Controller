from datetime import datetime

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
def getRatesInterval(db, ticket, first_date: FirstDate, last_date: LastDate, start_interval: DateTime, end_interval: DateTime, order = 1):
    datas = db[ticket].aggregate([
        {"$match":
            {
            "$and": [
                {"date":
                {
                    "$gte": first_date,
                    "$lte": last_date
                }
                }
            ],
            "$expr": { "$and": [ { "$and": [{"$gte": [{ "$hour": "$date" }, start_interval.hour ] }, {"$gte": [{ "$minute": "$date" }, start_interval.minute ] }]}, { "$and": [{"$lte": [{ "$hour": "$date" }, end_interval.hour ]}, {"$lte": [{ "$minute": "$date" }, end_interval.minute ]}] } ] }
            }
        },{
            "$project": {
                "date": {
                    "$dateToString": {
                    "date": "$date",
                    "format": "%Y-%m-%d"
                    }
                },
                "tick": { 
                    "date": "$date",
                    "open": "$open",
                    "close": "$close",
                    "high": "$high",
                    "low": "$low",
                    "tick_volume": "$tick_volume",
                    "real_volume": "$real_volume"
                }
            }
        },
        {
            "$sort": {
                "tick.date": 1
            }
        },
        {
            "$group": { 
                "_id": "$date", 
                "ticks" : {
                    "$push" : "$tick",
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

# Retorna duas cotações por dia
def getTwoRates(db, ticket, first_date: FirstDate, last_date: LastDate, start_interval: DateTime, end_interval: DateTime, order = 1):
    datas = db[ticket].aggregate([
        {"$match":
            {
            "$and": [
                {"date":
                {
                    "$gte": first_date,
                    "$lte": last_date
                }
                }
            ],
            "$expr": { "$or": [ { "$and": [{"$eq": [{ "$hour": "$date" }, start_interval.hour ] }, {"$eq": [{ "$minute": "$date" }, start_interval.minute ] }]}, { "$and": [{"$eq": [{ "$hour": "$date" }, end_interval.hour ]}, {"$eq": [{ "$minute": "$date" }, end_interval.minute ]}] } ] }
            }
        },{
            "$project": {
            "date": {
                "$dateToString": {
                "date": "$date",
                "format": "%Y-%m-%d"
                }
            },
            "tick": { 
                "date": "$date",
                "open": "$open",
                "close": "$close",
                "high": "$high",
                "low": "$low",
                "tick_volume": "$tick_volume",
                "real_volume": "$real_volume"
            }
            }
        },
        {
            "$sort": {
            "tick.date": 1
            }
        },
        {
            "$group": { 
                "_id": "$date", 
                "ticks" : {
                    "$push" : "$tick"
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

# Retorna as informações diarias (OHCL), podendo filtrar por dia da semana e/ou volume
def getDayRate(db, ticket, first_date: FirstDate, last_date: LastDate, minVolume = 0, daysOfWeek = [1, 2, 3, 4, 5], order = 1):
    datas = db[ticket].aggregate([
        {
            "$match": {
                "date": {
                    "$gte": first_date,
                    "$lte": last_date
                },
            "$expr": { "$in": [{ "$isoDayOfWeek": "$date" }, daysOfWeek] }
            }
        },
        {
            "$sort": {
            "date": 1
        }
        },
        {
            "$project": {
                
                "date": {
                    "$dateToString": {
                    "date": "$date",
                    "format": "%Y-%m-%d"
                    }
                },
                "tick": {
                    "date": "$date",
                    "open": "$open",
                    "close": "$close",
                    "high": "$high",
                    "low": "$low",
                    "real_volume": "$real_volume"
                }
            }
        },
        {
            "$group": {
                "_id": "$date",
                "date":{
                    "$first": "$tick.date"
                },
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
        },
        {
            "$group": {
                "_id": "null",
                "min_volume": {
                    "$min": "$day_volume"
                },
                "avg_volume": {
                    "$avg": "$day_volume"
                },
                "ticks": {
                    "$push": "$$ROOT"
                }
            }
        },
        {
            "$match": {
                "$expr": { "$gte": ["$min_volume", minVolume] }
            }
        }
    ])
    return list(datas)

# Retorna o horário diário das mínimas
def getTimesMin(db, ticket, first_date: FirstDate, last_date: LastDate):
    datas = db[ticket].aggregate([
        {
            "$match":
            {
            "$and": [
                {
                "date":
                    {
                        "$gte": first_date,
                        "$lte": last_date
                    }
                }
            ],
            }
        },
        {
            "$project": {
                "date": {
                    "$dateToString": {
                    "date": "$date",
                    "format": "%Y-%m-%d"
                    }
                },
                "tick": {
                    "date": "$date",
                    "open": "$open",
                    "close": "$close",
                    "high": "$high",
                    "low": "$low",
                    "tick_volume": "$tick_volume",
                    "real_volume": "$real_volume"
                }
            }
        },
        {
            "$sort": {
                "tick.low": 1
            }
        },
        {
            "$group": {
                "_id": "$date",
                "time": {"$first": "$tick.date"}
            }
        },
        {
            "$sort": {
                "_id": 1
            }
        }
    ])
    return list(datas)

# Retorna as informações de 5 em 5 min, filtradas por volume diário
def getDayMinutes(db, ticket, first_date: FirstDate, last_date: LastDate, minVolume = 0, order = 1):
    datas = db[ticket].aggregate([
        {
            "$match": {
                "date": {
                    "$gte": first_date,
                    "$lte": last_date
                }
            }
        },
        {
            "$sort": {
            "date": 1
        }
        },
        {
            "$project": {
                
                "date": {
                    "$dateToString": {
                    "date": "$date",
                    "format": "%Y-%m-%d"
                    }
                },
                "tick": {
                    "date": "$date",
                    "open": "$open",
                    "close": "$close",
                    "high": "$high",
                    "low": "$low",
                    "real_volume": "$real_volume"
                }
            }
        },
        {
            "$group": {
                "_id": "$date",
                "date":{
                    "$first": "$tick.date"
                },
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
                },
                "ticks": {
                    "$push": "$tick"
                }
            }
        },
        {
            "$sort": {
            "_id": order
            }
        },
        {
            "$group": {
                "_id": "null",
                "min_volume": {
                    "$min": "$day_volume"
                },
                "avg_volume": {
                    "$avg": "$day_volume"
                },
                "ticks": {
                    "$push": "$$ROOT"
                }
            }
        },
        {
            "$match": {
                "$expr": { "$gte": ["$min_volume", minVolume] }
            }
        }
    ])
    return list(datas)
