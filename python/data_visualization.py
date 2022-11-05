import matplotlib.pyplot as plt
import data_analysis as da
import numpy as np

MASTER_JSON_PATH = 'master_2.json'

def plot_price_histogram():
    '''Plot the occurence of each products' price in the whole dataset'''
    json_data = da.read_json_file(MASTER_JSON_PATH)
    price_histogram = da.price_histogram(json_data)

    # plotting
    plt.figure()
    plt.bar(list(price_histogram.keys()), list(price_histogram.values()))
    plt.title('Histogram of prices')
    plt.xlabel('Price (USD)')
    plt.ylabel('Frequency')
    plt.xscale('log')

    plt.show()

def plot_avg_price_timeseries():
    '''
    Plot distribution of average price over months from
    9-2021 to 6-2022
    '''
    json_data = da.read_json_file(MASTER_JSON_PATH)
    avg_price_month_dist = da.average_per_month(json_data)

    # plotting
    plt.figure()
    plt.plot([tup[0] for tup in avg_price_month_dist],[tup[1] for tup in avg_price_month_dist])
    plt.title('Average price per month')
    plt.ylabel('Average price (USD)')
    plt.xlabel('Month')
    plt.xticks(rotation=45, ha='right')

    plt.show()

def plot_med_price_timeseries():
    '''
    Plot distribution of median price over months from
    9-2021 to 6-2022
    '''
    json_data = da.read_json_file(MASTER_JSON_PATH)
    med_price_month_dist = da.median_per_month(json_data)

    # plotting
    plt.figure()
    plt.plot([tup[0] for tup in med_price_month_dist],[tup[1] for tup in med_price_month_dist])
    plt.title('Median price per month')
    plt.ylabel('Median price (USD)')
    plt.xlabel('Month')
    plt.xticks(rotation=45, ha='right')

    plt.show()

def plot_category_allocation():
    json_data = da.read_json_file(MASTER_JSON_PATH)
    category_stat = da.extract_type_of_product(json_data)

    total_prods = sum(category_stat.values())
    list_of_categories = list(category_stat.keys())
    list_of_counts = list(category_stat.values())
    list_of_allocation = np.array(list_of_counts) / total_prods

    # set up colors
    cmap = plt.get_cmap('tab20')
    my_colors = [cmap(i) for i in np.linspace(0,1,len(list_of_categories))]

    # plotting
    plt.figure()
    plt.pie(list_of_allocation,autopct='%1.2f%%',colors=my_colors)
    plt.legend(list_of_categories)
    plt.show()

def main():
    # plot_price_histogram()
    # plot_med_price_timeseries()
    plot_category_allocation()
    # pass

if __name__ == '__main__':
    main()