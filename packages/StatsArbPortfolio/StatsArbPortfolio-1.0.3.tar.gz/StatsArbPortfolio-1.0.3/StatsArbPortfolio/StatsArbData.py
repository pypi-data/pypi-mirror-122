import pandas as pd
import numpy as np
import datetime
from os import listdir
from os.path import exists
import yfinance as yf
np.random.seed(0)

class Data:
	def __init__(self, trading_year):
		wikidata = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]
		self.trading_year = trading_year
		self.sp500 = list(wikidata["Symbol"])
		self.START = str(trading_year-3)+"-01-01"
		self.END = str(trading_year+1)+"-01-06"
		print("imported data from {} to {}".format(self.START, self.END))
    
	def import_data(self, download_new_data = False):
		datafile_name = "data_{}-{}".format(self.trading_year-3,self.trading_year)
		if exists(datafile_name) and not download_new_data:
			print("{} is available already".format(datafile_name))
			df = pd.read_csv(datafile_name)
			return df
		self.n_companies = 0
		df = pd.DataFrame([], columns = ["Date"])
		for i, name in enumerate(self.sp500):
			cols = []
			try:
				ticker = yf.Ticker(name)
				hist = ticker.history(start = self.START, end = self.END).reset_index()
				if hist.shape[0] > 0:
					if self.n_companies == 0:
						df["Date"] = hist["Date"]
					df[name] = hist["Close"]
					self.n_companies += 1
					print("#",i, name, "was successfully appended!!!")
				else:
					print("#",i, name, "has not enough data")
			except:
				print("#",i, name, "failed to append...")
		df.to_csv(datafile_name, index = False, header = True)
		print("data has been saved with name {}".format(datafile_name))
		return df

	def number_of_companies(self):
		return self.n_companies

class Prepared_Data:
	def __init__(self, df, year):
		self.df = df
		try:
			self.df["Date"] = self.df["Date"].apply(lambda x: x.strftime("%Y-%m-%d"))
		except:
			print("Date is already string") 
		self.test_year = year

	def datasets(self):
		def create_label(df,perc=[0.5,0.5]):
			perc = [0.]+list(np.cumsum(perc))
			label = df.iloc[:,1:].pct_change(fill_method=None)[1:].apply(lambda x: pd.qcut(x.rank(method='first'),perc,labels=False), axis=1)
			return label
        
		def create_stock_data(df, st):
			st_data = pd.DataFrame([])
			st_data['Date'] = list(df['Date'])
			st_data['Name'] = [st]*len(st_data)
			for k in list(range(1,21))+list(range(40,241,20)):
				st_data['R'+str(k)] = df[st].pct_change(k)
			st_data['R-future'] = df[st].pct_change().shift(-1)  
			st_data['label'] = list(label[st])+[np.nan] 
			st_data['Month'] = list(df['Date'].str[:-3])
			st_data = st_data.dropna()
		    
			trade_year = st_data['Month'].str[:4]
			st_data = st_data.drop(columns=['Month'])
			st_train_data = st_data[trade_year<str(self.test_year)]
			st_test_data = st_data[trade_year==str(self.test_year)]
			return np.array(st_train_data),np.array(st_test_data)

		label = create_label(self.df)
		stock_names = sorted(list(self.df.columns[1:]))
		train_data,test_data = [],[]

		for st in stock_names:
			st_train_data,st_test_data = create_stock_data(self.df,st)
			train_data.append(st_train_data)
			test_data.append(st_test_data)

		train_data = np.concatenate([x for x in train_data])
		test_data = np.concatenate([x for x in test_data])

		self.y_training = train_data[:,-1]
		self.y_testing = test_data[:,-1]
		self.X_training = train_data[:,2:-2]
		self.X_testing = test_data[:,2:-2]

		return train_data, test_data

	def train_test_datasets(self):
		return self.X_training.astype(float), self.y_training.astype(float), self.X_testing.astype(float), self.y_testing.astype(float)


class ObtainData:
	def __init__(self, trading_year):
		self.finance_data = Data(trading_year = trading_year)
		self.data = self.finance_data.import_data()
		self.prepared_data = Prepared_Data(self.data, year = 2019)
		self.train_data, self.trading_data = self.prepared_data.datasets()
		self.X_training, self.y_training, self.X_testing, self.y_testing = self.prepared_data.train_test_datasets()
	
	def getSplitData(self):
		print("Train dataset size: ", self.train_data.shape, "Trading dataset size: ", self.trading_data.shape)
		print(self.train_data[:5,:3])
		print(self.trading_data[:5,:3])
		return self.X_training, self.y_training, self.X_testing, self.y_testing

	def getTrainTestData(self):
		return self.train_data, self.trading_data

