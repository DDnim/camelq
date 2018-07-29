import logging
import datetime
from camelq.struct_account import account


logging.basicConfig(level=logging.INFO)

class server():
    def __init__(self, db, p_account = None, balance = 0, lantecy = 0, buy_commission = 0, sell_commission = 0, swap_commission = 0):
        
        self.db = db
        self.lantecy = lantecy
        self.buy_commission = buy_commission
        self.sell_commission = sell_commission
        self.swap_commission = swap_commission

        # todo
        self.data_server = []

        if p_account is None:
            self.account = account.account(default_currency='jpy',balance = balance)
        else:
            self.account = p_account
        
        self.t_profit = 0

        self.trade_profit = []
        self.trade_value = []
        self.trade_balance = []
    
    def order(self, product, side, size, time):
        profit = 0
        if side == 'buy':
            price = self.get_price(side, size, time)['price']
            if self.account.balance > 0:
                while size != 0:
                    profit, size = self.account.exchange(product, size, price)
                    self.account.balance = self.account.balance + profit
                    #deposit * (1 + self.buy_commission) +
            else:
                logging.error('Balance is not enough')
        elif side == 'sell':
            price = self.get_price(side, size, time)['price']
            if self.account.balance > 0:
                while size != 0:
                    profit, size = self.account.exchange(product, -size, price)
                    self.account.balance = self.account.balance + profit
                    #+ deposit * (1 - self.sell_commission)
            else:
                logging.error('Product is not enough')
        else:
            logging.error('Side need be [buy] or [sell], inputed:' + side)
        print(datetime.datetime.fromtimestamp(time))

    def get_price(self, side, size, time):
        cur = self.db.get_db_cur()
        if side == 'BUY':
            _side = 'B'
        else:
            _side = 'S'
        
        query_sql = "SELECT * FROM bitflyer_executions_btc_jpy where id = (SELECT min(id) FROM bitflyer_executions_btc_jpy WHERE u_time = (SELECT MIN(u_time) FROM bitflyer_executions_btc_jpy where u_time > {} and side = '{}'))".format(time + self.lantecy, _side)
        #logging.debug(query_sql)
        cur.execute(query_sql)

        column_names = [desc[0] for desc in cur.description]
        d = dict()
        for row in cur:
            d.update(zip(column_names,row))
        return d

    def get_ohlc(self, code, time):
        cur = self.db.get_db_cur()
        time_str = datetime.datetime.fromtimestamp(time)

        query_sql = "SELECT * FROM bitflyer_executions_btc_jpy_ohlc where time >= '{}' order by time LIMIT 1 OFFSET 0".format(time_str)
        #logging.debug(query_sql)
        cur.execute(query_sql)

        column_names = [desc[0] for desc in cur.description]
        d = dict()
        for row in cur:
            d.update(zip(column_names,row))
        return d

    def get_balance(self):
        return float(self.account.balance)

    def get_executions(self, code = ''):
        return self.account.executions[code]

    def get_executions_size(self, code = ''):
        s = 0
        if code in self.account.executions.keys():
            for v in self.account.executions[code]:
                s = s + v.size
        return s

    def get_executions_value(self, code = ''):
        s = 0
        if code in self.account.executions.keys():
            for v in self.account.executions[code]:
                s = s + v.size * v.price
        return s

    def get_executions_profit(self, time):
        s = 0
        for key, value in self.account.executions.items():
            if key != self.account.default_currency :
                size_sum = 0
                value_sum = 0
                price = float(self.get_ohlc(key, time)['close'])
                for v in value:
                    size_sum = size_sum + v.size 
                    value_sum = value_sum + v.size * float(v.price)
                if size_sum != 0:
                    s = s + (price - value_sum / size_sum) * size_sum
        return float(s)
        

    def refresh(self, time):
        blance = self.get_balance()
        profit = self.get_executions_profit(time)
        self.trade_balance.append(blance)
        self.trade_profit.append(profit)
        self.trade_value.append(blance + profit)
