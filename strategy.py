def loc_min_max_stg(num_rows, dollars, adj_closing_val_list, assumed_trade_units):
    """This strategy uses the idea of local minima and maxima for trading. For this specific one 
        three points are used for evaluating the local extrema. 
        The function returns the value of the invested dollars, the trade dollars and the total 
        number of trades executed in the specified number of days.
    """
    #Calculate and initialize the dollars traded and invested per unit of the index
    trade_dollars = 0.0
    val_per_index = dollars/adj_closing_val_list[2]  #the invested dollars per unit index
    trade_d_per_index = trade_dollars/adj_closing_val_list[2]  #the dollars in the trade bin per unit index
    max_trade = assumed_trade_units/adj_closing_val_list[2]  #maximum value of traded dollars per unit index

    tot_num_trades = 0
    #Perform the trade strategy
    for i in range(num_rows-2):
        #Calculate the diffence between the closing values of the index for today and yesterday, and yesterday and the day before it
        slope_a = adj_closing_val_list[i+1] - adj_closing_val_list[i] 
        slope_b = adj_closing_val_list[i+2] - adj_closing_val_list[i+1]
        if (slope_b > 0 and slope_a < 0) and trade_d_per_index >= max_trade:  #If local min and there are enough dollars for trade, buy
            trade_d_per_index -= max_trade
            trade_dollars = trade_d_per_index * adj_closing_val_list[i+2]
            dollars = max_trade * adj_closing_val_list[i+2] + val_per_index * adj_closing_val_list[i+2]
            tot_num_trades += 1
        elif (slope_b < 0 and slope_a > 0) and val_per_index > max_trade:  #If local max and there are enough invested dollars, sell
            trade_d_per_index += max_trade
            trade_dollars = trade_d_per_index * adj_closing_val_list[i+2]
            dollars = val_per_index * adj_closing_val_list[i+2] - max_trade * adj_closing_val_list[i+2]
            tot_num_trades += 1
        val_per_index = dollars/adj_closing_val_list[i+2]
        trade_d_per_index = trade_dollars/adj_closing_val_list[i+2]
        max_trade = assumed_trade_units/adj_closing_val_list[i+2]

    return [dollars, trade_dollars, tot_num_trades]