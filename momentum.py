

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
		
		
			