import dash
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output
import dash_core_components as dcc
from dash import dash_table

# from pandas_datareader import data as web
import yfinance as yf
from datetime import datetime as Dt

import numpy as np
import pandas as pd
from ta.trend import MACD
from ta.momentum import StochasticOscillator
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import math

import sys
from scipy import stats
import statsmodels.regression.linear_model as lm
import statsmodels.api as sm
import datetime


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# # app = dash.Dash(__name__)
# page2_table_example = pd.read_csv('AAPL_stock_data.csv')
# page2_table_example = page2_table_example.iloc[page2_table_example.shape[1]-10]

app.layout = html.Div(
    dbc.Container(
        dbc.Tabs(
            [
                dbc.Tab(
                    [
                        html.Br(),
                        html.P('The latest international macro-enocomic data are shown below'),
                        dcc.Graph(id='page1-graph1'),
                        dcc.Graph(id='page1-graph2'),
                        dcc.Graph(id='page1-graph3'),
                        dcc.Graph(id='page1-graph4'),
                        dcc.Graph(id='page1-graph5'),
                        dcc.Graph(id='page1-graph6'),
                        dcc.Graph(id='page1-graph7'),
                        dcc.Graph(id='page1-graph8'),
                        dcc.Graph(id='page1-graph9')
                    ],
                    label='Financial Data Dashboard'
                ),
                dbc.Tab(
                    [
                        html.Br(),
                        html.P('Please choose the start year'),
                        dcc.Dropdown(
                            id='page2-dropdown1',
                            options=[
                                {'label': '2010', 'value': '2010'},
                                {'label': '2011', 'value': '2011'},
                                {'label': '2012', 'value': '2012'},
                                {'label': '2013', 'value': '2013'},
                                {'label': '2014', 'value': '2014'},
                                {'label': '2015', 'value': '2015'},
                                {'label': '2016', 'value': '2016'},
                                {'label': '2017', 'value': '2017'},
                                {'label': '2018', 'value': '2018'},
                                {'label': '2019', 'value': '2019'},
                                {'label': '2020', 'value': '2020'},
                                {'label': '2021', 'value': '2021'}
                            ], value='2020'),
                        html.P('Please choose the interested stock in the dropdown'),
                        dcc.Dropdown(
                            id='page2-dropdown2',
                            options=[
                                {'label': 'Coke', 'value': 'COKE'},
                                {'label': 'Tesla', 'value': 'TSLA'},
                                {'label': 'Apple', 'value': 'AAPL'},
                                {'label': 'Amazon', 'value': 'AMZN'},
                                {'label': 'MicroSoft', 'value': 'MSFT'},
                                {'label': 'Nvidia', 'value': 'NVDA'},
                                {'label': 'IBM', 'value': 'IBM'},
                                {'label': 'Boeing', 'value': 'BA'},
                                {'label': 'S&P 500', 'value': '^GSPC'},
                                {'label': 'Nasdaq', 'value': 'NDAQ'},
                                {'label': 'Dow Jones', 'value': '^DJI'},
                                {'label': 'FTSE100', 'value': '^FTSE'}
                            ], value='AMZN'),
                        dcc.Graph(id='page2-graph1'),
                        html.P('Please select how many days of the selected stock data to display'),
                        dcc.Dropdown(
                            id='table_drop',
                            options=[{'label': '1', 'value': 1},
                                     {'label': '2', 'value': 2},
                                     {'label': '3', 'value': 3},
                                     {'label': '4', 'value': 4},
                                     {'label': '5', 'value': 5},
                                     {'label': '6', 'value': 6},
                                     {'label': '7', 'value': 7},
                                     {'label': '8', 'value': 8},
                                     {'label': '9', 'value': 9},
                                     {'label': '10', 'value': 10}], value=5
                        ),
                        dash_table.DataTable(id='page2_table'),
                        dcc.Graph(id='page2-graph2'),
                        dcc.Graph(id='page2-graph3'),
                        dcc.Graph(id='page2-graph4'),
                        dcc.Graph(id='page2-graph5'),
                        dcc.Graph(id='page2-graph6')
                    ],
                    label='Stock Data Visualization'
                ),
                dbc.Tab(
                    [
                        html.Br(),
                        html.P('Welcome to use stock comparison tool'),
                        html.P('Please select the start date'),
                        dbc.Input(id="page2_2_input1", placeholder="yyyy-mm-dd", type="text", value='2021-01-01'),
                        html.P('Please select the end date'),
                        dbc.Input(id="page2_2_input2", placeholder="yyyy-mm-dd", type="text", value='2021-12-31'),
                        html.P('Please select the first target stock'),
                        dcc.Dropdown(
                            id='page2_2_dropdown1',
                            options=[
                                {'label': 'Coke', 'value': 'COKE'},
                                {'label': 'Tesla', 'value': 'TSLA'},
                                {'label': 'Apple', 'value': 'AAPL'},
                                {'label': 'Amazon', 'value': 'AMZN'},
                                {'label': 'MicroSoft', 'value': 'MSFT'},
                                {'label': 'Nvidia', 'value': 'NVDA'},
                                {'label': 'IBM', 'value': 'IBM'},
                                {'label': 'Boeing', 'value': 'BA'},
                                {'label': 'S&P_500', 'value': '^GSPC'},
                                {'label': 'Nasdaq', 'value': 'NDAQ'},
                                {'label': 'Dow_Jones', 'value': '^DJI'}
                            ], value='AMZN'),
                        html.P('Please select the second target stock'),
                        dcc.Dropdown(
                            id='page2_2_dropdown2',
                            options=[
                                {'label': 'Coke', 'value': 'COKE'},
                                {'label': 'Tesla', 'value': 'TSLA'},
                                {'label': 'Apple', 'value': 'AAPL'},
                                {'label': 'Amazon', 'value': 'AMZN'},
                                {'label': 'MicroSoft', 'value': 'MSFT'},
                                {'label': 'Nvidia', 'value': 'NVDA'},
                                {'label': 'IBM', 'value': 'IBM'},
                                {'label': 'Boeing', 'value': 'BA'},
                                {'label': 'S&P_500', 'value': '^GSPC'},
                                {'label': 'Nasdaq', 'value': 'NDAQ'},
                                {'label': 'Dow_Jones', 'value': '^DJI'}
                            ],
                            value='BA'),
                        dcc.Graph(id='page2_2_graph1'),
                        dcc.Graph(id='page2_2_graph2'),
                        dcc.Graph(id='page2_2_graph3'),
                        dcc.Graph(id='page2_2_graph4')
                    ],
                    label='Stock comparison'
                ),
                dbc.Tab(

                    [
                        html.Br(),
                        html.P('Welcome to use CAPM model visualization tool. If nothing is shown, please try other input options a few times until it works well.'),
                        html.P('Please select the start date'),
                        dbc.Input(id="page3_input1", placeholder="yyyy-mm-dd", type="text", value='2021-01-01'),
                        html.P('Please select the end date'),
                        dbc.Input(id="page3_input2", placeholder="yyyy-mm-dd", type="text", value='2021-12-31'),
                        html.P('Please select the first target stock'),
                        html.P('Please select the interested stock'),
                        dcc.Dropdown(
                            id='page3-dropdown1',
                            options=[
                                {'label': 'Coke', 'value': 'COKE'},
                                {'label': 'Tesla', 'value': 'TSLA'},
                                {'label': 'Apple', 'value': 'AAPL'},
                                {'label': 'Amazon', 'value': 'AMZN'},
                                {'label': 'MicroSoft', 'value': 'MSFT'},
                                {'label': 'Nvidia', 'value': 'NVDA'},
                                {'label': 'IBM', 'value': 'IBM'},
                                {'label': 'Boeing', 'value': 'BA'},
                            ], value='AMZN'),
                        html.P('Please select the benchmark'),
                        dcc.Dropdown(
                            id='page3-dropdown2',
                            options=[
                                {'label': 'S&P_500', 'value': '^GSPC'},
                                {'label': 'Nasdaq', 'value': 'NDAQ'},
                                {'label': 'Dow_Jones', 'value': '^DJI'}
                            ],
                            value='^GSPC'),

                        dcc.Graph(id='page3-graph1'),
                        dcc.Graph(id='page3-graph2')
                    ],
                    label='CAPM model on selected stock'
                ),
                dbc.Tab(
                    [
                        html.Br(),
                        html.P('Welcome to use Fama French and Q5-factor multi factor model visualization tool. This can take a bit long, even 1 minutes, sorry for the wait.'),
                        html.P('Please select the interested stock'),
                        dcc.Dropdown(
                            id='page4-dropdown1',
                            options=[
                                {'label': 'Coke', 'value': 'COKE'},
                                {'label': 'Tesla', 'value': 'TSLA'},
                                {'label': 'Apple', 'value': 'AAPL'},
                                {'label': 'Amazon', 'value': 'AMZN'},
                                {'label': 'MicroSoft', 'value': 'MSFT'},
                                {'label': 'Nvidia', 'value': 'NVDA'},
                                {'label': 'IBM', 'value': 'IBM'},
                                {'label': 'Boeing', 'value': 'BA'},
                                {'label': 'S&P_500', 'value': '^GSPC'},
                                {'label': 'Nasdaq', 'value': 'NDAQ'},
                                {'label': 'Dow_Jones', 'value': '^DJI'},
                                {'label': 'FTSE100', 'value': '^FTSE'}
                            ], value='AMZN'),
                        dcc.Graph(id='page4-graph1'),
                        dcc.Graph(id='page4-graph2'),
                        dcc.Graph(id='page4-graph3'),
                        dcc.Graph(id='page4-graph4'),
                        dcc.Graph(id='page4-graph5'),
                        dcc.Graph(id='page4-graph6'),
                    ],
                    label='Fama French and Q5-factor on selected stock'

                ),
            ]
        ),
        style={'margin-top': '50px'}
    )
)


