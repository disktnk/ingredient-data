import argparse
import datetime
import json
import os
import re

import texttable
import zenhan


SHAPED_FILE_NAME = 'data.json'


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


def get_formatted_table():
    table = texttable.Texttable()
    table.set_deco(texttable.Texttable.HEADER)
    return table


def regularization(name):
    return zenhan.z2h(zenhan.h2z(name, mode=4), mode=3)


def get_data(path):
    need_reload = False
    abs_path = os.path.abspath(path)
    mtime = datetime.datetime.fromtimestamp(
        os.path.getmtime(abs_path)).isoformat()
    if os.path.exists(SHAPED_FILE_NAME):
        with open(SHAPED_FILE_NAME, 'r') as f:
            shaped_file = json.load(f)
        if shaped_file['path'] != abs_path:
            need_reload = True
        if shaped_file['mtime'] != mtime:
            need_reload = True
    else:
        need_reload = True

    products, ingreds = {}, {}
    if need_reload:
        with open(abs_path, 'r') as f:
            lines = f.readlines()
        item_set = {}
        temp_product = None
        for line in lines:
            line = line.strip()
            if line == '':
                if temp_product is None:
                    # previous products are recorded
                    continue
                # previous product is not recorded
                p = Product(
                    temp_product.id, temp_product.name, temp_product.ingreds)
                p.make_ingreds_list(ingreds)
                products[p.id] = p
                temp_product = None
                continue
            if temp_product is None:
                # this line is new product
                temp_product = Product(len(products)+1, regularization(line))
                continue
            # this line is about ingredients
            items = re.split('[,，、]', line)
            for item in items:
                name = regularization(item)
                if name in item_set:
                    ingred = item_set[name]
                    temp_product.add_ingreds(ingred.id)
                    continue
                ingred = Ingred(len(item_set)+1, name)
                item_set[name] = ingred
                ingreds[ingred.id] = ingred
                temp_product.add_ingreds(ingred.id)
        if temp_product is not None:
            # collect last product if remained
            p = Product(
                temp_product.id, temp_product.name, temp_product.ingreds)
            p.make_ingreds_list(ingreds)
            products[p.id] = p

        data_dict = {
            'path': abs_path, 'mtime': str(mtime), 'products': [],
            'ingreds': []}
        for p in products.values():
            p_dict = {'id': p.id, 'name': p.name, 'ingreds': p.ingreds}
            data_dict['products'].append(p_dict)
        for ingred in ingreds.values():
            i_dict = {'id': ingred.id, 'name': ingred.name}
            data_dict['ingreds'].append(i_dict)
        with open(SHAPED_FILE_NAME, 'w') as f:
            json.dump(data_dict, f, indent=2, ensure_ascii=False)
    else:
        with open(SHAPED_FILE_NAME, 'r') as f:
            shaped_file = json.load(f)
        i_dicts = shaped_file['ingreds']
        for i_dict in i_dicts:
            ingred = Ingred(i_dict['id'], i_dict['name'])
            ingreds[ingred.id] = ingred
        p_dicts = shaped_file['products']
        for p_dict in p_dicts:
            p = Product(p_dict['id'], p_dict['name'], p_dict['ingreds'])
            p.make_ingreds_list(ingreds)
            products[p.id] = p

    return products, ingreds


def count(products, ingreds, args):
    for ingred in ingreds.values():
        p_ids = [p.id for p in products.values() if ingred.id in p.ingreds]
        ingred.extend_products(p_ids)
        ingred.make_products_list(products)
    ingred_list = list(ingreds.values())
    sorted_ingreds = sorted(
        ingred_list, key=lambda ingred: len(ingred.products), reverse=True)

    table = get_formatted_table()
    table.set_cols_dtype(['i', 't', 'i', 't'])
    table.set_cols_align(['r', 'l', 'r', 'l'])
    table.add_row(['ID', 'Name', 'Num', 'Included'])
    for i, ingred in enumerate(sorted_ingreds):
        if args.num >= 0 and i >= args.num:
            break
        p_list = ingred.products_str
        if len(p_list) >= 30:
            p_list = '{}...'.format(p_list[:27])
        table.add_row([ingred.id, ingred.name, len(ingred.products), p_list])
    print(table.draw())


def show(products, ingreds, args):
    if args.type == 'ingredient' or args.type == 'i':
        if args.id is not None:
            ingred = ingreds.get(args.id, None)
            if ingred is None:
                print('id {:d} is not found'.format(args.id))
                return
            p_names = [
                p.name for p in products.values() if ingred.id in p.ingreds]
            p_names_str = ','.join(p_names)
            print('ID: {:d}'.format(ingred.id))
            print('name: {}'.format(ingred.name))
            print('included in: {}'.format(p_names_str))
            return
        table = get_formatted_table()
        table.set_cols_dtype(['i', 't'])
        table.set_cols_align(['r', 'l'])
        table.add_row(['ID', 'Name'])
        for i, ingred in enumerate(ingreds.values()):
            if args.num >= 0 and i >= args.num:
                break
            table.add_row([ingred.id, ingred.name])
        print(table.draw())
        return

    if args.type == 'product' or args.type == 'p':
        if args.id is not None:
            product = products.get(args.id, None)
            if product is None:
                print('id {:d} is not found'.format(args.id))
                return
            print('ID: {:d}'.format(product.id))
            print('name: {}'.format(product.name))
            print('ingredient: {}'.format(product.ingreds_str))
            return
        table = get_formatted_table()
        table.set_cols_dtype(['i', 't', 't'])
        table.set_cols_align(['r', 'l', 'l'])
        table.add_row(['ID', 'Name', 'Ingredients'])
        for i, p in enumerate(products.values()):
            if args.num >= 0 and i >= args.num:
                break
            ingred_list = p.ingreds_str
            if len(ingred_list) >= 30:
                ingred_list = '{}...'.format(ingred_list[:27])
            table.add_row([p.id, p.name, ingred_list])
        print(table.draw())


def main():
    parser = argparse.ArgumentParser(description='Count-up ingredient tool')
    parser.add_argument(
        '--data', default='data.txt', help='file path of dataset')
    parser.add_argument(
        '--num', '-n', type=int, default=-1, help='number of showing')
    subparsers = parser.add_subparsers()

    parser_count = subparsers.add_parser('count', help='Show ingredients')
    parser_count.set_defaults(handler=count)

    parser_list = subparsers.add_parser('list', help='Show all list')
    parser_list.add_argument(
        'type', choices=['i', 'ingredient', 'p', 'product'])
    parser_list.add_argument(
        '--id', '-i', type=int, default=None, help='id number')
    parser_list.set_defaults(handler=show)

    args = parser.parse_args()

    data = get_data(args.data)

    if hasattr(args, 'handler'):
        args.handler(*data, args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
