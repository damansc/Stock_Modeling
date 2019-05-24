

# method to create data frame that subtracts the dict key's standardized
# adj close from each of its value pairs to get divergence during
# the desired time delta.
import datetime as dt
from sklearn.preprocessing import StandardScaler
from sklearn.linear_modl import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

oneyr = dt.datetime.now()-dt.tiimedelta(365), end=dt.datetime.now(

df divergence(ticker='ticker', start=oneyr, plot=False, reg=False):
		div = df[high_pos_dict[ticker]]['Adj Close']
		scaler = StandardScaler().fit(div)
		global div_std
		div_std = scaler.transform(div)
		div_std_diff = div_std-div_std[ticker]
		
		if plot == True:
			div_std.plot.scatter()
			
		if reg == True:
			lr = LinearRegression()
			y = div_std[ticker]
			X = div_std[~div_std[ticker]]
			X_train, X_test, y_train, y_test = train_test_split(X,y, random_state=23)
			lr.fit(X_train, y_train)
			y_pred = lr.predict(X_test)
			y_true = y_test
			mape = mean_absolute_error(y_true, y_pred)
			mse = mean_squared_error(y_test, y_pred)
			r_sqrd = r2_score(y_true, y_pred)
			return mape, mse, r_sqrd

    sorted_df = div_std_diff.sort_values(by='date', ascending=True)
    condition = sorted_df > 0
    sorted_df['days-in-a-row'] = condition.cumsum() - condition.cumsum().where(~condition).ffill().astype(int)
    return sorted_df
    
    
 ## make method that will be useful for analyze the current days
 # pct change and compare that pct change to previous time
 # periods of the similar change and analyze how they move
 # the next few days afterwards as a way of making a swing trade.
 
 def swing_or_nah(pctdelta=.05, ticker=None, days=1):
 	if ticker==None:
 		ticker_list = []
 		for x in df.columns.values:
 			if df[x][df.datetime.now().date():].pct_change() >= 0.05:
 				 ticker_list.append(x)
 				 print('Stocks with {} percent change: {}'.format(pctdelta, ticker_list))
 		if ticker != None:
 			df = sp500_meta[ticker]['Adj Close'].pct_change()
 			condition_dates = df[(df >= 0.05)].index.values
 			condition_post = condition_dates+dt.timedelta(days)
 			df_post = df[df.index == condition_post]
 			avg_post = df_post.describe()
 			return(avg_post)
 			