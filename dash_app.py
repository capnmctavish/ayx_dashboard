import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Load data
cash_flow_df = pd.read_csv('ayx_cash_flow.csv', index_col='Cash_Flow')
cash_flow_df = cash_flow_df.T.reset_index()

balance_sheet_df = pd.read_csv('ayx_balancesheet.csv')
balance_sheet_df = balance_sheet_df.set_index("Balace_sheet_actuals").T
balance_sheet_df.index = pd.to_datetime(balance_sheet_df.index)

stock_df = pd.read_csv('ayx_stock.csv')
stock_df['Date'] = pd.to_datetime(stock_df['Date'])
# Extract relevant columns for plotting
plot_data_cash_flow = cash_flow_df[['Free Cash Flow', 'Net Issuance Payments Of Debt', 'Sale Of Investment']]

# Create Dash app
app = dash.Dash(__name__)

# Define app layout
app.layout = html.Div(children=[
    html.H1(children='Financial Analysis Dashboard'),

    dcc.Graph(
        id='free-cash-flow-plot',
        figure=px.line(cash_flow_df, x='index', y='Free Cash Flow', title='Free Cash Flow Over Time')
    ),

    dcc.Graph(
        id='sale-of-investment-plot',
        figure=px.bar(cash_flow_df, x='index', y='Sale Of Investment', title='Sale Of Investment Over Time')
    ),

    dcc.Graph(
        id='stock-based-compensation-plot',
        figure=px.bar(cash_flow_df, x='index', y='Stock Based Compensation', title='Stock Based Compensation Over Time')
    ),

    dcc.Graph(
        id='cash-flow-analysis-plot',
        figure={
            'data': [
                go.Scatter(x=plot_data_cash_flow.index, y=plot_data_cash_flow[col], mode='lines+markers', name=col) for col in plot_data_cash_flow.columns
            ],
            'layout': {
                'title': 'Cash Flow Analysis',
                'xaxis': {'title': 'Year'},
                'yaxis': {'title': 'Amount in billions'},
                'legend': {'title': 'Cash Flow Type'}
            }
        }
    ),

    dcc.Graph(
        id='balance-sheet-plot',
        figure={
            'data': [
                go.Scatter(x=balance_sheet_df.index, y=balance_sheet_df[col], mode='lines+markers', name=col) for col in balance_sheet_df.columns
            ],
            'layout': {
                'title': 'Total Assets and Total Liabilities Over Time',
                'xaxis': {'title': 'Year'},
                'yaxis': {'title': 'Amount (in billions)'},
                'legend': {'title': 'Balance Sheet Component'}
            }
        }
    ),

    dcc.Graph(
        id='historical-stock-prices-plot',
        figure={
            'data': [
                go.Scatter(x=stock_df['Date'], y=stock_df['Close'], mode='lines+markers', name='Closing Price')
            ],
            'layout': {
                'title': 'Historical Stock Prices',
                'xaxis': {'title': 'Date'},
                'yaxis': {'title': 'Closing Price'},
                'legend': {'title': 'Stock Price'}
            }
        }
    ),

    dcc.Graph(
        id='candlestick-chart-plot',
        figure=go.Figure(data=[go.Candlestick(x=stock_df['Date'],
                                              open=stock_df['Open'],
                                              high=stock_df['High'],
                                              low=stock_df['Low'],
                                              close=stock_df['Close'])],
                        layout={
                            'title': 'Candlestick Chart - Historical Stock Prices',
                            'xaxis': {'title': 'Date'},
                            'yaxis': {'title': 'Stock Price'},
                            'xaxis_rangeslider_visible': False
                        })
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)