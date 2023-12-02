import pandas as pd
import os
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

px.defaults.template = "ggplot2"

external_css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css", ]
# Create Dash app
app = dash.Dash(__name__, external_stylesheets=external_css)
server = app.server # Added in for Cloud Run compatibility
# Define app layout
app.layout = html.Div(className='text-dark text-center fw-bold fs-1', children=[
    html.H1(children='Financial Analysis Dashboard'),

    html.Div(className='container-fluid', children=[
        # First Row
        html.Div(className='row', children=[
            # First Column
            html.Div(className='col-md-4', children=[
                dcc.Graph(
                    id='free-cash-flow-plot',
                    figure=px.line(cash_flow_df, x='index', y='Free Cash Flow', title='Free Cash Flow Over Time')
                )
            ]),
            # Second Column
            html.Div(className='col-md-4', children=[
                dcc.Graph(
                    id='sale-of-investment-plot',
                    figure=px.bar(cash_flow_df, x='index', y='Sale Of Investment', title='Sale Of Investment Over Time')
                )
            ]),
            html.Div(className='col-md-4', children=[
                dcc.Graph(
                    id='stock-based-compensation-plot',
                    figure=px.bar(cash_flow_df, x='index', y='Stock Based Compensation', title='Stock Based Compensation Over Time')
                )
            ]),
        ]),

        # Second Row
        html.Div(className='row', children=[            
            # Second Column
            html.Div(className='col-md-6', children=[
                dcc.Graph(
                    id='cash-flow-analysis-plot',
                    figure={
                        'data': [
                            go.Scatter(x=cash_flow_df['index'], y=cash_flow_df[col], mode='lines+markers', name=col) for col in cash_flow_df.columns[1:]
                        ],
                        'layout': {
                            'title': 'Cash Flow Analysis',
                            'xaxis': {'title': 'Year'},
                            'yaxis': {'title': 'Amount in billions'},
                            'legend': {'title': 'Cash Flow Type'}
                        }
                    }
                )
            ]),
            html.Div(className='col-md-6', children=[
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
                )
            ]),
        ]),

        # Third Row
        html.Div(className='row', children=[            
            # Second Column
            html.Div(className='col-md-6', children=[
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
                )
            ]),
            html.Div(className='col-md-6', children=[
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
        ]),
    ]),
])



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))