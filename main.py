import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import strategy as stg

#Number of rows to skip from the top (the older data)
toprow = int(input("Please specify the number of days from the past you would like to skip? "))
#read the data into a DataFrame
sp500_data = pd.read_csv('sp500.csv', index_col='Date', parse_dates=True, skiprows=[i for i in range(1,toprow+1)])

#print the last 5 rows in the DataFrame and its number of rows and columns
print(sp500_data.tail(), end='\n\n')

#plot the closing value of the index against date
plt.figure(figsize=(14,6))
plt.xlabel("Date")
plt.ylabel("S&P 500 Index")
sns.lineplot(data=sp500_data['Adj Close'], label='Adjusted Closing Value')
plt.savefig('plot.pdf', bbox_inches='tight')
#plt.show()

#Store the number of rows in the DataFrame
num_rows, _ = sp500_data.shape
print("Number of days in the index market: " + str(num_rows), end='\n\n')

#Starting value for the investment
init_dollars = [100, 600, 1100, 1600, 2100, 2600, 3100, 3600, 4100, 4600, 5100, 5600, 6100, 6600, 7100, 7600, 8100,\
    8600, 9100, 9600, 10100]
dollars = []
print()

#Dollar value assumed for trade
assumed_trade_units = 10.0
#The dollar value of the trade bin, which contains the dollars that are used for buying and selling
trade_dollars = []

tot_num_trades = []

#Store the adjusted closing value of the day in a list
adj_closing_val_list = sp500_data['Adj Close']

for i in init_dollars:
    val1, val2, val3 = stg.loc_min_max_stg(num_rows, i, adj_closing_val_list, assumed_trade_units)
    dollars.append(val1)
    trade_dollars.append(val2)
    tot_num_trades.append(val3)

#print("You started your investment with $" + str(init_dollars) + '.', end='\n\n')
#print("The trade bin from which you've made changes on your investment has a value of ${:.2f} in the index market.".format(
#    trade_dollars), end='\n\n')
#print("Your total amount of dollars (invested plus trade dollars) after the \
#current trading cycle is ${:.2f} and you traded {} times.".format(
#    dollars + trade_dollars, tot_num_trades)
#    , end='\n\n')
#print("Your total amount of dollars after the \
#current investment cycle would be ${:.2f} with no trading involved.".format(
#    init_dollars*(adj_closing_val_list[-1]/adj_closing_val_list[2]))
#    )
print(tot_num_trades)