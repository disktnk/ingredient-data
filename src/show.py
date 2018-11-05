import argparse

import pandas
import texttable

from src.data import get_data


def get_formatted_table():
    table = texttable.Texttable()
    table.set_deco(texttable.Texttable.HEADER)
    return table


def count_include_in(products, ingreds):
    for ingred in ingreds.values():
        p_ids = [p.id for p in products.values() if ingred.id in p.ingreds]
        ingred.extend_products(p_ids)
        ingred.make_product_names(products)
    ingred_list = list(ingreds.values())
    return sorted(
        ingred_list, key=lambda ingred: len(ingred.products), reverse=True)


def count(products, ingreds, args):
    sorted_ingreds = count_include_in(products, ingreds)

    table = get_formatted_table()
    table.set_cols_dtype(['i', 't', 'i', 't'])
    table.set_cols_align(['r', 'l', 'r', 'l'])
    table.add_row(['ID', 'Name', 'Num', 'Included'])
    for i, ingred in enumerate(sorted_ingreds):
        if args.num >= 0 and i >= args.num:
            break
        p_list = ','.join(ingred.product_names)
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
            print('ingredient: {}'.format(','.join(product.ingred_names)))
            return
        table = get_formatted_table()
        table.set_cols_dtype(['i', 't', 't'])
        table.set_cols_align(['r', 'l', 'l'])
        table.add_row(['ID', 'Name', 'Ingredients'])
        for i, p in enumerate(products.values()):
            if args.num >= 0 and i >= args.num:
                break
            ingred_list = ','.join(p.ingred_names)
            if len(ingred_list) >= 30:
                ingred_list = '{}...'.format(ingred_list[:27])
            table.add_row([p.id, p.name, ingred_list])
        print(table.draw())


def save_excel(products, ingreds, args):
    sorted_ingreds = count_include_in(products, ingreds)

    df = pandas.DataFrame(columns=['Name', 'Num', 'Included'])
    for ingred in sorted_ingreds:
        df.loc[ingred.id] = [ingred.name, len(ingred.products),
                             ingred.product_names]

    df.to_excel(args.out, sheet_name='count')


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

    parser_excel = subparsers.add_parser(
        'excel', help='Save summary and master as excel')
    parser_excel.add_argument(
        '--out', '-o', default='summary.xlsx', help='output file name')
    parser_excel.set_defaults(handler=save_excel)

    args = parser.parse_args()

    data = get_data(args.data)

    if hasattr(args, 'handler'):
        args.handler(*data, args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
