from dbConnection import db
from datetime import datetime

ticket = 'AZUL4'
fist_date = datetime(2021,4,13)
last_date = datetime(2022,4,14,23,59)
start_interval = datetime(1,1,1,11,15)
end_interval = datetime(1,1,1,13,20)

datas = db[ticket].aggregate([
  {'$match':
    {
      '$and': [
        {'time':
          {
            '$gte': fist_date,
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
    '$group': { 
        '_id': '$date', 
        "ticks" : {
            "$push" : "$tick"
        }
    }
  }
])