@app.callback([Output('page2_table', 'data'), Output('page2_table', 'columns')],
              [Input('page2-dropdown2', 'value'), Input('table_drop', 'value')])
def update_page2_table(page2_input2, page2_input_table):
    table = yf.download(page2_input2, start='2022-01-01', proxy="127.0.0.1:33210")
    table = table.iloc[table.shape[0] - page2_input_table:]
    # print('table:', table)
    table_columns = [{'name': col, 'id': col} for col in table.columns]
    table_data = table.to_dict(orient='records')
    return table_data, table_columns


@app.callback([Output('page2-graph1', 'figure'), Output('page2-graph2', 'figure'), Output('page2-graph3', 'figure'),
               Output('page2-graph4', 'figure'), Output('page2-graph5', 'figure'), Output('page2-graph6', 'figure'),

               Output('page1-graph1', 'figure'), Output('page1-graph2', 'figure'), Output('page1-graph3', 'figure'),
               Output('page1-graph4', 'figure'), Output('page1-graph5', 'figure'), Output('page1-graph6', 'figure')
                  , Output('page1-graph7', 'figure'), Output('page1-graph8', 'figure'), Output('page1-graph9', 'figure')],
              [Input('page2-dropdown1', 'value'), Input('page2-dropdown2', 'value')])
