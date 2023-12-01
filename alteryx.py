
import yfinance as yahooFinance
import pandas as pd
import csv

GetAlteryxInformation = yahooFinance.Ticker("AYX")
ticker_hostorical_data = yahooFinance.download(tickers="AYX")
print(type(data))
data.to_csv('data.csv')


# print(GetAlteryxInformation.history(period="max"))
ayx = yahooFinance.Ticker("AYX")
print(ayx.balancesheet)
# ayx.balancesheet.to_csv('ayx_balancesheet.csv')
# ayx.earnings_trend.to_csv('ayx_earnings_trend.csv')
ayx.cash_flow.to_csv('ayx_cash_flow.csv')