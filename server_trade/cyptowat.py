import requests
import datetime
import hashlib, hmac, json
from camelq.common.common_request import *

class cyptowat():
    def __init__(self, key='', secret=b'', entry='https://api.cryptowat.ch/'):
        self.entry = entry
        self.key = key
        self.secret = secret

    def get_ticker_list(self):
        '''Get ticker list.'''
        response = requests.get(self.entry + 'markets/prices')
        if response.status_code == 200:
            return request_result(0, json.loads(response.text))
        else:
            return request_result(100, 'Request error: ' + str(response.status_code))

    def get_ohlc(self, market, product, periods=0):
        '''Get ohlc.'''
        response = requests.get(self.entry + 'markets/' + market + '/' + product + '/ohlc?periods=' + periods)
        if response.status_code == 200:
            return request_result(0, json.loads(response.text)['result'][str(periods)])
        else:
            return request_result(100, 'Request error: ' + str(response.status_code))

    def get_ohlcs(self, market, product):
        '''Get ohlc list.'''
        response = requests.get(self.entry + 'markets/' + market + '/' + product + '/ohlc')
        if response.status_code == 200:
            return request_result(0, json.loads(response.text)['result'])
        else:
            return request_result(100, 'Request error: ' + str(response.status_code))