def update_page2_graph(page2_input1, page2_input2):
    # print('page2 input1 is year ', str(page2_input1))
    start_time = str(page2_input1)+'-01-01'
    # print('page2 input1 is year ', start)
    df = yf.download(page2_input2, start=start_time, proxy="127.0.0.1:33210")
    # table = df.copy(deep=True)
    # table = table.iloc[table.shape[0] - page2_input_table:]
    # # print('table:', table)
    # table_columns = [{'name': col, 'id': col} for col in table.columns]
    # table_data = table.to_dict(orient='records')

    fig1 = go.Figure(go.Candlestick(x=df.index,
                                    open=df['Open'],
                                    high=df['High'],
                                    low=df['Low'],
                                    close=df['Close'],
                                    showlegend=False),
                     layout=go.Layout(
                         title=go.layout.Title(text=f"Stock Price and Moving Average of {page2_input2}")))

    # 把非交易日排除掉
    # hide weekends
    fig1.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])
    # removing all empty dates
    # build complete timeline from start date to end date
    dt_all = pd.date_range(start=df.index[0], end=df.index[-1])
    # retrieve the dates that ARE in the original datset
    dt_obs = [d.strftime("%Y-%m-%d") for d in pd.to_datetime(df.index)]
    # define dates with missing values
    dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]
    fig1.update_xaxes(rangebreaks=[dict(values=dt_breaks)])

    # add moving average
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()
    fig1.add_trace(go.Scatter(x=df.index,
                              y=df['MA5'],
                              opacity=0.7,
                              line=dict(color='blue', width=2),
                              name='MA 5'))

    fig1.add_trace(go.Scatter(x=df.index,
                              y=df['MA20'],
                              opacity=0.7,
                              line=dict(color='orange', width=2),
                              name='MA 20'))
    fig1.add_trace(go.Scatter(x=df.index,
                              y=df['MA50'],
                              opacity=0.7,
                              line=dict(color='pink', width=2),
                              name='MA 50'))

    # Plot volume trace on 2nd row
    fig2 = go.Figure(go.Bar(x=df.index,
                            y=df['Volume'],
                            ),
                     layout=go.Layout(title=go.layout.Title(text=f"Stock Trading Volumn of {page2_input2}")))
    # Plot MACD trace on 3rd row
    # MACD
    macd = MACD(close=df['Close'],
                window_slow=26,
                window_fast=12,
                window_sign=9)
    fig3 = go.Figure(go.Bar(x=df.index,
                            y=macd.macd_diff(),
                            name='MACD_DIF',
                            ),
                     layout=go.Layout(title=go.layout.Title(text=f"MACD Indicator {page2_input2}")))
    fig3.add_trace(go.Scatter(x=df.index,
                              y=macd.macd(),
                              line=dict(color='black', width=2),
                              name='MACD_DEA'
                              ))
    fig3.add_trace(go.Scatter(x=df.index,
                              y=macd.macd_signal(),
                              line=dict(color='blue', width=1),
                              name='MACD moving average of 3 days'
                              ))
    # Plot stochastics trace on 4th row
    # stochastic
    stoch = StochasticOscillator(high=df['High'],
                                 close=df['Close'],
                                 low=df['Low'],
                                 window=14,
                                 smooth_window=3)
    fig4 = go.Figure(go.Scatter(x=df.index,
                                y=stoch.stoch(),
                                line=dict(color='black', width=2),
                                name='stochastic'
                                ),
                     layout=go.Layout(title=go.layout.Title(text=f"Stochastic of {page2_input2}")))
    fig4.add_trace(go.Scatter(x=df.index,
                              y=stoch.stoch_signal(),
                              name='stochastic moving average of 3 days',
                              line=dict(color='blue', width=1),
                              ))
    # 传统的stochastics oscillator 80超买，20超卖,把这个加进stochastics

    const1 = np.linspace(start=20, stop=20, num=len(df.index))
    const2 = np.linspace(start=80, stop=80, num=len(df.index))
    fig4.add_trace(go.Scatter(x=df.index,
                              y=const1,
                              line=dict(color='red', width=1),
                              name='20'
                              ))
    fig4.add_trace(go.Scatter(x=df.index,
                              y=const2,
                              line=dict(color='green', width=1),
                              name='80'
                              ))

    # fig5 volatility
    df.insert(df.shape[1], 'Ln', 0)
    df.insert(df.shape[1], 'Ln2', 0)

    for i in range(df.shape[0] - 1):
        df['Ln'].iloc[i + 1] = math.log(df['Close'].iloc[i + 1] / df['Close'].iloc[i])
        df['Ln2'].iloc[i + 1] = df['Ln'].iloc[i + 1] ** 2
    df.insert(df.shape[1], 'Volatility', 0)
    for i in range(df.shape[0] - 2):
        df['Volatility'].iloc[i + 2] = math.sqrt(df['Ln2'].iloc[1:i + 2].sum() / (i + 2 - 1))
    fig5 = go.Figure(go.Scatter(x=df.index,
                                y=df['Volatility'],
                                line=dict(color='blue', width=1)
                                ),
                     layout=go.Layout(title=go.layout.Title(text=f"Volatility of {page2_input2}")))

    # figure6 value at risk
    df['daily_ret'] = df['Close'].pct_change(1)
    # print(df)
    sRate = df['daily_ret'].iloc[1:].sort_values(ascending=True)
    # print(sRate)
    p = np.percentile(sRate, (1, 5, 10), interpolation='midpoint')  # 输出分位度为1%，5%和10%即置信度99%，95%和90%时的值
    print(p)  # 1%分位值为第一个-0.05377872，即根据历史数据，value at risk回报率高于-0.05377872的可能为99%
    fig6 = go.Figure(go.Bar(x=['99%', '95%', '90%'],
                            y=p
                            ), layout=go.Layout(
        title=go.layout.Title(text=f"Value at risk on 99%, 95% and 90% of {page2_input2}")))

    # show gdp data
    world_gdp_data = pd.read_csv('API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4251000.csv')
    # world_gdp_data = world_gdp_data.reset_index(drop=True)
    world_gdp = world_gdp_data.iloc[259][4:66]
    China_gdp = world_gdp_data.iloc[40][4:66]
    USA_gdp = world_gdp_data.iloc[251][4:66]
    UK_gdp = world_gdp_data.iloc[81][4:66]
    # print(Russian_gdp)
    x = np.arange(1960, 2022, 1)
    page1_fig1 = go.Figure(go.Scatter(
        x=x,
        y=world_gdp,
        name='World GDP data'), layout=go.Layout(title=go.layout.Title(text="GDP data of world main economy"),
                                                 xaxis_title="Year", yaxis_title="GDP/million dollars", )
    )
    page1_fig1.add_trace(go.Scatter(
        x=x,
        y=China_gdp,
        name='China GDP data')
    )
    page1_fig1.add_trace(go.Scatter(
        x=x,
        y=USA_gdp,
        name='USA GDP data')
    )
    page1_fig1.add_trace(go.Scatter(
        x=x,
        y=UK_gdp,
        name='UK GDP data')
    )

    # show gdp per capital data
    world_gdp_perCapital_data = pd.read_csv('API_NY.GDP.PCAP.CD_DS2_en_csv_v2_4251004.csv')
    world_gdp_perCapital = world_gdp_perCapital_data.iloc[259][4:66]
    China_gdp_perCapital = world_gdp_perCapital_data.iloc[40][4:66]
    USA_gdp_perCapital = world_gdp_perCapital_data.iloc[251][4:66]
    UK_gdp_perCapital = world_gdp_perCapital_data.iloc[81][4:66]
    x2 = np.arange(1960, 2022, 1)
    page1_fig2 = go.Figure(go.Scatter(
        x=x2,
        y=world_gdp_perCapital,
        name='World GDP per capital data'),
        layout=go.Layout(title=go.layout.Title(text="GDP per capital data of world main economy"),
                         xaxis_title="Year", yaxis_title='GDP per capital/dollars', )
    )
    page1_fig2.add_trace(go.Scatter(
        x=x2,
        y=China_gdp_perCapital,
        name='China GDP per capital data')
    )
    page1_fig2.add_trace(go.Scatter(
        x=x2,
        y=USA_gdp_perCapital,
        name='USA GDP per capital data')
    )
    page1_fig2.add_trace(go.Scatter(
        x=x2,
        y=UK_gdp_perCapital,
        name='UK GDP per capitaldata')
    )

    # show gdp growth rate data
    world_gdp_growth_data = pd.read_csv('API_NY.GDP.PCAP.KD.ZG_DS2_en_csv_v2_4250851.csv')
    world_gdp_growth = world_gdp_growth_data.iloc[259][4:66]
    China_gdp_growth = world_gdp_growth_data.iloc[40][4:66]
    USA_gdp_growth = world_gdp_growth_data.iloc[251][4:66]
    UK_gdp_growth = world_gdp_growth_data.iloc[81][4:66]
    x3 = np.arange(1960, 2022, 1)
    page1_fig3 = go.Figure(go.Scatter(
        x=x3,
        y=world_gdp_growth,
        name='World GDP growth rate'),
        layout=go.Layout(title=go.layout.Title(text="GDP growth rate of world main economy"),
                         xaxis_title="Year", yaxis_title='GDP growth rate/percent', )
    )
    page1_fig3.add_trace(go.Scatter(
        x=x3,
        y=China_gdp_growth,
        name='China GDP growth rate')
    )
    page1_fig3.add_trace(go.Scatter(
        x=x3,
        y=USA_gdp_growth,
        name='USA GDP growth rate')
    )
    page1_fig3.add_trace(go.Scatter(
        x=x3,
        y=UK_gdp_growth,
        name='UK GDP growth rate')
    )

    # show world electricity consumption data
    world_electricity_data = pd.read_csv('API_EG.USE.ELEC.KH.PC_DS2_en_csv_v2_4251643.csv')
    world_electricity = world_electricity_data.iloc[259][4:66]
    China_electricity = world_electricity_data.iloc[40][4:66]
    USA_electricity = world_electricity_data.iloc[251][4:66]
    UK_electricity = world_electricity_data.iloc[81][4:66]
    x4 = np.arange(1960, 2022, 1)
    page1_fig4 = go.Figure(go.Scatter(
        x=x4,
        y=world_electricity,
        name='World electricity consumption'),
        layout=go.Layout(title=go.layout.Title(text="Electricity Consumption of world main economy"),
                         xaxis_title="Year", yaxis_title='Electricity consumption / kW·h per capital', )
    )
    page1_fig4.add_trace(go.Scatter(
        x=x4,
        y=China_electricity,
        name='China electricity consumption')
    )
    page1_fig4.add_trace(go.Scatter(
        x=x4,
        y=USA_electricity,
        name='USA electricity consumption')
    )
    page1_fig4.add_trace(go.Scatter(
        x=x4,
        y=UK_electricity,
        name='UK electricity consumption')
    )

    # show world population rate data
    world_population_data = pd.read_csv('API_SP.POP.GROW_DS2_en_csv_v2_4251293.csv')
    world_population = world_population_data.iloc[259][4:66]
    China_population = world_population_data.iloc[40][4:66]
    USA_population = world_population_data.iloc[251][4:66]
    UK_population = world_population_data.iloc[81][4:66]
    x5 = np.arange(1960, 2022, 1)
    page1_fig5 = go.Figure(go.Scatter(
        x=x5,
        y=world_population,
        name='World population growth rate'),
        layout=go.Layout(title=go.layout.Title(text="Population growth rate of world main economy"),
                         xaxis_title="Year", yaxis_title='Population growth rate / percent', )
    )
    page1_fig5.add_trace(go.Scatter(
        x=x5,
        y=China_population,
        name='China population growth rate')
    )
    page1_fig5.add_trace(go.Scatter(
        x=x5,
        y=USA_population,
        name='USA population growth rate')
    )
    page1_fig5.add_trace(go.Scatter(
        x=x5,
        y=UK_population,
        name='UK population growth rate')
    )

    # show world inflation data(GDP deflator)
    world_inflation_data = pd.read_csv('API_NY.GDP.DEFL.KD.ZG_DS2_en_csv_v2_4250766.csv')
    world_inflation = world_inflation_data.iloc[259][4:66]
    China_inflation = world_inflation_data.iloc[40][4:66]
    USA_inflation = world_inflation_data.iloc[251][4:66]
    UK_inflation = world_inflation_data.iloc[81][4:66]
    x6 = np.arange(1960, 2022, 1)
    page1_fig6 = go.Figure(go.Scatter(
        x=x6,
        y=world_inflation,
        name='World inflation rate'),
        layout=go.Layout(title=go.layout.Title(text="inflation rate of world main economy"),
                         xaxis_title="Year", yaxis_title='inflation rate / percent', )
    )
    page1_fig6.add_trace(go.Scatter(
        x=x6,
        y=China_inflation,
        name='China inflation rate')
    )
    page1_fig6.add_trace(go.Scatter(
        x=x6,
        y=USA_inflation,
        name='USA inflation rate')
    )
    page1_fig6.add_trace(go.Scatter(
        x=x6,
        y=UK_inflation,
        name='UK inflation rate')
    )

    # show gold data
    start_date = '2021-1-1'
    today = datetime.date.today()
    latest_day = today + datetime.timedelta(days=-1)
    # end_date = '2022-7-22'
    Gold_data = yf.download('GLD', start=start_date, end=latest_day, group_by="ticker", proxy="127.0.0.1:33210",
                            index_col=0, auto_adjust=True)
    page1_fig7 = go.Figure(go.Scatter(
        x=Gold_data.index, y=Gold_data['Close']),
        layout=go.Layout(title=go.layout.Title(text=f'Gold Price from{start_date} until {today}'),
                         xaxis_title="Year", yaxis_title='Gold Price/dollar', )
    )

    # show oil data
    Oil_data = yf.download('USO', start=start_date, end=today, group_by="ticker", proxy="127.0.0.1:33210",
                           index_col=0, auto_adjust=True)
    page1_fig8 = go.Figure(go.Scatter(
        x=Oil_data.index, y=Oil_data['Close']),
        layout=go.Layout(title=go.layout.Title(text=f'Oil Price from{start_date} until {today}'),
                         xaxis_title="Year", yaxis_title='Oil Price/dollar', )
    )

    # show gas data
    Gas_data = yf.download('UNG', start=start_date, end=today, group_by="ticker", proxy="127.0.0.1:33210",
                           index_col=0, auto_adjust=True)
    page1_fig9 = go.Figure(go.Scatter(
        x=Gas_data.index, y=Gas_data['Close']),
        layout=go.Layout(title=go.layout.Title(text=f'Gas Price from{start_date} until {today}'),
                         xaxis_title="Year", yaxis_title='Gas Price/dollar', )
    )


    return fig1, fig2, fig3, fig4, fig5, fig6, page1_fig1, page1_fig2, page1_fig3, page1_fig4, page1_fig5, page1_fig6, page1_fig7, page1_fig8, page1_fig9


