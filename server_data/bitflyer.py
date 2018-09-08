from camelq.db_data import bitflyer as database
import pandas
import datetime,time
import numpy
from camelq.server_trade import bitflyer
import json
class indicator_bitflyer():
    def __init__(self, code):
        self.code = code
    
    def _refresh_ohlc(self, time_from, time_to):
        connection = database.get_db_connection()
        cur = database.get_db_cur()

        cur.execute("SELECT MAX(time) FROM bitflyer_executions_{}_ohlc".format(self.code))
        for row in cur:
            fr = row[0]
        if fr is None:
            fr = time_from
        to = time_to

        for i in range(fr, to, 86400):
            query = "SELECT u_time, price FROM bitflyer_executions_{} WHERE {} <= u_time AND u_time < {}".format(self.code, str(i), str(i + 86400))
            data = pandas.read_sql_query(query, connection)
            # cur.execute(query, time_from, time_to)
            # query = "SELECT MAX(time) FROM bitflyer_executions_{}_ohlc")
            # data = self.sql_get_all(i, i + 86400 - 1)
            
            df = pandas.DataFrame(data, columns=['u_time','price'],dtype='float')
            #df['Time'] = pandas.to_datetime(df.u_time, unit='s')
            df.index = pandas.DatetimeIndex(pandas.to_datetime(df.u_time, unit='s'))
            ohlc = df.price.resample('T').ohlc()
            print(ohlc)
            for index, row in ohlc.dropna().iterrows():
                query = "INSERT INTO bitflyer_executions_" + self.code + "_ohlc SELECT %s,%s,%s,%s,%s WHERE NOT EXISTS (SELECT time FROM bitflyer_executions_" + self.code + "_ohlc WHERE time = %s)"
                cur.execute(query, (int(index.timestamp()), row['open'], row['high'], row['low'], row['close'],int(index.timestamp()),))

            last = ohlc.iloc[-1:]
            for index, row in last.dropna().iterrows():
                query = "UPDATE bitflyer_executions_" + self.code + "_ohlc set open = %s, high = %s, low = %s, close = %s where time = %s"
                cur.execute(query, (row['open'], row['high'], row['low'], row['close'],int(index.timestamp()),))

    def get_ohlc(self, time_from, time_to = 0):
        connection = database.get_db_connection()
        if time_to == 0:
            time_to = datetime.datetime.now().strftime('%s')
        d = pandas.read_sql_query("SELECT * FROM bitflyer_executions_{}_ohlc WHERE '{}' <= time and time < '{}'".format(self.code, time_from, time_to), connection,'time')
        return d

    def ticker(self,product):
        res = api.get_ticker(product)
        if res['result_code'] != 0:
            return {'N/A'}
        else:
            return {'market' : 'bitflyer', 'product' : product,'price' : res['result_info']['ltp']}

d = indicator_bitflyer('FX_BTC_JPY')
fr = int(datetime.datetime(2018, 7, 10).timestamp())
to = int(datetime.datetime.now().timestamp())
print(fr,to)
d._refresh_ohlc(fr, to)