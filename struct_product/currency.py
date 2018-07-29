from camelq.struct_product import product

class currency(product.product):
    def __init__(self, code = '', size = 0, price = 1):
        self.code = code
        self.size = size
        self.price = price

