''' Collect price data from selected JSON files '''
import os
import re
import json
from glob import glob

# These items are datadump collections, skip them
SKIP_LIST = [
    '../database/1354.json',
    '../database/984.json',
    '../database/768.json',
    '../database/977.json',
    '../database/617.json',
    '../database/977.json',
    '../database/617.json',
    '../database/977.json',
    '../database/1286.json',
    '../database/1543.json',
    '../database/482.json'
]

# Use this FILE_LIST as a test list to understand how it extracts prices
FILE_LIST = {
    'Fly_Credits': [1110], # ./database/1110.json
    'Online_Banking': [1536],
    'Online_Casino': [1565],
    'Credit_Cards': [1112],
    'Cryptocurrency_Markets': [825],
    'Email_Services': [767],
    'Food': [1128],
    'Hotels': [1230],
    'Insurance': [780],
    'Entertaiment': [1186],
    'Social_Networks': [445],
    'Shopping': [1573]
}

# Reads all JSON files
FILE_LIST = {
    'Test': glob('../database/*.json')
}

def read_json(filename):
    ''' Read JSON file '''
    json_data = {}
    with open(filename, 'r', encoding='utf-8') as myfile:
        json_data = json.load(myfile)
    return json_data

def prices_from_text(text_str):
    ''' All USD prices from the text_str to a sorted integer list '''
    number_list = []
    text_str = text_str.replace('Tutorials and Guides', '').replace('Wallets Botnet logs', '')
    text_lower = text_str.lower()
    if 'guide' in text_lower or 'botnet' in text_lower:
        return number_list
    if not '$**' in text_str:
        return number_list
    # Search prices
    regex = r'\s\*\*\d+\$\*\*\s'
    for line in text_str.split('\n'):
        line = line.lower()
        if not '**' in line or not '$' in line:
            continue
        if 'mix' in line: # Skip mixed data packages
            continue
        # Skip 0 pcs or more than 1 pcs
        skip_this = False
        for pcs in ['0', '2', '3', '4', '5', '6', '7', '8', '9']:
            for word in ['pcs', 'piece']:
                if pcs + word in line or pcs + ' ' + word in line:
                    skip_this = True
                    break
        if skip_this:
            continue
        for number in re.findall(regex, line):
            number = float(number.replace('*', '').replace('$', '').strip())
            if 0 < number < 1000000: # More than zero and less than million
                print('Example line %d: %s' % (len(number_list) + 1, line.strip()))
                number_list.append(number)
    number_list.sort()
    return number_list

def get_title_from_text(text_str):
    ''' Get the title text '''
    if not '######' in text_str:
        return ''
    for line in text_str.split('\n'):
        if not '######' in line:
            continue
        title = line.replace('#', '').strip()
        if ' Main ' in title:
            continue
        if title:
            return title
    return ''

def collect_prices(inputfile):
    ''' Collect all prices from the input file '''
    assert os.path.isfile(inputfile)
    item = read_json(inputfile)
    assert item
    text = item.get('text', '')
    assert len(text) > 100
    title = get_title_from_text(text)
    if 'guide' in title.lower() or 'tutorial' in title.lower():
        return []
    if 'package' in title.lower() or 'bulk' in title.lower():
        return []
    price_list = prices_from_text(text)
    if len(price_list) < 1:
        return []
    print('Input file: %s' % inputfile)
    print('Url: /%s' % '/'.join(item['url'].split('/')[-2:]))
    print('Title: %s' % title)
    print('Products: %d' % len(price_list))
    average = float(sum(price_list)) / len(price_list)
    print('Average: %.1f USD' % average)
    median = price_list[int(len(price_list) / 2)]
    print('Median: %.1f USD' % median)
    print('')
    return price_list

product_pages_used = 0
prices = []

for key, value_list in FILE_LIST.items():
    print(key.replace('_', ' ').upper())
    for value in value_list:
        if str(value) in SKIP_LIST:
            continue
        if 'database' in str(value):
            new_prices = collect_prices(value)
            if new_prices:
                prices.extend(new_prices)
                product_pages_used = product_pages_used + 1
        else:
            new_prices = collect_prices('database/%d.json' % value)
            if new_prices:
                prices.extend(new_prices)
                product_pages_used = product_pages_used + 1

prices.sort()
total = len(prices)

price_json = {}
for price in prices:
    price_json[price] = price_json.get(price, 0) + 1

print('USD, COUNT, PERCENT')
for usd, value in price_json.items():
    print('%d, %.1f, %f' % (usd, value, float(value)/total * 100))

average = float(sum(prices)) / total
median = prices[int(total / 2)]
print('\nUsed %d product pages' % product_pages_used)
print('Total Products: %d' % total)
print('Min: %.1f USD, Max: %.1f USD' % (prices[0], prices[-1]))
print('Average: %.1f USD, Median: %.1f USD\n' % (average, median))
