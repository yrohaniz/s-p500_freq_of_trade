import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

#read the data into a DataFrame
sp500_data = pd.read_csv('sp500.csv', index_col='Date', parse_dates=True)
print(sp500_data.head())
#plot the closing value of the index against date
plt.figure(figsize=(14,6))
plt.xlabel("Date")
plt.ylabel("S&P 500 Index")
sns.lineplot(data=sp500_data['Adj Close'], label='Adjusted Closing Value')
plt.show()