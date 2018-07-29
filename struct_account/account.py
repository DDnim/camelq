from camelq.struct_product import currency, product
from camelq.struct_execution import executions

class account():
    def __init__(self, default_currency = 'jpy', balance = 0):
        self.__executions = executions.executions()
        self.default_currency = default_currency
        
        self.__executions.exchange(default_currency, balance, 1)
        self.profit = 0
        self.value = 0
    
    def exchange(self, code, size, price):
        return self.__executions.exchange(code, size, price)

    @property
    def balance(self):
        return None

    @balance.setter
    def balance(self, v):
        self.__executions.members[self.default_currency][0].size = v

    @balance.getter
    def balance(self):
        return self.__executions.members[self.default_currency][0].size

    @property
    def executions(self):
        return None

    @executions.getter
    def executions(self):
        return self.__executions.members


# t = account(balance=50000)
# print(t.balance)
# size = 1
# print(t.exchange('mytest', 4, 8))
# print(t.exchange('mytest', -1, 7))
# # 3 8
# print(t.exchange('mytest', -8, 9))
# # -5 9
# print(t.exchange('mytest', -2, 10))
# # -2 10
# print(t.exchange('mytest', 16, 10))
# # -5 9 5
# # -2 10
# # 9 10

# print(t.exchange('mytest', 14, 12))
# for x in t.executions['mytest']:
#     print(x.size, x.price)