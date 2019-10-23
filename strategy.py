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
        if (slope_b > 0.0 and slope_a <= 0.0) and trade_d_per_index >= max_trade:  #If local min and there are enough dollars for trade, buy
            trade_d_per_index -= max_trade
            trade_dollars = trade_d_per_index * adj_closing_val_list[i+2]
            dollars = max_trade * adj_closing_val_list[i+2] + val_per_index * adj_closing_val_list[i+2]
            tot_num_trades += 1
        elif (slope_b < 0.0 and slope_a >= 0.0) and val_per_index > max_trade:  #If local max and there are enough invested dollars, sell
            trade_d_per_index += max_trade
            trade_dollars = trade_d_per_index * adj_closing_val_list[i+2]
            dollars = val_per_index * adj_closing_val_list[i+2] - max_trade * adj_closing_val_list[i+2]
            tot_num_trades += 1
        val_per_index = dollars/adj_closing_val_list[i+2]
        trade_d_per_index = trade_dollars/adj_closing_val_list[i+2]
        max_trade = assumed_trade_units/adj_closing_val_list[i+2]

    return [dollars, trade_dollars, tot_num_trades]

##########################################################################################
##########################################################################################
def index_val_sign_npts_stg(n, num_rows, dollars, adj_closing_val_list):
    """This strategy uses the idea of the value of the index day to day. For this specific one 
        n points are used for evaluating whether the change is positive or negative. 
        The function returns the value of the invested dollars, the trade dollars and the total 
        number of trades executed in the specified number of days.
    """
    #Initialize lists for storing the values of the trade investment dollars and the fixed investment dollars
    trade_dollars = []
    fixed_dollars = []
    fixed_invt_dollars = dollars
    percent = 1.0 #The percentage of dollars that is traded

    #Initialize the dollars invested per unit of the index
    dollars_per_index = dollars/adj_closing_val_list[n]
    dollars = 0.0

    tot_num_trades = 0
    #Perform the trade strategy
    for i in range(num_rows-n):
        #Calculate the diffence between the closing values of the index for today and yesterday, and yesterday and the day before it and so forth
        slope_a = 0.0 
        for j in range(n):
            slope_a += adj_closing_val_list[i+j+1] - adj_closing_val_list[i+j]

        fixed_dollars.append(round(fixed_invt_dollars*(adj_closing_val_list[i+n]/adj_closing_val_list[n]),2))
        if slope_a > 0.0 and dollars > 0:  #If index has increased, buy in
            dollars_per_index += (percent*dollars)/adj_closing_val_list[i+n]
            dollars -= percent * dollars
            tot_num_trades += 1
        elif slope_a < 0.0 and dollars_per_index > 0:  #If index has decreased, sell out
            dollars += percent * dollars_per_index * adj_closing_val_list[i+n]
            dollars_per_index -= percent * dollars_per_index
            tot_num_trades += 1
        trade_dollars.append(round(dollars + dollars_per_index * adj_closing_val_list[i+n],2))

    return [fixed_dollars, trade_dollars, tot_num_trades]

########################################################################################################
########################################################################################################

def loc_min_max_allinnout_stg(num_rows, dollars, adj_closing_val_list):
    """This strategy uses the idea of local minima and maxima for trading. For this specific one 
        three points are used for evaluating the local extrema. 
        The function returns the value of the invested dollars after trading back and forth all 
        the invested dollars each time a minimum and maximum in the index value is hit, and the total 
        number of trades executed in the specified number of days. First move is to buy.
    """
    #Initialize lists for storing the values of the trade investment dollars and the fixed investment dollars
    trade_dollars = []
    fixed_dollars = []
    fixed_invt_dollars = dollars
    percent = 0.1 #The percentage of dollars that is traded

    #Initialize the dollars invested per unit of the index
    dollars_per_index = dollars/adj_closing_val_list[2]
    dollars = 0.0

    tot_num_trades = 0
    #Perform the trade strategy
    for i in range(num_rows-2):
        #Calculate the diffence between the closing values of the index for today and yesterday, and yesterday and the day before it
        slope_a = adj_closing_val_list[i+1] - adj_closing_val_list[i] 
        slope_b = adj_closing_val_list[i+2] - adj_closing_val_list[i+1]
        fixed_dollars.append(round(fixed_invt_dollars*(adj_closing_val_list[i+2]/adj_closing_val_list[2]),2))
        if (slope_b > 0.0 and slope_a < 0.0) and dollars > 0:  #If local min, buy in
            dollars_per_index += (percent*dollars)/adj_closing_val_list[i+2]
            dollars -= percent * dollars
            tot_num_trades += 1
        elif (slope_b < 0.0 and slope_a > 0.0) and dollars_per_index > 0:  #If local max, sell out
            dollars += percent * dollars_per_index * adj_closing_val_list[i+2]
            dollars_per_index -= percent * dollars_per_index
            tot_num_trades += 1
    
        #invt_tr_dols = dollars_per_index * adj_closing_val_list[i+2]
        #if dollars > 0.0:
            #trade_dollars.append(round(dollars,2))
        #elif invt_tr_dols > 0.0:
            #trade_dollars.append(round(invt_tr_dols,2))
        trade_dollars.append(round(dollars + dollars_per_index * adj_closing_val_list[i+2],2))

    return [fixed_dollars, trade_dollars, tot_num_trades]