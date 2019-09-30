import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

#Number of rows to skip from the top (the older data)
toprow = 7000
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
plt.show()

#Store the number of rows in the DataFrame
number_rows = len(sp500_data.index)

#Principal value
dollar = 100

#Appreciation/Depreciation value
assumed_A_D_val = 5

#Store the adjusted closing value of the day in a list
adj_closing_val_list = sp500_data['Adj Close']

init_dollar = dollar
#Perform the investment strategy
for i in range(number_rows-1):
    slope = adj_closing_val_list[i+1] - adj_closing_val_list[i]
    if slope > 0:
        dollar += assumed_A_D_val
    elif slope < 0:
        dollar -= assumed_A_D_val
    else:
        dollar = dollar

print("The final value of the investment: " + str(dollar), end='\n\n')

rel_Apprn = ((dollar - init_dollar)/init_dollar)*100
print("Relative appreciation in percent: " + str(rel_Apprn))