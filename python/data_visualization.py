import matplotlib.pyplot as plt
import data_analysis as da
import numpy as np

MASTER_JSON_PATH = '../analysis_result/product_pages.json'
CATEGORY_STAT_PATH = '../analysis_result/category_stat.csv'

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
    list_of_counts = [tup[1] for tup in category_stat]

    total_prods = sum(list_of_counts)
    list_of_categories = [tup[0] for tup in category_stat]
    list_of_allocation = np.array(list_of_counts) / total_prods

    # set up colors
    cmap = plt.get_cmap('tab20')
    my_colors = [cmap(i) for i in np.linspace(0,1,len(list_of_categories))]

    # plotting
    plt.figure()
    plt.pie(list_of_allocation,autopct='%1.2f%%',colors=my_colors)
    plt.legend(list_of_categories)
    plt.show()

def plot_cumprob_price():
    '''Plot the cumulative frequency of each price in the ascending
    range of prices'''

    json_data = da.read_json_file(MASTER_JSON_PATH)
    cumfreq_price = da.cumulative_price_distribution(json_data)

    plt.figure()
    plt.plot([x[0] for x in cumfreq_price],[x[1] for x in cumfreq_price],'r-')
    plt.xlabel('Price (USD)')
    plt.ylabel('Cumulative probability (%)')
    plt.yticks(np.arange(0,110,10))
    plt.xticks(np.arange(0,55,5))
    plt.show()

def tuplelize_category_stat(file_path):
    '''Retrieve stat from the CSV file to a list of tuples
    (<category>,<amount_of_products>,<avg_price>)'''

    stats_tuples = []
    with open(file_path, 'r', encoding='utf-8') as fp:
        lines = fp.read().strip().split('\n')
        for i in range(1,len(lines)):
            stats_tuples.append(lines[i].split(','))
    return stats_tuples

def plot_category_stat():
    '''Plot the statistical result in terms of product category.
    On the left y-axis, it illustartes the number of products.
    On the right y-axis, it shows the average price'''

    stat_result = tuplelize_category_stat(CATEGORY_STAT_PATH)
    list_of_category = [tup[0] for tup in stat_result]
    list_of_num_prods = list(map(int,[tup[1] for tup in stat_result]))
    list_of_avg_price = list(map(float,[tup[2] for tup in stat_result]))
    list_of_category = ['\n'.join(x.split()) for x in list_of_category]

    # plotting
    fig,ax = plt.subplots()
    X_axis = np.arange(len(list_of_category))

    # plot number of prods
    ax.bar(X_axis - 0.2, list_of_num_prods, width=0.4 ,color='red')
    ax.set_xlabel('Product type')
    ax.set_ylabel('Amount of items', color='red')
    ax.set_ylim(ymin=0)
    ax.set_yticks(np.arange(0,44000,4000))
    ax.set_xticks(X_axis, list_of_category)

    # plot average price
    ax2 = ax.twinx()
    ax2.bar(X_axis + 0.2, list_of_avg_price, width=0.4,color='blue')
    ax2.set_ylabel('Average price (USD)', color='blue')
    # ax2.set_yticks(np.arange(0,130,10))

    plt.show()

def plot_top_average_price_seller():
    json_data = da.read_json_file(MASTER_JSON_PATH)
    # Top 10
    avg_price_index = 5
    top_avg_price_sellers = da.top_field_seller(json_data, avg_price_index)

    # plotting
    plt.figure()
    plt.bar([tup[0] for tup in top_avg_price_sellers],
        [tup[avg_price_index] for tup in top_avg_price_sellers])
    plt.ylabel('Average price (USD)')
    plt.xlabel('Store')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(np.arange(0,550,50))
    plt.show()

def plot_top_num_prods_seller():
    json_data = da.read_json_file(MASTER_JSON_PATH)
    # Top 10
    num_prods_index = 1
    top_num_prods_sellers = da.top_field_seller(json_data, num_prods_index)

    avg_price_index = 5
    top_avg_price_sellers = da.top_field_seller(json_data, avg_price_index)

    # plotting
    fig,(ax1, ax2) = plt.subplots(2)
    
    # plot average price bar chart
    labels1 = np.arange(len([tup[0] for tup in top_avg_price_sellers]))
    ax1.bar(labels1 - 0.2,
        [tup[avg_price_index] for tup in top_avg_price_sellers], width=0.4)
    ax1.set_ylabel('Average price (USD)', color='blue')
    ax1.set_xlabel('Store')
    ax1.set_xticks(labels1,[tup[0] for tup in top_avg_price_sellers])
    # ax1.set_xticklabels(labels1)
    ax1.set_yticks(np.arange(0,525,25))
    ax1.set_title('Top 10 stores according to the average price')

    # second y-axis for num of products
    ax1_prime = ax1.twinx()
    ax1_prime.bar(labels1 + 0.2, [tup[num_prods_index] for tup in top_avg_price_sellers]
        , width=0.4 ,color='red')
    ax1_prime.set_ylabel('Number of products', color='red')
    ax1_prime.set_yticks(np.arange(0,13000,1000))

    # plot num of prods bar chart
    labels2 = np.arange(len([tup[0] for tup in top_num_prods_sellers]))
    ax2.bar(labels2 - 0.2,
        [tup[avg_price_index] for tup in top_num_prods_sellers], width=0.4, color='blue')
    ax2.set_ylabel('Average price (USD)', color='blue')
    ax2.set_xlabel('Store')
    ax2.set_xticks(labels2, [tup[0] for tup in top_num_prods_sellers])
    # ax2.set_xticklabels(labels2)
    ax2.set_title('Top 10 stores according to the total number of sold items')
    ax2.set_yticks(np.arange(0,525,25))
    

    # second y-axis for average price
    ax2_prime = ax2.twinx()
    ax2_prime.bar(labels2 + 0.2, [tup[num_prods_index] for tup in top_num_prods_sellers],
        width=0.4 ,color='red')
    ax2_prime.set_ylabel('Number of products', color='red')
    ax2_prime.set_yticks(np.arange(0,13000,1000))

    plt.show()

def main():
    # plot_price_histogram()
    # plot_med_price_timeseries()
    # plot_category_allocation()
    # plot_cumprob_price()
    # plot_category_stat()
    # plot_top_average_price_seller()
    plot_top_num_prods_seller()
    # pass

if __name__ == '__main__':
    main()