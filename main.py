import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import strategy as stg

#Number of rows to skip from the top (the older data)
prior_days = int(input("Please specify the number of days from the past you would like to skip? "))
#read the data into a DataFrame
skip_list = [i for i in range(1,prior_days+1)] #number of rows (days) to skip from the past in the data
sp500_data = pd.read_csv('sp500.csv', index_col='Date', parse_dates=True, skiprows=skip_list)

#print the last 5 rows in the DataFrame and its number of rows and columns
print(sp500_data.tail(), end='\n\n')

#plot the closing value of the index against date
f1 = plt.figure(figsize=(14,6))
plt.xlabel("Date")
plt.ylabel("S&P 500 Index")
sns.lineplot(data=sp500_data['Adj Close'], label='Adjusted Closing Value')
f1.savefig('index_plot.pdf', bbox_inches='tight')
#plt.show()

#Store the number of rows in the DataFrame
num_rows, _ = sp500_data.shape
print("Number of days in the index market: " + str(num_rows), end='\n\n')

#Starting value for the investment
init_dollars = [100.00, 600.00, 1100.00, 1600.00, 2100.00, 2600.00, 3100.00, 3600.00, 4100.00, 4600.00,\
     5100.00, 5600.00, 6100.00, 6600.00, 7100.00, 7600.00, 8100.00, 8600.00, 9100.00, 9600.00, 10100.00]
#dollars = []
#print()

#Dollar value assumed for trade (a specified percentage of each initial dollar)
#assumed_trade_units = []
#for k,_ in enumerate(init_dollars):
    #assumed_trade_units.append(0.1*init_dollars[k])


#The dollar value of the trade bin, which contains the dollars that are used for buying and selling
#trade_dollars = []

#tot_num_trades = []

#Store the adjusted closing value of the day in a list
adj_closing_val_list = sp500_data['Adj Close']

n = 14 #Number of days to wait between trades

#for n in range(2, 100, 2):
    #fixed_dollars, trade_dollars, tot_num_trades = stg.index_val_sign_npts_stg(n, num_rows, init_dollars[0], adj_closing_val_list)
    #if (fixed_dollars < trade_dollars):
       # print(n)

#fixed_dollars, trade_dollars, tot_num_trades = stg.loc_min_max_allinnout_stg(num_rows, init_dollars[0], adj_closing_val_list)
fixed_dollars, trade_dollars, tot_num_trades = stg.index_val_sign_npts_stg(n, num_rows, init_dollars[0], adj_closing_val_list)

#for i,_ in enumerate(init_dollars):
    #val1, val2, val3 = stg.loc_min_max_stg(num_rows, init_dollars[i], adj_closing_val_list, assumed_trade_units[i])
    #val1, val2, val3 = stg.index_val_sign_2pts_stg(num_rows, init_dollars[i], adj_closing_val_list, assumed_trade_units[i])
    #dollars.append(round(val1,2))
    #trade_dollars.append(round(val2,2))
    #tot_num_trades.append(val3)

#Calculate the final value of each initial dollar value invested in the index without doing any trade
#tot_dollars_woutrade = [round(j*(adj_closing_val_list[num_rows-1]/adj_closing_val_list[2]),2) for j in init_dollars]
#Calculate the final value plus trade cash of each initial dollar value invested in the index with the adopted trading strategy
#tot_dollars_wtrade = [sum(x) for x in zip(dollars, trade_dollars)]

f2 = plt.figure(figsize=(12,6))
line1 = plt.plot([j for j in range(num_rows-n)], fixed_dollars, 'k', label="Investment without trade")
line2 = plt.plot([j for j in range(num_rows-n)], trade_dollars, 'r--', label="Investment with trade")
#line3 = plt.plot(init_dollars, trade_dollars, 'k', label="Cash for trading")
#line4 = plt.plot(init_dollars, tot_num_trades, 'r--', label="Number of times traded the index")
plt.legend(loc='upper left')
plt.title("The final value of the investments (with and without trade) against time for {} days into past.\
\nHere the strategy is the local extrema with three data points and the data is captured at trade events".format(num_rows))
plt.xlabel("Time (not a true representation)")
plt.ylabel("Dollars")
#plt.yticks(np.arange(80, 160, 10))
#plt.xlim(0,100)
plt.grid(True)
f2.savefig('local_extrema_3pts_{}yr(s)_plot.pdf'.format(int(num_rows/365)), bbox_inches='tight')

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
