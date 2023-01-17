
import streamlit as st
import time
import requests
import pandas as pd
import numpy as np
import re
import string
import os
import json
import streamlit.components.v1 as components
from io import BytesIO
from time import sleep
import math

from numpy import *
import json
from pandas import DataFrame, Series
from numpy.random import randn

import io
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from streamlit_extras.app_logo import add_logo
import ccxt,pytz,time,schedule, requests
from datetime import datetime, timedelta, date
import pandas_ta as ta
import plotly.graph_objects as go
import plotly.express as px
from pprint import pprint
import statsmodels.regression.linear_model as rg
  

# Desiging & implementing changes to the standard streamlit UI/UX
st.set_page_config(page_icon="img/page_icon.png")    #Logo
st.markdown('''<style>.css-1egvi7u {margin-top: -4rem;}</style>''',
    unsafe_allow_html=True)
# Design change hyperlink href link color
st.markdown('''<style>.css-znku1x a {color: #9d03fc;}</style>''',
    unsafe_allow_html=True)  # darkmode
st.markdown('''<style>.css-znku1x a {color: #9d03fc;}</style>''',
    unsafe_allow_html=True)  # lightmode
# Design change height of text input fields headers
st.markdown('''<style>.css-qrbaxs {min-height: 0.0rem;}</style>''',
    unsafe_allow_html=True)
# Design change spinner color to primary color
st.markdown('''<style>.stSpinner > div > div {border-top-color: #9d03fc;}</style>''',
    unsafe_allow_html=True)
# Design change min height of text input box
st.markdown('''<style>.css-15tx938{min-height: 0.0rem;}</style>''',
    unsafe_allow_html=True)

