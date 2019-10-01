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
print("number of rows and columns:", sp500_data.shape, end='\n\n')

#plot the closing value of the index against date
plt.figure(figsize=(14,6))
plt.xlabel("Date")
plt.ylabel("S&P 500 Index")
sns.lineplot(data=sp500_data['Adj Close'], label='Adjusted Closing Value')
plt.savefig('plot.pdf', bbox_inches='tight')
#plt.show()

#Store the number of rows in the DataFrame
number_rows = len(sp500_data.index)

#Principal value
dollar = int(input("How much do you wish to invest (in dollars)? "))
print()

#Dollar value assumed for trade
assumed_trade_units = 5

#Store the adjusted closing value of the day in a list
adj_closing_val_list = sp500_data['Adj Close']

#Calculate the value of invested dollars with respect to the index
val_per_index = dollar/adj_closing_val_list[0]
cap = val_per_index

tot_num_trades = 0
#Perform the trade strategy
for i in range(number_rows-1):
    slope = adj_closing_val_list[i+1] - adj_closing_val_list[i]
    if slope > 0 and val_per_index < cap:
        val_per_index += (assumed_trade_units*slope)/adj_closing_val_list[i+1]
        tot_num_trades += 1
    elif slope < 0 and val_per_index > 0:
        val_per_index -= (assumed_trade_units*slope)/adj_closing_val_list[i+1]
        tot_num_trades += 1

print("You started your investment with $" + str(dollar) + '.', end='\n\n')
print("The amount of dollars after the adopted trading cycle is $" + str(adj_closing_val_list[-1]*val_per_index) + " and you traded " + str(tot_num_trades) + " times.", end='\n\n')