@app.callback([Output('page2_2_graph1', 'figure'), Output('page2_2_graph2', 'figure'), Output('page2_2_graph3', 'figure'), Output('page2_2_graph4', 'figure')],
              [Input('page2_2_input1', 'value'), Input('page2_2_input2', 'value'), Input('page2_2_dropdown1', 'value'), Input('page2_2_dropdown2', 'value')])
def update_page2_2(startDate, endDate, stock1, stock2):
    stockData1 = yf.download(stock1, start=startDate, end=endDate, proxy="127.0.0.1:33210")
    stockData2 = yf.download(stock2, start=startDate, end=endDate, proxy="127.0.0.1:33210")
    market_benchmark = yf.download('^GSPC', start=startDate, end=endDate, group_by='ticker', proxy="127.0.0.1:33210")
    stockData1['daily_ret'] = stockData1['Close'].pct_change(1)
    stockData2['daily_ret'] = stockData2['Close'].pct_change(1)
    market_benchmark['daily_ret'] = market_benchmark['Close'].pct_change(1)
    # compare daily return of the chosen two stock
    page2_2_fig1 = go.Figure(go.Scatter(
                    x=stockData1.index,
                    y=stockData1['daily_ret'],
                    name=f'daily return curve of {stock1}'), layout=go.Layout(title=go.layout.Title(text=f'Comparison of  daily return of {stock1} and {stock2}'),
                                                             xaxis_title='Date', yaxis_title='Return Rate')
                          )
    page2_2_fig1.add_trace(go.Scatter(
                    x=stockData2.index,
                    y=stockData2['daily_ret'],
                    name = f'daily return curve of {stock2}')
                        )
    page2_2_fig1.add_trace(go.Scatter(
        x=market_benchmark.index,
        y=market_benchmark['daily_ret'],
        name=f'daily return curve of S&P 500')
    )
    # compare return rate, sharpe ratio and value at risk of the chosen two stock
    return_rate1 = stockData1['Close'].iloc[stockData1.shape[0]-1] / stockData1['Close'].iloc[0] * 100
    return_rate2 = stockData2['Close'].iloc[stockData2.shape[0]-1] / stockData2['Close'].iloc[0] * 100
    return_market = market_benchmark['Close'].iloc[market_benchmark.shape[0] - 1] / market_benchmark['Close'].iloc[0] * 100

    RiskFreeRate = 1.2855 / 100  # UK 1-Year Treasury Bond on 30/03/2022
    sharpe_stock1 = (stockData1['Close'] - RiskFreeRate).mean() / (stockData1['Close'] - RiskFreeRate).std()
    sharpe_stock2 = (stockData2['Close'] - RiskFreeRate).mean() / (stockData2['Close'] - RiskFreeRate).std()
    # print(return_market['Close'])
    sharpe_market = (market_benchmark['Close'] - RiskFreeRate).mean() / (market_benchmark['Close'] - RiskFreeRate).std()

    sRate1 = stockData1['daily_ret'].iloc[1:].sort_values(ascending=True)
    p1 = np.percentile(sRate1, (1, 5, 10), interpolation='midpoint')  # 输出分位度为1%，5%和10%即置信度99%，95%和90%时的值
    sRate2 = stockData2['daily_ret'].iloc[1:].sort_values(ascending=True)
    p2 = np.percentile(sRate2, (1, 5, 10), interpolation='midpoint')  # 输出分位度为1%，5%和10%即置信度99%，95%和90%时的值
    sRate_market = market_benchmark['daily_ret'].iloc[1:].sort_values(ascending=True)
    p_m = np.percentile(sRate_market, (1, 5, 10), interpolation='midpoint')  # 输出分位度为1%，5%和10%即置信度99%，95%和90%时的值

    # print([return_rate1, sharpe_stock1, p1[0], p1[1], p1[2]])
    # print([return_rate2, sharpe_stock2, p2[0], p2[1], p2[2]])
    page2_2_fig2 = go.Figure(go.Bar(x=['return rate'],
                                    y=[return_rate1],
                                    name=f'return rate of {stock1}'
                                    ), layout=go.Layout(
                            title=go.layout.Title(text=f"return rate of {stock1} and {stock2}")))
    page2_2_fig2.add_trace(go.Bar(x=['return rate'],
                                  y=[return_rate2],
                                  name=f'return rate of {stock2}'))
    page2_2_fig2.add_trace(go.Bar(x=['return rate'],
                                  y=[return_market],
                                  name=f'return rate of S&p 500'))

    page2_2_fig3 = go.Figure(go.Bar(x=['Sharpe ratio'],
                                    y=[sharpe_stock1],
                                    name=f'Sharpe ratio of {stock1}'
                                    ), layout=go.Layout(
        title=go.layout.Title(text=f"Sharpe Ratio of {stock1} and {stock2}")))
    page2_2_fig3.add_trace(go.Bar(x=['Sharpe ratio'],
                                  y=[sharpe_stock2],
                                  name=f'Sharpe ratio of {stock2}'))
    page2_2_fig3.add_trace(go.Bar(x=['Sharpe ratio'],
                                  y=[sharpe_market],
                                  name=f'Sharpe ratio of S&P 500'))
    categories = ['99%', '95%', '90%']

    page2_2_fig4 = go.Figure(go.Scatterpolar(
        r=p1,
        theta=categories,
        fill='toself',
        name=f'Value at Risk of {stock1}')
    )
    page2_2_fig4.add_trace(go.Scatterpolar(
        r=p2,
        theta=categories,
        fill='toself',
        name=f'Value at Risk of {stock2}'
    ))
    page2_2_fig4.add_trace(go.Scatterpolar(
        r=p_m,
        theta=categories,
        fill='toself',
        name='Value at Risk of S&P 500'
    ))
    # page2_2_fig4 = go.Figure(go.Bar(x=['99%', '95%', '90%'],
    #                                 y=p1,
    #                                 name=f'Value at Risk of {stock1}'
    #                                 ), layout=go.Layout(
    #     title=go.layout.Title(text=f"Value at risk on 99%, 95% and 90% of {stock1} and {stock2}")))
    # page2_2_fig4.add_trace(go.Bar(x=['99%', '95%', '90%'],
    #                               y=p2,
    #                               name=f'Value at Risk of {stock2}'))
    # page2_2_fig4.add_trace(go.Bar(x=['99%', '95%', '90%'],
    #                               y=p_m,
    #                               name='Value at Risk of S&P 500'))
    return page2_2_fig1, page2_2_fig2, page2_2_fig3, page2_2_fig4

