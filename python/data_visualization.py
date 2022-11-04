import matplotlib.pyplot as plt
import data_analysis as da

MASTER_JSON_PATH = 'master_2.json'

def plot_price_histogram():
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

def main():
    # plot_price_histogram()
    # plot_med_price_timeseries()
    pass

if __name__ == '__main__':
    main()