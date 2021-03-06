# -*- coding: utf-8 -*-
"""
Created on Fri May 31 08:49:04 2019

@author: daman
"""

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import dash_table
import os

print(os.getcwd())
df = pd.read_csv('sp500_meta.csv')
df.Date = pd.to_datetime(df.Date)
df.set_index([df.Date], inplace=True)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

tickers = df.columns.unique().sort_values()

app.layout = html.Div([
        html.Div([
                html.H1('Stock Dashboard'),
                html.H2('By: Daman Cox'),
                html.H3('Stock Price')
                ]),
        html.Div([
                dcc.Dropdown(id='ticker-picker',
                             options = [{'label': i, 'value': i } for i in tickers],
                             value='MSFT')
                ]),
        html.Div([
                dcc.Graph(id='price-graph')                
                ]),
        html.Div([
                html.H3('Percent Change in Price'),
                dcc.RangeSlider(id='year-slider',
                                updatemode = 'mouseup',
                                min=df.index.min().year,
                                max=df.index.max().year,
                                value=[df.index.min().year, df.index.max().year],
                                marks={str(year): str(year) for year in df.index.year.unique()},
                                step=None)
                ]),
        html.Div([
                dcc.Graph(id='returns-graph')
                ], style={'width': '75%', 'display': 'inline-block'})
        
        ])

# stock price graph.                
@app.callback(
        Output('price-graph', 'figure'),
        [Input('ticker-picker', 'value'),
         Input('year-slider', 'value')])

def update_graphic(ticker_value, year_range):
    mask = (df.index.year >= year_range[0]) & (df.index.year <= year_range[1])
    dff = df[mask]
    
    return {
        'data': [go.Scatter(
                x=dff.index,
                y=dff[ticker_value],
                text=ticker_value,
                )],
        'layout': go.Layout(
                xaxis = {
                        'title': 'Date'
                        },
                yaxis= {
                        'title': 'Price - USD'
                        },
                margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
                hovermode='closest'
                        
                )
            }

# percent change graph
@app.callback(
        Output('returns-graph', 'figure'),
        [Input('ticker-picker', 'value'),
         Input('year-slider', 'value')])

def update_returns(ticker_value, year_range):
    mask = (df.index.year >= year_range[0]) & (df.index.year <= year_range[1])
    dff = df[mask]

    return {
        'data': [go.Scatter(
                x=dff.index,
                y=dff[ticker_value].pct_change(),
                text=ticker_value,
                )],
        'layout': go.Layout(
                xaxis = {
                        'title': 'Date'
                        },
                yaxis= {
                        'title': 'Percent Change'
                        },
                margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
                hovermode='closest'
                        
                )
        }
    
if __name__ == '__main__':
    app.run_server(debug=True)    