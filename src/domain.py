class Product(object):

    def __init__(self, id, name, ingreds=None):
        self.id = id
        self.name = name
        if ingreds is None:
            self.ingreds = []
        else:
            self.ingreds = ingreds
        self.ingred_names = ''

    def add_ingreds(self, ingred_id):
        self.ingreds.append(ingred_id)

    def make_ingred_names(self, ingreds):
        self.ingred_names = [ingreds[i].name for i in self.ingreds]


class Ingred(object):

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.products = []
        self.product_names = []

    def extend_products(self, product_ids):
        self.products.extend(product_ids)

    def make_product_names(self, products):
        self.product_names = [products[i].name for i in self.products]
