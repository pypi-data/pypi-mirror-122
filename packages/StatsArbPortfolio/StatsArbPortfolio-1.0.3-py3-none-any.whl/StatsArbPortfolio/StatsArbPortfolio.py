import pandas as pd
import numpy as np
import datetime
from os import listdir
import yfinance as yf
import torch 
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.datasets as dsets
import torch.nn.functional as F
import matplotlib.pylab as plt
import numpy as np
import pandas as pd
import sys
from torch.utils.data import Dataset, DataLoader
from os import listdir
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import r2_score
from joblib import dump, load
from . import StatsArbModels #as Models
from . import StatsArbData #.ObtainData as ObtainData

class Portfolio:
	def __init__(self, trading_year, stock):
		self.stock = stock
		temp = ObtainData(trading_year = trading_year)
		self.train_data, self.trading_data = temp.getTrainTestData()
		mask = pd.Series(self.trading_data[:,1]).apply(lambda x: True if x.upper() in [stock] else False)
		self.df = self.trading_data[mask]
		self.start_date = str(trading_year) + "-01-01"
		self.end_date = str(trading_year+1) + "-01-01"

	def simulation(self, name, prices, signal, init_budget = 10000):
		sharpe_ratio = [0]
		roi = [0]
		holdings = []
		cash = []
		total = []

		bnh_roi = [0]
		daily_returns = [0]
		bnh_sharpe_ratio = []

		initial_shares = init_budget // prices[0]

		name = name.upper()
		budget = init_budget
		shares = 0
		investment = 0
		length = prices.shape[0]
		
		for i, (curPrice, curSignal) in enumerate(zip(list(prices), list(signal))):
			if curSignal == 1 and shares == 0 and i < length-1:
            			shares = (budget // curPrice)
            			investment += shares * curPrice
            			budget -= investment
			elif investment > 0 and curSignal == 0 or i == length-1:
            			budget += shares * curPrice
            			shares = 0
            			investment = 0
            			roi.append(budget/init_budget - 1)
            			sharpe_ratio.append(np.mean(roi)/np.std(roi))
			holdings.append(shares*curPrice)
			cash.append(budget)
			total.append(budget + shares*curPrice)

			if i > 0:
				daily_returns.append((prices[i-1]-prices[i])/prices[i-1])
				bnh_roi.append((initial_shares*prices[i] - init_budget)/init_budget)

			if len(roi) < len(total):
				if i != 0:
					roi.append(roi[-1])
					sharpe_ratio.append(sharpe_ratio[-1])

			bnh_sharpe_ratio.append(np.mean(bnh_roi)/np.std(bnh_roi))
          
		print(name)
		print("final budget: $", budget)
		print("Algorithm Return: ", roi[-1])
		print("Algorithm Sharpe Ratio: ", sharpe_ratio[-1])

		bnh_return = (initial_shares*prices[-1]-init_budget)/init_budget
		print("Buy & Hold Return: ", bnh_return)
		print("Buy & Hold Sharpe Ratio: ", bnh_sharpe_ratio[-1])

		return roi[-1], bnh_return, (bnh_roi, bnh_sharpe_ratio, roi, sharpe_ratio, holdings, cash, total)

	def plot_trading(self, stk, model_name, prices, signals, dates, roi):
		dummy = pd.DataFrame([])
		dummy["Date"] = dates
		dummy["Price"] = prices
		dummy["Signal"] = signals
          
		mask = dummy["Signal"].diff() != 0
		mask[0] = True
      
		dummy["Signal"] = dummy["Signal"][mask]
		dummy = dummy.set_index("Date")
      
		plt.figure(figsize = (14,7))
		plt.title(stk + " " + model_name +" Signals. ROI: " + str(roi), fontsize = 8)
		plt.plot(dummy["Price"], color = "gray", label = "Closing Price")
		plt.plot(dummy["Price"][dummy["Signal"] == 1], '^', color = 'g', label = "BUY/HOLD")
		plt.plot(dummy["Price"][dummy["Signal"] == 0], 'v', color = 'r', label = "SELL/SHORT")
		plt.legend()

		plt.xticks(dummy.index[::15], fontsize = 16, rotation = 45)
		plt.yticks(fontsize = 16)
		plt.show()
  
	def plot_roi(self, stk, model_name, df):
		plt.figure(figsize = (14,7))
		plt.title("ROI for {} using {}".format(stk, model_name))
		plt.plot(df["ROI"], color = "b", label = "Algorithm")
		plt.plot(df["ROI BnH"], color = "r", label = "Buy & Hold")
		plt.legend()
	      
		plt.ylabel("ROI %")
		plt.show()

	def plot_sharpe_ratio(self, stk, model_name, df):
		plt.figure(figsize = (14,7))
		plt.title("Sharpe Ratio for {} using {}".format(stk, model_name))
		plt.plot(df["Sharpe Ratio"], color = "b", label="Algorithm")
		plt.plot(df["Sharpe Ratio BnH"], color = "r", label="Buy & Hold")
		plt.legend()

		plt.ylabel("Sharpe Ratio")
		plt.show()
  
	def plot_cash(self, stk, model_name, df):
		plt.figure(figsize = (14,7))
		plt.title("Returns for {} using {}".format(stk, model_name))
		plt.plot(df["Holdings"], color = "b", label = "Holdings")
		plt.plot(df["Cash"], color = "g", label = "Cash")
		plt.plot(df["Total"], color = "r", label = "Total")
		plt.legend()
		
		plt.ylabel("US$")
		plt.show()

	def BackTesting(self, model = None, model_name = "None", my_df = None, plot_holding_cash = True, ):
		name = self.stock.upper()
		stk = yf.Ticker(name)
		hist_data = stk.history(start = self.start_date, end = self.end_date).reset_index()
		prices = np.asanyarray(hist_data["Close"])
		dates = hist_data["Date"]

		X = self.trading_data[self.trading_data[:,1] == name][:,2:-2]

		signals = None
		if "DNN" in model_name:
			X = torch.tensor(X.astype(float)).float()
			z = model(X)
			_, y_hat = torch.max(z,1)
			signals = y_hat.numpy()
		else:
			signals = model.predict(X)

		roi, bnh_roi, (bnh_returns, bnh_sharpe_ratio, returns, sharpe_ratio, holdings, cash, total) = self.simulation(name, prices, signals)
		self.plot_trading(name, model_name, prices, signals, dates, roi)

		temp_df = pd.DataFrame([])
		temp_df["Date"] = dates
		temp_df["Sharpe Ratio BnH"] = np.array(bnh_sharpe_ratio)
		temp_df["Sharpe Ratio"] = np.array(sharpe_ratio)
		temp_df["ROI"] = np.array(returns)
		temp_df["ROI BnH"] = np.array(bnh_returns)
		temp_df["Holdings"] = np.array(holdings)
		temp_df["Cash"] = np.array(cash)
		temp_df["Total"] = np.array(total)
		temp_df = temp_df.set_index("Date")

		self.plot_cash(name, model_name, temp_df)
		self.plot_roi(name, model_name, temp_df)
		self.plot_sharpe_ratio(name, model_name, temp_df)

	def portfolios(self, model, model_id = 1):
		assert model_id == 1 or model_id == 2 or model_id == 3 or model_id == 4, "model_id should be 1 (DNN Model 1), 2 (DNN Model 2), 3 (Random Forest), or 4 (Gradient Boosted Trees)"
		if model_id == 1:
			self.BackTesting(model, "DNN Model 1")
		if model_id == 2:
			self.BackTesting(model, "DNN Model 2")
		if model_id == 3:
			self.BackTesting(model, "Random Forests")
		if model_id == 4:
			self.BackTesting(model, "Gradient-Boosted Trees")

class Simulation:
	def __init__(self, trading_year, stock, model_id):
		self.trading_year = trading_year
		self.portfolio = Portfolio(trading_year = trading_year, stock = stock)
		self.model_id = model_id
		self.my_model = Models(self.trading_year)
		self.dnn1, self.dnn2, self.rf, self.gbt = self.my_model.getModels()

	def plot_data(self):
		assert self.model_id == 1 or self.model_id == 2 or self.model_id == 3 or self.model_id == 4, "model_id is {} should be 1 (DNN Model 1), 2 (DNN Model 2), 3 (Random Forest), or 4 (Gradient Boosted Trees)".format(self.model_id)
		if self.model_id == 1:
			self.portfolio.portfolios(self.dnn1, model_id = self.model_id)
		if self.model_id == 2:
			self.portfolio.portfolios(self.dnn2, model_id = self.model_id)
		if self.model_id == 3:
			self.portfolio.portfolios(self.rf, model_id = self.model_id)
		if self.model_id == 4:
			self.portfolio.portfolios(self.gbt, model_id = self.model_id)
      
