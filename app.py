
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
from PIL import Image
from geosky import geo_plug
from countryinfo import CountryInfo
  

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


def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

my_logo = add_logo(logo_path="img/icon.png", width=60, height=70)
st.sidebar.image(my_logo)

API_KEY = "06a0159059dc1c945b62591f03bbf59d"
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"
  
  
    # ------ layout setting---------------------------
st.sidebar.markdown(
            """
    ## Project Overview
    Weather App dashboard is an app that...
    Get started already!""")    

  
st.sidebar.markdown("## Select Country & City from below options") # add a title to the sidebar container

countries = geo_plug.all_CountryNames()
countries.insert(0, "Country")
countries_list = list(countries)

country_select = st.sidebar.selectbox(
            "Country",
            (countries_list),)

if country_select !="Country":
    states = CountryInfo(country_select)
    states_list = states.provinces()
    states_list.insert(0, "State")
    state_select = st.sidebar.selectbox(
            "State",
            (states_list),)
    
    if state_select !="State":
      city = geo_plug.all_State_CityNames(state_select)
      cities = []
      for key,values in eval(city)[0].items():
        cities.append(values)
        #cities[0]
      cities_list = cities[0]
      cities_list.insert(0, "City")
      city_select = st.sidebar.selectbox(
            "City",
            (cities_list),)
    
#st.sidebar.write("Converted price = ", simpleConverter.convert(price, str(from_conv), str(to_conv)))

unit=st.sidebar.radio("Select Temperature Unit ",["Celsius","Fahrenheit"])
speed=st.sidebar.radio("Select Wind Speed Unit ",["Metre/sec","Kilometre/hour"])

if unit=="Celsius":
    temp_unit=" °C"
else:
    temp_unit=" °F"
    
if speed=="Kilometre/hour":
    wind_unit=" km/h"
else:
    wind_unit=" m/s"
    
  
st.write("\n")  # add spacing  

st.sidebar.markdown(

    """
    -----------
    # Other Apps
 
    1. [Crypto Converter Dashboard](https://chemicopy-crypto-conv-dashboard-app-10tiqj.streamlit.app/)
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

  
if(st.button("Go!")):
    st.write("Done!")
