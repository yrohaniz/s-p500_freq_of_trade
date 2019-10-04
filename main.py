import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

#Number of rows to skip from the top (the older data)
toprow = int(input("Please specify the number of days from the past you would like to skip? "))
#read the data into a DataFrame
sp500_data = pd.read_csv('sp500.csv', index_col='Date', parse_dates=True, skiprows=[i for i in range(1,toprow+1)])

#print the last 5 rows in the DataFrame and its number of rows and columns
print(sp500_data.tail(), end='\n\n')
r, _ = sp500_data.shape
print("Number of days in the index market: " + str(r), end='\n\n')

#plot the closing value of the index against date
plt.figure(figsize=(14,6))
plt.xlabel("Date")
plt.ylabel("S&P 500 Index")
sns.lineplot(data=sp500_data['Adj Close'], label='Adjusted Closing Value')
plt.savefig('plot.pdf', bbox_inches='tight')
#plt.show()

#Store the number of rows in the DataFrame
number_rows = len(sp500_data.index)

#Starting value for the investment
init_dollars = int(input("How much do you wish to invest (in dollars)? "))
dollars = init_dollars
print()

#Dollar value assumed for trade
assumed_trade_units = 10.0
#The dollar value of the trade bin, which contains the dollars that are used for buying and selling
trade_dollars = 0.0

#Store the adjusted closing value of the day in a list
adj_closing_val_list = sp500_data['Adj Close']

#Calculate and initialize the trading dollars per unit of the index
val_per_index = dollars/adj_closing_val_list[1]  #the invested dollars per unit index
trade_d_per_index = trade_dollars/adj_closing_val_list[1]  #the dollars in the trade bin per unit index
max_trade = assumed_trade_units/adj_closing_val_list[1]  #maximum value of traded dollars per unit index

tot_num_trades = 0
#Perform the trade strategy
for i in range(number_rows-1):
    slope = adj_closing_val_list[i+1] - adj_closing_val_list[i]  #Calculate the diffence between the closing values of the index for today and yesterday
    if slope > 0 and trade_d_per_index >= max_trade:  #If the slope is positive and there are enough dollars for trade, buy
        trade_d_per_index -= max_trade
        trade_dollars = trade_d_per_index * adj_closing_val_list[i+1]
        dollars = max_trade * adj_closing_val_list[i+1] + val_per_index * adj_closing_val_list[i+1]
        tot_num_trades += 1
    elif slope < 0 and val_per_index > max_trade:  #If the slope is negative and there are enough invested dollars, sell
        trade_d_per_index += max_trade
        trade_dollars = trade_d_per_index * adj_closing_val_list[i+1]
        dollars = val_per_index * adj_closing_val_list[i+1] - max_trade * adj_closing_val_list[i+1]
        tot_num_trades += 1
    val_per_index = dollars/adj_closing_val_list[i+1]
    trade_d_per_index = trade_dollars/adj_closing_val_list[i+1]
    max_trade = assumed_trade_units/adj_closing_val_list[i+1]
    

print("You started your investment with $" + str(init_dollars) + '.', end='\n\n')
print("The trade bin from which you've made changes on your investment has a value of ${:.2f} in the index market.".format(
    trade_dollars), end='\n\n')
print("Your total amount of dollars (invested plus trade dollars) after the \
current trading cycle is ${:.2f} and you traded {} times.".format(
    dollars + trade_dollars, tot_num_trades)
    )