# Design hide top header line
hide_decoration_bar_style = '''<style>header {visibility: hidden;}</style>'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
# Design hide "made with streamlit" footer menu area
hide_streamlit_footer = """<style>#MainMenu {visibility: hidden;}
                        footer {visibility: hidden;}</style>"""
st.markdown(hide_streamlit_footer, unsafe_allow_html=True)

# disable warnings
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_option('deprecation.showfileUploaderEncoding', False)

st.title('Weather App dashboard')
st.subheader("Navigate to side bar to see full project info as well as options to choose from, to get started!")

  
from forex_python.converter import CurrencyRates
from forex_python.converter import CurrencyCodes

class CurrencyConverter:
    def __init__(self, YOUR_APP_ID, symbols):
            self.YOUR_APP_ID = "5b709615dfbf4532bb3296a5ea23c7c6"
            self.symbols = symbols
            self._symbols = ",".join([str(s) for s in symbols])

            r = requests.get(
                "https://openexchangerates.org/api/latest.json",
                params = {
                    "app_id" : self.YOUR_APP_ID,
                    "symbols" : self._symbols,
                    "show_alternatives": True
                        }
                )
            self.rates_ = r.json()["rates"]
            self.rates_["USD"] = 1

    def convert(self, value, symbol_from, symbol_to):
        try:
            return value * 1/self.rates_.get(symbol_from) * self.rates_.get(symbol_to)
        except TypeError:
            print("Error")
            return None

YOUR_APP_ID = "5b709615dfbf4532bb3296a5ea23c7c6"
simpleConverter = CurrencyConverter(YOUR_APP_ID, ["MATIC" , "XAU","BTC","ETH","DOGE", "GBP", 
             "EUR", "NZD", "USD", "NPR", "BTC", "JPY","BGN","CZK","DKK","GBP","HUF","PLN","RON","SEK", 
                                                  "CHF","ISK","NOK","TRY","AUD","BRL","CAD","CNY","HKD","IDR","ILS",
                                                  "INR","KRW","MXN","MYR","PHP","SGD", "THB", "ZAR"])



c = CurrencyRates()
    
def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://github.com/chemicoPy/weather-app-dashboard/blob/main/img/page_icon.png);
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "My Company Name";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

add_logo()

  
    # ------ layout setting---------------------------
st.sidebar.markdown(
            """
    ## Project Overview
    Crypto Converter is an app that converts crypto coin price to a local currency price. You can check price on a visualization board as well when you select the option and hit on the button.
    
    Get started already!""")    

  
st.sidebar.markdown("## Select Crypto pair & Interval below") # add a title to the sidebar container

from_conv = st.sidebar.selectbox(
            "Convert From",
            ("GBP", 
"EUR", "NZD", "USD", "NPR","JPY","BGN","CZK","DKK","GBP","HUF","PLN","RON","SEK", 
              "CHF","ISK","NOK","TRY","AUD","BRL","CAD","CNY","HKD","IDR","ILS",
               "INR","KRW","MXN","MYR","PHP","SGD", "THB", "ZAR"),)

to_conv = st.sidebar.selectbox(
            "Convert To",
            ("GBP", 
             "EUR", "NZD", "USD", "NPR", "JPY","BGN","CZK","DKK","GBP","HUF","PLN","RON","SEK", 
                                                  "CHF","ISK","NOK","TRY","AUD","BRL","CAD","CNY","HKD","IDR","ILS", "INR","KRW","MXN","MYR","PHP","SGD", "THB", "ZAR"),)
    
price = st.sidebar.number_input("Enter price to convert")

st.sidebar.write("Converted price = ", simpleConverter.convert(price, str(from_conv), str(to_conv)))
#st.write("Converted price= ", (c.get_symbol(to_conv), simpleConverter.convert(price, from_conv, to_conv)) 

    # ---------------forex pair selection------------------
  
st.write("\n")  # add spacing   

st.sidebar.markdown("## Visualization")    
instrument = st.sidebar.selectbox(
        '', ["Select Forex Pair of interest", "MATIC/USDT" , "XAU/USDT","BTC/USDT","ETH/USDT",
             "DOGE/USDT", "BNB/USDT", "USD/USDT", "XRP/USDT", "SOL/USDT", "TRX/USDT", "LTC/USDT", "SHIB/USDT"], index=0)
Tframe = st.sidebar.selectbox(
        '', ["Interval of interest", "1m","5m","15m","30m","1h","2h","4h","1d","1w","month"], index=0)

if st.sidebar.button("Show Viz!"):
  lim = 1000
  bybit = ccxt.bybit()

  if instrument=="Select Forex Pair of interest" and Tframe=="Interval of interest":
    st.write("Kindly navigate to sidebar to see more options...")

  else:
    klines = bybit.fetch_ohlcv(instrument, timeframe=Tframe, limit= lim, since=None)

    from datetime import datetime, timedelta
    one_month_ago = datetime.now() - timedelta(days=30)
    filtered_klines = [kline for kline in klines if datetime.fromtimestamp(kline[0]/1000) >= one_month_ago]
    
# convert the klines list to a DataFrame
    df = pd.DataFrame(filtered_klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

# convert the timestamp column to a datetime type
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# set the timestamp column as the index
    df.set_index('timestamp', inplace=True)


# calculate RSI
    df['rsi'] = ta.rsi(df['close'])

# calculate Stochastics
    stoch_data = df.copy()

#df['stoch_k'], df['stoch_d'] = ta.stoch(df['high'], df['low'], df['close'])
#New calculation for Stochastic
    stoch_data['high'] = stoch_data['high'].rolling(14).max()
    stoch_data['low'] = stoch_data['low'].rolling(14).min()
    stoch_data['%k'] = (stoch_data["close"] - stoch_data['low'])*100/(stoch_data['high'] - stoch_data['low'])
    stoch_data['%d'] = stoch_data['%k'].rolling(3).mean()
    df['stoch_data'] = stoch_data['%d']


# Candlestick plot

    data = [go.Candlestick(x=df.index,
                       open=df.open,
                       high=df.high,
                       low=df.low,
                       close=df.close)]

    layout = go.Layout(title= f'{instrument} in {Tframe} Candlestick with Range Slider',
                   xaxis={'rangeslider':{'visible':True}})
    fig = go.Figure(data=data,layout=layout)
    plt.show()
    st.write(fig)

    
    import plotly.graph_objs as go

# create a line chart using the close data
    line = go.Scatter(
        x=df.index,
        y=df['close'],
        name='Close',
        line=dict(color='#17BECF')
)

# create the layout for the chart
    layout = go.Layout(
        title= f'{instrument} in {Tframe} Kline Data',
    xaxis=dict(
        title='Time',
        rangeslider=dict(visible=True)
    ),
    yaxis=dict(
        title='Price (USDT)'
    )
)

# create the figure and plot the chart
    fig = go.Figure(data=[line], layout=layout)
    plt.show()
    st.write(fig)

    import plotly.express as px

# create the line chart
    fig = px.line(df, x=df.index, y=df['rsi'], title=f'{instrument} in {Tframe} Kline Data')

# add the red and green lines
    fig.add_shape(
    type='line',
    x0=df.index[0],
    x1=df.index[-1],
    y0=75,
    y1=75,
    yref='y',
    line=dict(color='red', dash='dot')
)
        
    fig.add_shape(
    type='line',
    x0=df.index[0],
    x1=df.index[-1],
    y0=25,
    y1=25,
    yref='y',
    line=dict(color='green', dash='dot')
)

# set the y-axis range to include 0 and 100
    fig.update_layout(yaxis=dict(range=[0, 100]))

    plt.show()
    st.write(fig)

    st.write(df)
    
st.sidebar.markdown(

    """
    -----------
    # Other Apps
 
    1. [Weather App](https://www.movavi.com/support/how-to/how-to-convert-music-to-wav.html)
    2. [Immigration Dashboard](https://www.movavi.com/support/how-to/how-to-convert-music-to-wav.html)
    3. [Crime Dashboard](https://www.movavi.com/support/how-to/how-to-convert-music-to-wav.html)
    """)
    
    
st.sidebar.markdown(

    """
    -----------
    # Let's connect
 
    [![Victor Ogunjobi](https://img.shields.io/badge/Author-@VictorOgunjobi-gray.svg?colorA=gray&colorB=dodgergreen&logo=github)](https://www.github.com/chemicopy)
    [![Victor Ogunjobi](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logoColor=white)](https://www.linkedin.com/in/victor-ogunjobi-a761561a5/)
    [![Victor Ogunjobi](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=gray)](https://twitter.com/chemicopy_)
    """)



   
