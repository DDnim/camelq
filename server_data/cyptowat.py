from camelq.server_trade import cyptowat as trade
import json

api = trade.cyptowat()

class cyptowat():
    def ticker_list(self):
        res = api.get_ticker_list()

        if res['result_code'] != 0:
            return {'N/A'}
        else:
            return res['result_info']['result']
        
    def get_ohlc(self, market, product, periods):
        res = api.get_ohlc(market, product, periods)

        if res['result_code'] != 0:
            return {'N/A'}
        else:
            return res['result_info']

    def get_ohlcs(self, market, product):
        res = api.get_ohlcs(market, product)

        if res['result_code'] != 0:
            return {'N/A'}
        else:
            return res['result_info']