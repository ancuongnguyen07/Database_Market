import json
import re, os
from glob import glob

"""
These functions below are inspired by Juha Nurmi's script in
https://mega.nz/folder/aJwVyIYJ#9SWh-Z3-TpPfjHZeFxbeew
(example_price.py)
"""

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

# Collect all JSON file names
FILE_LIST = glob('../database/*.json')

# hash tags for detecting the potential title of products
TITLE_DETECT = '######'

# hash tags for detecting the potential seller name
SELLER_DETECT = '###'

def read_json_file(file_path):
    with open(file_path, encoding='utf-8') as fp:
        file_content = json.load(fp)
    return file_content

def get_title_from_text(text):
    lines_text = text.split('\n')
    for line in lines_text:
        if line.startswith(TITLE_DETECT) and not ('Main' in line
            or 'Product Information' in line):
            return line.lstrip(f'{TITLE_DETECT}').strip()
    return 'No title'

def get_seller_from_text(text):
    lines_text = text.split('\n')
    for line in lines_text:
        if line.startswith(f'{SELLER_DETECT} '):
            return line.lstrip(f'{SELLER_DETECT}').strip()
    return 'No seller'

def get_prices_from_text(text_str):
    ''' All USD prices from the text_str to a sorted integer list '''
    number_list = []
    text_str = text_str.replace('Tutorials and Guides', '').replace('Wallets Botnet logs', '')
    text_lower = text_str.lower()
    if 'guide' in text_lower or 'botnet' in text_lower:
        return number_list
    if not '$**' in text_str:
        return number_list
    # Search prices
    # change the regex from its origin to fit case 5622185.json in
    # which the line containing price does not have whitespace at the end
    # or at the begining. Moreover, the regex now covers the cases of
    # float number of prives, e.g 1.5 USD
    regex = r'\s*\*\*\d+\.*\d*\$\*\*\s*'
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
            number = float(number.strip().strip('**').rstrip('$'))
            if 0 < number < 1000000: # More than zero and less than million
                number_list.append(number)
    number_list.sort()
    return number_list

# def collect_prices(inputfile):
#     ''' Collect all prices from the input file '''
#     assert os.path.isfile(inputfile)
#     item = read_json_file(inputfile)
#     assert item
#     text = item.get('text', '')
#     assert len(text) > 100
#     title = get_title_from_text(text)
#     for word in ['guide', 'tutorial', 'package', 'bulk']:
#         if word in title.lower():
#             return []
#     price_list = get_prices_from_text(text)
#     if len(price_list) < 1:
#         return []
#     print('Input file: %s' % inputfile)
#     # print('Url: /%s' % '/'.join(item['url'].split('/')[-2:]))
#     print('Title: %s' % title)
#     print('Products: %d' % len(price_list))
#     average = np.average(price_list)
#     print('Average: %.1f USD' % average)
#     median = np.median(price_list)
#     print('Median: %.1f USD' % median)
#     return price_list

def extract_features(json_file):
    '''Collects fields including json_id, seller, prices, products
    and store them into a dictionary'''
    assert os.path.isfile(json_file)
    json_data = read_json_file(json_file)
    assert json_data
    json_id = json_file.split('/')[-1]
    text_str = json_data['text']
    assert len(text_str) > 100
    title = get_title_from_text(text_str)
    seller = get_seller_from_text(text_str)
    prices_list = get_prices_from_text(text_str)

    # save features into a dictionary
    feature_dict = {'id': json_id.split('.')[0], 'time-stamp': json_data['timestamp'], 'seller': seller,
                    'product': title, 'prices': prices_list}
    return feature_dict

def save_into_json(file_path, json_list):
    with open(file_path, 'w', encoding='utf-8') as fp:
        for product_page in json_list:
            fp.write(json.dumps(product_page))
            fp.write('\n')

def main():
    full_features_list = []
    for json_file in FILE_LIST:
        if json_file in SKIP_LIST:
            continue
        # json_file = '../database/5622185.json'
        feature_dict = extract_features(json_file)
        full_features_list.append(feature_dict)
    save_into_json('master.json',full_features_list)

if __name__ == '__main__':
    main()