@app.callback([Output('page3-graph1', 'figure'), Output('page3-graph2', 'figure')],
              [Input('page3_input1', 'value'), Input('page3_input2', 'value'), Input('page3-dropdown1', 'value'), Input('page3-dropdown2', 'value')])
def update_page3_graph(startDate, endDate, input1, input2):
    #     page3 capm model
    RISKY_ASSET = input1
    MARKET_BENCHMARK = input2
    # print('page3_Risky', RISKY_ASSET)
    # print('page3_market', MARKET_BENCHMARK)
    stockObject = yf.download(RISKY_ASSET, start=startDate, end=endDate, proxy="127.0.0.1:33210")
    marketBenchmark = yf.download(MARKET_BENCHMARK, start=startDate, end=endDate, group_by="ticker",
                                  proxy="127.0.0.1:33210")
    # print(marketBenchmark)
    stockObject['Close'] = stockObject['Close'] / stockObject['Close'].iloc[0]
    marketBenchmark['Close'] = marketBenchmark['Close'] / marketBenchmark['Close'].iloc[0]
    stockObject['daily_ret'] = stockObject['Close'].pct_change(1)
    marketBenchmark['daily_ret'] = marketBenchmark['Close'].pct_change(1)
    lr = stats.linregress(stockObject['daily_ret'].iloc[1:], marketBenchmark['daily_ret'].iloc[1:])

    beta, alpha, r_value, p_value, std_err = lr
    rf = 1.2855 / 100  # UK 1-Year Treasury Bond on 30/03/2022
    Ef = (marketBenchmark['Close'].iloc[marketBenchmark['Close'].shape[0] - 1] - marketBenchmark['Close'].iloc[0]) / \
         marketBenchmark['Close'].iloc[0]
    CAPM_expectReturnRate = rf + beta * (Ef - rf)
    page3_fig1 = go.Figure(go.Bar(
        x=['risk-free rate', 'market rate', f'CAPM model rate of {RISKY_ASSET}'],
        y=[rf, Ef, CAPM_expectReturnRate]), layout=go.Layout(title=go.layout.Title(
        text=f'Investing Return Rate of Risk-free Rate, Market Rate and CAPM model Rate of {RISKY_ASSET}'),
                                                             xaxis_title="investing rate comparison",
                                                             yaxis_title='investing return rate')
    )

    RiskFreeRate = 1.2855 / 100  # UK 1-Year Treasury Bond on 30/03/2022
    sharpe_stock = (stockObject['Close'] - RiskFreeRate).mean() / (stockObject['Close'] - RiskFreeRate).std()
    sharpe_market = (marketBenchmark['Close'] - RiskFreeRate).mean() / (marketBenchmark['Close'] - RiskFreeRate).std()
    page3_fig2 = go.Figure(go.Bar(
        x=[f'Sharpe Ratio of {RISKY_ASSET}', f'Sharpe Ratio of {MARKET_BENCHMARK}'],
        y=[sharpe_stock, sharpe_market]),
        layout=go.Layout(title=go.layout.Title(text=f'Sharpe Ratio of {RISKY_ASSET} and Market Benchmark'),
                         xaxis_title="Sharpe Ratio Comparison", yaxis_title='Sharpe Ratio')
    )
    return page3_fig1, page3_fig2


