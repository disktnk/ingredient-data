import codecs
import datetime
import json
import os
import re

import zenhan

from src.domain import Ingred
from src.domain import Product


SHAPED_FILE_NAME = 'data.json'


def regularization(name):
    return zenhan.z2h(zenhan.h2z(name, mode=4), mode=3)


def get_data(path):
    need_reload = False
    abs_path = os.path.abspath(path)
    if not os.path.exists(abs_path):
        raise ValueError('not found data.txt, please put the file')
    mtime = datetime.datetime.fromtimestamp(
        os.path.getmtime(abs_path)).isoformat()
    if os.path.exists(SHAPED_FILE_NAME):
        with codecs.open(SHAPED_FILE_NAME, 'r', 'utf-8') as f:
            shaped_file = json.load(f)
        if shaped_file['path'] != abs_path:
            need_reload = True
        if shaped_file['mtime'] != mtime:
            need_reload = True
    else:
        need_reload = True

    products, ingreds = {}, {}
    if need_reload:
        with codecs.open(abs_path, 'r', 'utf-8') as f:
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
        with codecs.open(SHAPED_FILE_NAME, 'w', 'utf-8') as f:
            json.dump(data_dict, f, indent=2, ensure_ascii=False)
    else:
        with codecs.open(SHAPED_FILE_NAME, 'r', 'utf-8') as f:
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
