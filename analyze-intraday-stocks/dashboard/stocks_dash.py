# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import explore

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


fig = explore.query1()

app.layout = html.Div(children=[
    html.H1(children='Hello stocks'),

    #dcc.Graph(figure=explore.query1()),
    #dcc.Graph(figure=explore.query2()),
    #dcc.Graph(figure=explore.query3()),
    html.Div(["Input symbol: ",
              dcc.Input(id='symbol-input', value="AAPL", type='text')]),
    html.Br(),
    html.Div(["Input date: ",
              dcc.Input(id='date-input', value="2021-05-03", type='text')]),
    html.Br(),
    dcc.Graph(figure=explore.query8(symbol="AAPL", date="2021-05-03"),
              id="candlestick")
    
])

@app.callback(
    Output('candlestick', 'figure'),
    Input('date-input', 'value'),
    Input('symbol-input', 'value'))

def update_figure(selected_date, selected_symbol):
    return explore.query8(symbol=selected_symbol, date=selected_date)

if __name__ == '__main__':
    app.run_server(debug=True)