'''Do some statistics such as max, min, average, median'''

import json
import numpy as np
from collections import Counter

JSON_FILE = 'master.json'

def read_json_file(file_path):
    json_data = []
    with open(file_path, encoding='utf-8') as fp:
        for line in fp:
            json_dict = json.loads(line)
            json_data.append(json_dict)
    return json_data

def get_top_seller(json_data, n=5):
    '''Return sellers selling the top greatest amount of products'''
    seller_list = Counter() # key as seller, value as number of products
    for entry in json_data:
        seller = entry['seller']
        num_of_prods = len(entry['prices'])
        
        seller_list[seller] += num_of_prods

    return seller_list.most_common(n)

def get_average_by_seller(json_data, seller):
    '''Return the average price of products which are sold by the given seller'''
    seller_exist = False
    aggregated_sum = 0
    num_of_prods = 0
    for entry in json_data:
        if entry['seller'] == seller:
            seller_exist = True
            aggregated_sum += np.sum(np.array(entry['prices']))
            num_of_prods += len(entry['prices'])
    if not seller_exist:
        return None
    return float(aggregated_sum / num_of_prods)

def get_median_by_seller(json_data, seller):
    '''Return the median price of products which are sold by the given seller'''
    seller_exist = False
    prices = []
    for entry in json_data:
        if entry['seller'] == seller:
            seller_exist = True
            prices.extend(entry['prices'])
    if not seller_exist:
        return None
    return np.median(np.array(prices))

def data_set_statistic(json_data):
    '''Return total products, max, min, average, median price, total seller'''
    prices = []
    sellers = set()
    for entry in json_data:
        prices.extend(entry['prices'])
        sellers.add(entry['seller'])

    prices_np = np.array(prices)
    total_products = len(prices)
    max_price = np.max(prices_np)
    min_price = np.min(prices_np)
    avg_price = np.average(prices_np)
    median_price = np.median(prices_np)
    total_seller = len(sellers)

    return [total_products, max_price, min_price, avg_price, median_price, total_seller]

def main():
    json_data = read_json_file(JSON_FILE)
    # top_seller = get_top_seller(json_data)
    # print(top_seller)

    total_products, max_price, min_price, avg_price, median_price, total_seller = data_set_statistic(json_data)
    print(f'Total number of products: {total_products}')
    print(f'Maximum price: {max_price} USD')
    print(f'Minimum price: {min_price} USD')
    print(f'Average price: {avg_price:.2f} USD')
    print(f'Median price: {median_price} USD')
    print(f'Total number of sellers: {total_seller}')
    print(f'Total number of urls inspected: {len(json_data)}')

if __name__ == '__main__':
    main()
        