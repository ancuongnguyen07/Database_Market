'''Do some statistics such as max, min, average, median'''

import json
import numpy as np
from collections import Counter

JSON_FILE = 'master_2.json'

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

def price_histogram(json_data):
    '''
    explore popular prices in the whole dataset
    return a dictionary with a following format:
    key: 'price', value: 'its frequency'
    Example: {2.0: 3, 4.3: 10}
    '''
    price_counter = Counter()

    for line in json_data:
        for p in line['prices']:
            price_counter[float(p)] += 1
    
    return price_counter

def get_month_from_date(date_string):
    '''return integer form of month from a date string
    date string format: yyyy-mm-dd'''
    year,month,day = date_string.split('-')
    return '-'.join([month,year[-2:]])

def average_per_month(json_data):
    '''
    Explore the average price of each month
    return a dictionary with the following format:
    key: <month>, value: <avg_price>
    '''
    avg_price_dist = {}
    for entry in json_data:
        for price,date in zip(entry['prices'],entry['dates']):
            month = get_month_from_date(date)
            if month not in avg_price_dist:
                avg_price_dist[month] = [price]
            else:
                avg_price_dist[month].append(price)

    for month in avg_price_dist:
        avg_price_dist[month] = np.average(np.array(avg_price_dist[month]))

    # sort in time ascending order
    # example: 09-21, 10-21, 11-21,...,7-22
    sorted_items = list(sorted(avg_price_dist.items(), key=lambda x:(x[0].split('-')[1],
                        x[0].split('-')[0])))

    return sorted_items

def median_per_month(json_data):
    '''
    Explore the median price of each month
    return a dictionary with the following format:
    key: <month>, value: <median_price>
    '''
    med_price_dist = {}
    for entry in json_data:
        for price,date in zip(entry['prices'],entry['dates']):
            month = get_month_from_date(date)
            if month not in med_price_dist:
                med_price_dist[month] = [price]
            else:
                med_price_dist[month].append(price)

    for month in med_price_dist:
        med_price_dist[month] = np.median(np.array(med_price_dist[month]))

    # sort in time ascending order
    # example: 09-21, 10-21, 11-21,...,7-22
    sorted_items = list(sorted(med_price_dist.items(), key=lambda x:(x[0].split('-')[1],
                        x[0].split('-')[0])))

    return sorted_items

def main():
    # json_data = read_json_file(JSON_FILE)
    # top_seller = get_top_seller(json_data)
    # print(top_seller)
    pass


if __name__ == '__main__':
    main()
        