import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import strategy as stg

x = np.linspace(6, 7, num=10)
new_x = []
for num in x:
    new_x.append(num + np.random.choice([-0.9, 0.1]))

y = np.exp(new_x)
output = pd.DataFrame({'Date': x, 'Adj Close': y})
output.to_csv("fakedata.csv", index=False)
#plt.figure(figsize=(12,6))
#plt.plot(x,y)
#plt.show()

print(output.tail(10))

num_rows, _ = output.shape
adj_closing_val_list = output['Adj Close']

fixed_dollars, trade_dollars, tot_num_trades = stg.loc_min_max_allinnout_stg(num_rows, 100.00, adj_closing_val_list)

f2 = plt.figure(figsize=(12,6))
line1 = plt.plot(x[2:], fixed_dollars, 'k', label="Investment without trade")
line2 = plt.plot(x[2:], trade_dollars, 'r--', label="Investment with trade")
#line3 = plt.plot(x, y, 'b')
plt.legend(loc='upper left')
plt.title("The final value of the investments (with and without trade) against time for {} days into past.\
\nHere the strategy is the local extrema with three data points and the data is captured at trade events".format(num_rows))
plt.xlabel("Time (not a true representation)")
plt.ylabel("Dollars")
#plt.yticks(np.arange(80, 160, 10))
#plt.xlim(0,100)
plt.grid(True)
f2.savefig('local_extrema_3pts_{}yr(s)_plot.pdf'.format(int(num_rows/365)), bbox_inches='tight')

#print(fixed_dollars)
#print(trade_dollars)