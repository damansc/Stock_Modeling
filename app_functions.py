# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 09:38:12 2019

@author: daman
"""

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import os


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
        html.Div([
                html.H1('Budgeting Dashboard'),
                html.H2('Carolyn and Daman Household Budget')
                ]),
        html.Div([
                dcc.Tabs(id='budget-tabs', value='total-hh', children = [
                        dcc.Tab(label='Total Household', value='total-hh'),
                        dcc.Tab(label='Carolyn', value='carolyn-budget'),
                        dcc.Tab(label='Daman', value='daman-budget')])
                ]),
        html.Div([
                dcc.Input(placeholder='income',
                          type=int,
                          value=2083),
                dcc.Input(placeholder='bills',
                          type=int,
                          value=1169),
                dcc.Input(placeholder='savings',
                          type=int,
                          value=0),
                dcc.Input(placeholder='Investments',
                          type=int,
                          value=0)
                ])
        
        ])