#page4 multi factor
@app.callback([Output('page4-graph1','figure'),Output('page4-graph2','figure'),Output('page4-graph3','figure'),Output('page4-graph4','figure'),Output('page4-graph5','figure'), Output('page4-graph6','figure')]
              ,[Input('page4-dropdown1', 'value')])
def update_page4_graph(page4_input1):
    RISKY_ASSET = page4_input1
    page4_start_date = '2019-1-1'
    page4_end_date = '2021-12-30'
    # print('page4 input',page4_input1)
    stockObject_page4 = yf.download(RISKY_ASSET, start=page4_start_date, end=page4_end_date, group_by="ticker",proxy="127.0.0.1:33210", index_col=0)

    stockObject_page4_qFactor = stockObject_page4.copy(deep=True)# 复制一份给qfactor用
    returns_3 = pd.read_csv('F-F_Research_Data_Factors_daily.csv', index_col=0)
    returns_5 = pd.read_csv('F-F_Research_Data_5_Factors_2x3_daily.csv', index_col=0)
    returns_3['Date'] = returns_3.index
    returns_5['Date'] = returns_5.index
    stockObject_page4['daily_ret'] = stockObject_page4['Close'].pct_change(1)

    # 观察发现3因子和5因子数据集的SMB不一样，Mkt-RF和HML是一样的
    stockObject_page4['Date'] = stockObject_page4.index
    stockObject_page4.insert(stockObject_page4.shape[1], 'Mkt-RF', 0)
    stockObject_page4.insert(stockObject_page4.shape[1], 'SMB_3', 0)
    stockObject_page4.insert(stockObject_page4.shape[1], 'SMB_5', 0)
    stockObject_page4.insert(stockObject_page4.shape[1], 'HML', 0)
    stockObject_page4.insert(stockObject_page4.shape[1], 'RMW', 0)
    stockObject_page4.insert(stockObject_page4.shape[1], 'CMA', 0)
    stockObject_page4.insert(stockObject_page4.shape[1], 'RF', 0)

    # 合并fama french五因子数据到yf 股票data里 yf下载的数据可能比上面得到的end_iloc要提前（yf似乎下载指定结束日期之前交易日的数据）
    for i in range(returns_3.shape[0]):
        if Dt.strptime(returns_3['Date'][i], '%Y/%m/%d') == Dt.strptime(str(stockObject_page4['Date'].iloc[0]).split(' ')[0], '%Y-%m-%d'):
            iloc_offset_3 = i
