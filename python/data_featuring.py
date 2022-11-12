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

def skipping_criteria(text_str):
    '''If below criteria meet, this text_str should be skipped'''
    text_str = text_str.replace('Tutorials and Guides', '').replace('Wallets Botnet logs', '')
    text_lower = text_str.lower()
    if 'guide' in text_lower or 'botnet' in text_lower:
        return True
    if not '$**' in text_str:
        return True

def skipping_pcs_criteria(line):
    '''Skip 0 pcs or more than 1 pcs and mix stuffs'''
    line = line.lower()
    regex_pcs = r'(\d+) pc'
    regex_pieces = r'(\d+) piece'

    # skip mix stuffs
    if ' mix ' in line:
        return True

    # skip 0 pcs or more than 1 pcs
    num_list = re.findall(regex_pcs, line)
    num_list.extend(re.findall(regex_pieces, line))
    for num in num_list:
        if num != '1':
            return True

    # for pcs in ['0', '2', '3', '4', '5', '6', '7', '8', '9']:
    #     for word in ['pcs', 'piece']:
    #         if pcs + word in line or pcs + ' ' + word in line:
    #             skip_this = True
    #             break
    return False

def get_category_from_title(prod_info):
    '''Return the type of product from its title'''
    prod_info = prod_info.lower()
    if any(x in prod_info for x in ['info', 'ssn', 'dob', 'dl']):
        return 'Personal Data'
    elif '.' in prod_info:
        return 'Online Account'
    elif 'email' in prod_info:
        return 'Email'
    elif 'credit card' in prod_info:
        return 'Credit card'
    elif 'bank' in prod_info:
        return 'Bank Account'
    elif 'passport' in prod_info:
        return 'Passport'
    elif 'bin' in prod_info:
        return 'Bank Identity Number'
    elif 'rdp' in prod_info:
        return 'Remote Desktop Protocol'
    else:
        return 'Other'

def get_dates_from_text(text_str):
    '''Last upload date of products from text_str'''
    date_list = []

    if '**10000000$**' in text_str:
        return date_list

    regex = r'(\d{4}-\d{2}-\d{2})'
    lines = text_str.split('\n')
    for i,line in enumerate(lines):
        line = line.lower()
        if line.startswith('dob') or '**0$**' in line: # Skip date of birth info of victims
            continue

        if skipping_pcs_criteria(line):
            # print(line)
            continue

        if skipping_pcs_criteria(lines[i-1]) or skipping_pcs_criteria(lines[i-2]):
            # print(lines[i-1])
            continue

        for date in re.findall(regex, line):
            if date.startswith('2021') or date.startswith('2022'):
                date_list.append(date)
        
    return date_list

def get_prices_from_text(text_str):
    ''' All USD prices from the text_str'''
    number_list = []
    # Search prices
    # change the regex from its origin to fit case 5622185.json in
    # which the line containing price does not have whitespace at the end
    # or at the begining. Moreover, the regex now covers the cases of
    # float number of prives, e.g 1.5 USD
    regex = r'\*\*(\d+\.*\d*)\$\*\*'
    lines = text_str.split('\n')
    for i,line in enumerate(lines):
        line = line.lower()
        if not '**' in line or not '$' in line:
            continue

        # Skip 0 pcs or more than 1 pcs and mix stuffs
        if (skipping_pcs_criteria(line) or skipping_pcs_criteria(lines[i-1])
            or skipping_pcs_criteria(lines[i-2])):
            continue

        for number in re.findall(regex, line):
            number = float(number)
            if 0 < number < 1000000: # More than zero and less than million
                number_list.append(number)
    # number_list.sort()
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
    if skipping_criteria(text_str):
        return None
    title = get_title_from_text(text_str)
    seller = get_seller_from_text(text_str)
    prices_list = get_prices_from_text(text_str)
    dates_list = get_dates_from_text(text_str)
    assert len(dates_list) == len(prices_list), f'{json_id}: dates:{len(dates_list)}\nprices:{len(prices_list)}'
    category = get_category_from_title(title)

    # save features into a dictionary
    feature_dict = {'id': json_id.split('.')[0], 'time-stamp': json_data['timestamp'], 'category': category,
                    'seller': seller, 'product': title, 'prices': prices_list, 'dates': dates_list}
    return feature_dict

def save_into_json(file_path, json_list):
    with open(file_path, 'w', encoding='utf-8') as fp:
        for product_page in json_list:
            fp.write(json.dumps(product_page))
            fp.write('\n')

def test():
    file_test = '../database/1508.json'
    json_data = read_json_file(file_test)
    # dates = get_dates_from_text(json_data['text'])
    prices = get_prices_from_text(json_data['text'])
    # for i,date in enumerate(dates):
    #     print(f'{i+1}: {date}')

def create_master_file():
    full_features_list = []
    for json_file in FILE_LIST:
        if json_file in SKIP_LIST:
            continue
        # json_file = '../database/5622185.json'
        feature_dict = extract_features(json_file)
        if feature_dict == None:
            continue
        full_features_list.append(feature_dict)
    save_into_json('../analysis_result/product_pages.json',full_features_list)

def main():
    create_master_file()
    # test()

if __name__ == '__main__':
    main()
