from camelq.struct_product import product, currency

class executions():
    def __init__(self):
        self.members = dict()

    def create_product(self, code=''):
        new_execution = []
        self.members.update({code : new_execution})
        self.members[code]
        return new_execution

    def products(self, code):
        if code in self.members.keys():
            return self.members[code]
        else:
            return self.create_product(code)

    def exchange(self, code = '', size = 0, price = 0):
        m_execution = self.products(code)
        res_size = 0
        if len(m_execution) > 0:
            if m_execution[0].size * size < 0:
                if size < 0:
                    diff = price - m_execution[0].price
                elif size > 0:
                    diff = m_execution[0].price - price
                    
                res_size = m_execution[0].size + size
                if abs(size) < abs(m_execution[0].size):
                    trade_size = abs(size)
                    m_execution[0].size = res_size
                    deposit = trade_size * price
                    profit = trade_size * diff
                    res_size = 0
                else:
                    trade_size = abs(m_execution[0].size)
                    m_execution.pop(0)
                    deposit = trade_size * price
                    profit = trade_size * diff
                    if res_size != 0:
                        t_d, t_p, _ = self.exchange(code,res_size,price)
                        return t_d + deposit, t_p + profit, 0
            else:
                deposit = size * price
                profit = 0
                m_execution.append(product.product(code = code, size = size, price = price))
        else:
            deposit = size * price
            profit = 0
            m_execution.append(product.product(code = code, size = size, price = price))
        return deposit, profit, res_size


# t = executions()
# size = 1
# print(t.exchange('mytest', 1, 10))
# print(t.exchange('mytest', 1, 10))
# print(t.exchange('mytest', 1, 10))
# print(t.exchange('mytest', -1, 1))
# for x in t.members['mytest']:
#     print(x.size, x.price)