#                 print('OFFSET iteration is', iloc_offset_3)
    for i in range(returns_5.shape[0]):
        if Dt.strptime(returns_5['Date'][i], '%Y/%m/%d') == Dt.strptime(str(stockObject_page4['Date'].iloc[0]).split(' ')[0], '%Y-%m-%d'):
            iloc_offset_5 = i
#                 print('OFFSET iteration is', iloc_offset_5)
        # 然后，把stockObject那段长度之前的fama-french数据放进stockObject

    for i in range(stockObject_page4.shape[0]):
        stockObject_page4['Mkt-RF'].iloc[i] = returns_3['Mkt-RF'].iloc[i + iloc_offset_3]
        stockObject_page4['SMB_3'].iloc[i] = returns_3['SMB'].iloc[i + iloc_offset_3]
        stockObject_page4['SMB_5'].iloc[i] = returns_5['SMB'].iloc[i + iloc_offset_5]
        stockObject_page4['HML'].iloc[i] = returns_3['HML'].iloc[i + iloc_offset_3]
        stockObject_page4['RMW'].iloc[i] = returns_5['RMW'].iloc[i + iloc_offset_5]
        stockObject_page4['CMA'].iloc[i] = returns_5['CMA'].iloc[i + iloc_offset_5]
        stockObject_page4['RF'].iloc[i] = returns_3['RF'].iloc[i + iloc_offset_3]
        stockObject_page4['daily_ret'].iloc[i] -= returns_3['RF'].iloc[i + iloc_offset_3]

    # stockObject.loc[1:,'CT'] = ct.add_constant(stockObject) #ct是多元线性拟合的截距项
    x_ff3 = stockObject_page4[['Mkt-RF', 'SMB_3', 'HML']].iloc[1:]
    y_ff3 = stockObject_page4['daily_ret'].iloc[1:]
    x_ff3 = sm.add_constant(x_ff3)
    ff3fm = lm.OLS(y_ff3, x_ff3).fit()
    x_ff5 = stockObject_page4[['Mkt-RF', 'SMB_5', 'HML', 'RMW', 'CMA']].iloc[1:]
    y_ff5 = stockObject_page4['daily_ret'].iloc[1:]
    x_ff5 = sm.add_constant(x_ff5)
    ff5fm = lm.OLS(y_ff5, x_ff5).fit()
    print('Fama French 3 factors summary')
    print(ff3fm.summary())
    print('Fama French 5 factors summary')
    print(ff5fm.summary())

    # 绘制ff5fm模型预测收益率，和实际进行可视化对比
    intercept3, beta_Mkt_RF_3, beta_SMB_3, beta_HML_3 = ff3fm.params
    intercept5, beta_Mkt_RF_5, beta_SMB_5, beta_HML_5, beta_RMW, beta_CMA = ff5fm.params
    stockObject_page4.insert(stockObject_page4.shape[1], 'ff3fm_return', 0)
    stockObject_page4.insert(stockObject_page4.shape[1], 'ff5fm_return', 0)
    stockObject_page4['ff3fm_return'] = stockObject_page4['RF'] + beta_Mkt_RF_3 * stockObject_page4['Mkt-RF'] + beta_SMB_3 * stockObject_page4['SMB_3'] + beta_HML_3 * stockObject_page4['HML']
    stockObject_page4['ff5fm_return'] = stockObject_page4['RF'] + beta_Mkt_RF_5 * stockObject_page4['Mkt-RF'] + beta_SMB_5 * stockObject_page4['SMB_5'] + beta_HML_5 * stockObject_page4['HML'] + beta_RMW * stockObject_page4['RMW'] + beta_CMA * stockObject_page4['CMA']

    #跑一下q5模型
    q_returns = pd.read_csv('q5_factors_daily_2021_2.csv', index_col=0)
    q_returns.columns.tolist
    # returns.rename_axis('Date',axis='columns')
    q_returns['Date'] = q_returns.index
    # print(q_returns)
    stockObject_page4_qFactor['daily_ret'] = stockObject_page4_qFactor['Close'].pct_change(1)

    stockObject_page4_qFactor['Date'] = stockObject_page4_qFactor.index
    stockObject_page4_qFactor.insert(stockObject_page4_qFactor.shape[1], 'Mkt-RF', 0)
    stockObject_page4_qFactor.insert(stockObject_page4_qFactor.shape[1], 'ME', 0)
    stockObject_page4_qFactor.insert(stockObject_page4_qFactor.shape[1], 'IA', 0)
    stockObject_page4_qFactor.insert(stockObject_page4_qFactor.shape[1], 'ROE', 0)
    stockObject_page4_qFactor.insert(stockObject_page4_qFactor.shape[1], 'EG', 0)
    stockObject_page4_qFactor.insert(stockObject_page4_qFactor.shape[1], 'RF', 0)

    for i in range(q_returns.shape[0]):
        if Dt.strptime(q_returns['Date'][i], '%Y/%m/%d') == Dt.strptime(str(stockObject_page4_qFactor['Date'].iloc[0]).split(' ')[0], '%Y-%m-%d'):
            iloc_offset_qFactor = i
