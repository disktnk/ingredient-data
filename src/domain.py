class Product(object):

    def __init__(self, id, name, ingreds=None):
        self.id = id
        self.name = name
        if ingreds is None:
            self.ingreds = []
        else:
            self.ingreds = ingreds
        self.ingreds_str = ''

    def add_ingreds(self, ingred_id):
        self.ingreds.append(ingred_id)

    def make_ingreds_list(self, ingreds):
        ingreds_list = [ingreds[i].name for i in self.ingreds]
        self.ingreds_str = ','.join(ingreds_list)


class Ingred(object):

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.products = []
        self.products_str = ''

    def extend_products(self, product_ids):
        self.products.extend(product_ids)

    def make_products_list(self, products):
        products_list = [products[i].name for i in self.products]
        self.products_str = ','.join(products_list)
