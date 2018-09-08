import sys
import json

from camelq.module_bot import TestTrade_MA20180720 as quant


setting = json.load(open(sys.argv[1], 'r'))

q = quant.quant(setting)
q.run()