#         print('qFactor OFFSET iteration is', iloc_offset_qFactor)
    for i in range(stockObject_page4_qFactor.shape[0]):
        stockObject_page4_qFactor['Mkt-RF'].iloc[i] = q_returns['R_MKT'].iloc[i + iloc_offset_qFactor] - q_returns['R_F'].iloc[i + iloc_offset_qFactor]
        stockObject_page4_qFactor['ME'].iloc[i] = q_returns['R_ME'].iloc[i + iloc_offset_qFactor]
        stockObject_page4_qFactor['IA'].iloc[i] = q_returns['R_IA'].iloc[i + iloc_offset_qFactor]
        stockObject_page4_qFactor['ROE'].iloc[i] = q_returns['R_ROE'].iloc[i + iloc_offset_qFactor]
        stockObject_page4_qFactor['EG'].iloc[i] = q_returns['R_EG'].iloc[i + iloc_offset_qFactor]
        stockObject_page4_qFactor['RF'].iloc[i] = q_returns['R_F'].iloc[i + iloc_offset_qFactor]
        stockObject_page4_qFactor['daily_ret'].iloc[i] -= q_returns['R_F'].iloc[i + iloc_offset_qFactor]
    # stockObject_qFactor.to_csv('stockObject.csv')
    x_qf = stockObject_page4_qFactor[['Mkt-RF', 'ME', 'IA', 'ROE', 'EG']].iloc[1:]
    y_qf = stockObject_page4_qFactor['daily_ret'].iloc[1:]
    x_qf = sm.add_constant(x_qf)
    Qf = lm.OLS(y_qf, x_qf).fit()
    print('q5 factors summary')
    print(Qf.summary())
    intercept_q5, beta_Mkt_RF_q5, beta_ME, beta_IA, beta_ROE, beta_EG = Qf.params
    stockObject_page4_qFactor.insert(stockObject_page4_qFactor.shape[1], 'qf_return', 0)
    stockObject_page4_qFactor['qf_return'] = intercept_q5 + stockObject_page4_qFactor['RF'] + beta_Mkt_RF_q5 * stockObject_page4_qFactor['Mkt-RF'] + beta_ME * stockObject_page4_qFactor['ME'] + beta_IA * stockObject_page4_qFactor['IA'] + beta_ROE * stockObject_page4_qFactor['ROE'] + beta_EG * stockObject_page4_qFactor['EG']

    #显示ff3、5和q5 收益率与真实收益率
    page4_fig1 = go.Figure(go.Scatter(
                    x = stockObject_page4.index,
                    y = stockObject_page4['daily_ret'],
                    name = 'Actual daily return'),layout=go.Layout(title=go.layout.Title(text=f'Comparison of Actual daily return, Fama French and q5 factor return of {RISKY_ASSET}'),
                                                             xaxis_title='Date', yaxis_title='Return Rate')
                          )
    page4_fig1.add_trace(go.Scatter(
                    x = stockObject_page4.index,
                    y = stockObject_page4['ff3fm_return'],
                    name = 'Fama French 3 factor model daily return')
                        )
    page4_fig1.add_trace(go.Scatter(
                    x = stockObject_page4.index,
                    y = stockObject_page4['ff5fm_return'],
                    name = 'Fama French 5 factor model daily return')
                        )
    page4_fig1.add_trace(go.Scatter(
                    x=stockObject_page4_qFactor.index,
                    y=stockObject_page4_qFactor['qf_return'],
                    name='Q5-factor model daily return')
                        )
    page4_fig2 = go.Figure(go.Bar(
                    x = ['beta_Mkt-RF', 'beta_SMB', 'beta_HML', 'alpha'],
                    y = [beta_Mkt_RF_3, beta_SMB_3, beta_HML_3, intercept3]),
                           layout=go.Layout(title=go.layout.Title(text=f'Beta value of coefficient of Fama French 3 factor of {RISKY_ASSET}'),
                                                             xaxis_title='Coefficient value of Fama French Factors', yaxis_title='Coefficient value')
                          )

    page4_fig3 = go.Figure(go.Bar(
                    x = ['beta_Mkt-RF', 'beta_SMB', 'beta_HML', 'beta_RMW', 'beta_CMA', 'alpha'],
                    y = [beta_Mkt_RF_5, beta_SMB_5, beta_HML_5, beta_RMW, beta_CMA, intercept5]),
                           layout=go.Layout(title=go.layout.Title(text=f'Beta value of coefficient of Fama French 5 factor of {RISKY_ASSET}'),
                                                             xaxis_title='Coefficient value of Fama French Factors', yaxis_title='Coefficient value')
                          )
    page4_fig4 = go.Figure(go.Bar(
                    x = ['beta_Mkt-RF', 'beta_ME', 'beta_IA', 'beta_ROE', 'beta_EG', 'alpha'],
                    y = [beta_Mkt_RF_q5, beta_ME, beta_IA, beta_ROE, beta_EG, intercept_q5]),
                           layout=go.Layout(title=go.layout.Title(text=f'Beta value of coefficient of q5 factor of {RISKY_ASSET}'),
                                                             xaxis_title='Coefficient value of q5 Factors', yaxis_title='Coefficient value')
                          )
    #plot the radar figure
    radar_df_ff5 = pd.DataFrame(dict(r=[beta_Mkt_RF_5, beta_SMB_5, beta_HML_5, beta_RMW, beta_CMA, intercept5],
                                     theta=['beta_Mkt-RF', 'beta_ME', 'beta_IA', 'beta_ROE', 'beta_EG', 'alpha']))
    page4_fig5 = px.line_polar(radar_df_ff5, r='r', theta='theta', line_close=True)
    page4_fig5.update_traces(fill='toself')
    page4_fig5.update_layout(title_text='radar chart of Fama French 5 factor coefficients')

    radar_df_q5 = pd.DataFrame(dict(r=[beta_Mkt_RF_q5, beta_ME, beta_IA, beta_ROE, beta_EG, intercept_q5],
                                     theta=['beta_Mkt-RF', 'beta_ME', 'beta_IA', 'beta_ROE', 'beta_EG', 'alpha']))
    page4_fig6 = px.line_polar(radar_df_q5, r='r', theta='theta', line_close=True)
    page4_fig6.update_traces(fill='toself')
    page4_fig6.update_layout(title_text='radar chart of q5 factor coefficients')

    return page4_fig1, page4_fig2, page4_fig3, page4_fig4, page4_fig5, page4_fig6


if __name__ == '__main__':
    app.run_server(port=8051)
# if __name__ == '__main__':
#     app.run_server(debug=True)