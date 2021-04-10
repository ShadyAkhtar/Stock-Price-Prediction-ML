import base64
import os
import sys
sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)))
os.chdir(os.path.realpath(os.path.dirname(__file__)))

import pandas as pd
from flask import Flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from datetime import datetime 
from datetime import timedelta
import urllib3, shutil
import model


UPLOAD_DIRECTORY = "../datasets/data"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


external_stylesheets=[dbc.themes.BOOTSTRAP]

# Normally, Dash creates its own Flask server internally. By creating our own,
# we can create a route for downloading files directly:
server = Flask(__name__)
app = dash.Dash(server=server, external_stylesheets=external_stylesheets)

controls = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("Select Stock"),
                dcc.Dropdown(
                    id="my-dropdown",
                    options=[
                        # {'label': 'Google', 'value': 'GOOGL'},
                        # {'label': 'Tata Motors', 'value': 'TATAMOTORS'},
                        {'label': 'Reliance', 'value': 'RELIANCE'},
                        {'label': 'Indigo', 'value': 'INDIGO'},
                        {'label': 'Infosys', 'value': 'INFY'},
                        {'label': 'IRCTC', 'value': 'IRCTC'},
                        {'label': 'Aurobindo Pharma', 'value': 'AUROPHARMA'},
                        # {'label': 'AT&T Inc.', 'value': 'T'}
            
                    ],
                    value='RELIANCE',
                ),
                html.Br(),
                
            ]
        ),
    
        
    ],
    body=True,
)

app.layout = dbc.Container(
    [
        html.H1("Stock Recommendation System", style={
            'textAlign': 'center'}),
        html.Hr(),

        dbc.Alert(
    [
        html.H4("Forecasting Stock Predictions Using Machine Learning!", className="alert-heading"),
        html.P(
            "T.Y.Bsc (Computer Science) [2020-21] "
            "Semester- VI Project,"
            # "R. D. National College, Bandra - 400050"
        ),
    ]
),

        dbc.Row(
            [
                dbc.Col(controls, md=3),
                
                dbc.Col(dcc.Graph(id="my-graph"), md=9),
            ],
            align="left",
        ),

        html.Div(id='my-div', style={
            'textAlign': 'center',
            'color':'red',
            'font':'16px',

        }),

        
        html.Br(),
        html.Br(),
        html.Br(),

    ],
    fluid=True,


)


@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def get_data(selected_dropdown_value):


    date = datetime.today()
    ts = datetime.timestamp(date)
    start = int(ts)

    tss = datetime.today() - timedelta(days=3650)
    tss = datetime.timestamp(tss)
    end = int(tss)
    end

    # # url = 'https://query1.finance.yahoo.com/v7/finance/download/{}?period1={}&period2={}&interval=1d&events=history'.format(selected_dropdown_value,end,start)
    # url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=BSE:{}&apikey=DFS&outputsize=full&datatype=csv'.format(selected_dropdown_value)
    # c = urllib3.PoolManager()
    # filename = "../datasets/data/{}.csv".format(selected_dropdown_value)


    # with c.request('GET', url, preload_content=False) as res, open(filename, 'wb') as out_file:
    #     shutil.copyfileobj(res, out_file)

    data = pd.read_csv("../datasets/data/{}.csv".format(selected_dropdown_value), index_col = "timestamp")
    data.sort_values(["timestamp"], ascending = True, inplace=True)
    data.index = pd.to_datetime(data.index)



    #data = yf.download(selected_dropdown_value, start=datetime(2008, 5, 5), end=datetime.now())

    # dff = pd.DataFrame(data)
    # dfff = dff.set_index('timestamp')
    
    df = model.moving_avg(data)
    
    dff = model.make_predictions(data)
    

    return {
        'data': [{
            'x': df.index,
            'y': df['close'],
            'name': 'Close'
        },
        {
            'x': df.index,
            'y': df['MA10'],
            'name': 'MA10'

        },
        {
            'x': df.index,
            'y': df['MA30'],
            'name': 'MA30'

        },
        {
            'x': df.index,
            'y': df['MA44'],
            'name': 'MA44'

        },
        {
            'x': df.index,
            'y': df['MA50'],
            'name': 'MA50'

        },
        {
            'x': df.index,
            'y': df['rets'],
            'name': 'Returns'

        },
        {
            'x': dff.index,
            'y': dff['Forecast_reg'],
            'name': 'Regression',
            
        },
        {
            'x': dff.index,
            'y': dff['Forecast_knn'],
            'name': 'KNN',
            

        },
        {
            'x': dff.index,
            'y': dff['forecast_by'],
            'name': 'Bayesian',
            

        }
        ],
        'layout': {'margin': {'l': 60, 'r': 60, 't': 30, 'b': 30},'title': 'Stock Data Visualization', 'align':'center'}
    }



@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input('my-dropdown', 'value')]
)
def sentiment(input_value):

    polarity = model.retrieving_tweets_polarity(input_value)

    if polarity > 0:
        return 'According to the predictions and twitter sentiment analysis -> Investing in "{}" is a GREAT idea!'.format(str(input_value))
    
    elif polarity < 0:
        return 'According to the predictions and twitter sentiment analysis -> Investing in "{}" is a BAD idea!'.format(str(input_value))
            
    return 'According to the predictions and twitter sentiment analysis -> Investing in "{}" is a BAD idea!'.format(str(input_value))






if __name__ == "__main__":
    app.run_server(debug=True, port=8080)