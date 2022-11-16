'''Do some statistics such as max, min, average, median'''

import json
import numpy as np
from collections import Counter
import re, requests

JSON_FILE = '../analysis_result/product_pages.json'

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

def seller_analysis(json_data):
    '''return a list of tuples containing (seller,num_of_prods,min,max,avg,median)'''
    seller_dict = {}
    category_dict = {}
    # retrieving seller and his/her prices of products
    for entry in json_data:
        seller = entry['seller']

        if seller not in seller_dict:
            seller_dict[seller] = []
            category_dict[seller] = set()

        seller_dict[seller].extend(entry['prices'])
        category_dict[seller].add(entry['category'])

    seller_stat = []
    for seller in seller_dict.keys():
        list_of_prods = seller_dict[seller]
        num_of_prods = len(list_of_prods)
        min_price = min(list_of_prods)
        max_price = max(list_of_prods)
        # round the avg_price with 2 decimal places
        avg_price = np.around(np.average(np.array(list_of_prods)),2)
        median_price = np.median(np.array(list_of_prods))
        category_range = len(category_dict[seller])

        seller_stat.append((seller,num_of_prods,category_range,min_price,max_price,
                            avg_price,median_price))

    return seller_stat

def save_seller_stat(stats):
    '''save the seller stat into a CSV file'''
    with open('../analysis_result/seller_stat.csv', 'w') as fp:
        fp.write('Seller,Number of products,Range of product type,Minimum price,Maximum price,Average price,Median price\n')
        for entry in stats:
            stat_string = ','.join(list(map(str,entry)))
            fp.write(f'{stat_string}\n')

def dataset_statistic(json_data):
    '''Return total products, max, min, average, median price, total seller'''
    prices = []
    sellers = set()
    for entry in json_data:
        prices.extend(entry['prices'])
        sellers.add(entry['seller'])

    prices_np = np.array(prices)
    total_items = len(prices)
    max_price = np.max(prices_np)
    min_price = np.min(prices_np)
    avg_price = np.average(prices_np)
    median_price = np.median(prices_np)
    total_seller = len(sellers)

    return [total_items, max_price, min_price, avg_price, median_price, total_seller]

def save_dataset_stats(key_findings):
    '''Save numerical results from the whole dataset statistic to a .txt file'''
    total_items, max_price, min_price, avg_price, median_price, total_seller = key_findings

    with open('../analysis_result/dataset_stats.txt', 'w', encoding='utf-8') as fp:
        fp.write(f'Total number of items: {total_items}\n')
        fp.write(f'Maximum price: {max_price:.2f} USD\n')
        fp.write(f'Minimum price: {min_price:.2f} USD\n')
        fp.write(f'Average price: {avg_price:.2f} USD\n')
        fp.write(f'Median price: {median_price:.2f} USD\n')
        fp.write(f'Total number of sellers: {total_seller}')

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

def extract_type_of_product(json_data):
    '''return a stat of each type of product
    append price of each item belonging to a given type'''
    category_count = {}
    for entry in json_data:
        category = entry['category']
        
        if category not in category_count:
            category_count[category] = entry['prices']
        else:
            category_count[category].extend(entry['prices'])

    return [(category,len(price_list),np.mean(np.array(price_list))) for category,price_list 
            in category_count.items()]

def save_category_statistic(category_stat):
    '''Save the sorted statistic of category into a CSV file'''
    # sort by the num_of_prods of each category in decending order
    sorted_stat = list(sorted(category_stat, key=lambda x:x[1], reverse=True))

    with open('../analysis_result/category_stat.csv', 'w') as fp:
        fp.write('Category,Number of products,Average price\n')
        for category,counter,avg_price in sorted_stat:
            fp.write(f'{category},{counter},{avg_price:.2f}\n')

def cumulative_price_distribution(json_data):
    '''Return a list of tuple having format:
    (x,y) where x is a price, y is the cumulative probability of the price'''
    price_counter = price_histogram(json_data)
    sorted_price_dist = list(sorted(price_counter.items(), key=lambda x:x[0]))

    list_of_count = np.array([x[1] for x in sorted_price_dist])
    list_of_price = np.array([x[0] for x in sorted_price_dist])
    cumsum_price = np.cumsum(list_of_count)
    cumsum_price = cumsum_price / np.sum(list_of_count) * 100

    return [(x,y) for x,y in zip(list_of_price, cumsum_price) if x <= 50]

def extract_website(json_data):
    '''Extract compromised website from title of products'''
    webs = set()
    for entry in json_data:
        title = entry['product']
        regex = r'([a-zA-Z]+)\.([a-z]+)'
        webs.update(['.'.join(x) for x in re.findall(regex,title)])

    return webs

# def validate_websites(web_list):
#     valid_websites = []
#     headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0'}
#     for web in web_list:
#         print(web)
#         try:
#             response = requests.head(f'https://www.{web.lower()}', headers=headers, timeout=5)
#             print(response.status_code)
#             if response.status_code == 200:
#                 valid_websites.append(web)
#         except requests.exceptions.ConnectionError as e:
#             print('no response')
#             continue
#         except requests.exceptions.ReadTimeout as e:
#             print('Timeout')
#             continue
#     return valid_websites

def save_leaked_websites(web_list):
    with open('../analysis_result/leaked_websites.txt', 'w') as fp:
        for web in web_list:
            fp.write(f'{web}\n')

def leads_over_email(json_data):
    '''Explore allocation of leads email over all general compromised email'''
    leads = []
    emails = 0
    for entry in json_data:
        if entry['category'] == 'Email':
            list_of_prices = entry['prices']
            emails += len(list_of_prices)
            if 'lead' in entry['product'].lower():
                leads.extend(list_of_prices)
    return len(leads), len(leads) / emails, np.mean(leads)

def generate_leads_email_stat(json_data):
    leads, leads_prob, avg_price = leads_over_email(json_data)
    print(f'Number of lead emails: {leads}')
    print(f'Probability of genearl emails: {leads_prob*100}')
    print(f'Average price of leads: {avg_price:.2f} USD')

def top_field_seller(json_data, field, n=10):
    '''return top n seller according to the given field in descending order.
    The given field here means the index of a tuple (seller,num_of_prods,min,max,avg,median)
    '''
    seller_stat = seller_analysis(json_data)
    assert field < len(seller_stat[0]) and field >= 0, 'invalid index of seller_stat'
    sorted_stat = list(sorted(seller_stat, key=lambda x:x[field], reverse=True))

    return sorted_stat[:n]

def main():
    json_data = read_json_file(JSON_FILE)
    # top_seller = get_top_seller(json_data)
    # print(top_seller)
    # pass

    # seller_stat = seller_analysis(json_data)
    # save_seller_stat(seller_stat)
    # save_category_statistic(extract_type_of_product(json_data))
    # save_dataset_stats(dataset_statistic(json_data))

    # save_leaked_websites(extract_website(json_data))

    # generate_leads_email_stat(json_data)

if __name__ == '__main__':
    main()
        