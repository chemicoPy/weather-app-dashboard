
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
import datetime
  

# Desiging & implementing changes to the standard streamlit UI/UX
st.set_page_config(page_icon="img/page_icon.png")    #Logo

st.title("Weather App Dashboard 🌧️🌥️")

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


st.subheader("Navigate to side bar to see full project info as well as options to choose from, to get started!")

def add_bg_from_url():

    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url(https://wallpaperaccess.com/full/1442216.jpg);
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()

def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

my_logo = add_logo(logo_path="img/icon.png", width=60, height=70)
st.sidebar.image(my_logo)

api=st.secrets["api_key"]
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
    states_list.insert(0, "State/Province")
    state_select = st.sidebar.selectbox(
            "State/Province",
            (states_list),)
    
    if state_select !="State/Province":
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
      graph=st.sidebar.radio("Select Graph Type ",["Bar Graph","Line Graph"])

      if unit=="Celsius":
        temp_unit=" °C"
      else:
        temp_unit=" °F"
    
      if speed=="Kilometre/hour":
        wind_unit=" km/h"
      else:
        wind_unit=" m/s"
    
           
  
      if(st.sidebar.button("Go!")):
          url=f"https://api.openweathermap.org/data/2.5/weather?q={city_select}&appid={api}"
          response=requests.get(url)
          x=response.json()  

          lon=x["coord"]["lon"]
          lat=x["coord"]["lat"]
          ex="current,minutely,hourly"
          url2=f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={ex}&appid={api}'
          res=requests.get(url2)
          y=res.json()

          maxtemp=[]
          mintemp=[]
          pres=[]
          humd=[]
          wspeed=[]
          desc=[]
          cloud=[]
          rain=[]
          dates=[]
          sunrise=[]
          sunset=[]
          all_uvi=[]
          cel=273.15 
    
          for item in y["daily"]:
            
              if unit=="Celsius":
                maxtemp.append(round(item["temp"]["max"]-cel,2))
                mintemp.append(round(item["temp"]["min"]-cel,2))
              else:
                maxtemp.append(round((((item["temp"]["max"]-cel)*1.8)+32),2))
                mintemp.append(round((((item["temp"]["min"]-cel)*1.8)+32),2))

              if wind_unit=="m/s":
                wspeed.append(str(round(item["wind_speed"],1))+wind_unit)
              else:
                wspeed.append(str(round(item["wind_speed"]*3.6,1))+wind_unit)

                pres.append(item["pressure"])
                humd.append(str(item["humidity"])+' %')
            
                cloud.append(str(item["clouds"])+' %')
                rain.append(str(int(item["pop"]*100))+'%')

                desc.append(item["weather"][0]["description"].title())
                
                
              pres.append(item["pressure"])
              humd.append(str(item["humidity"])+' %')
            
              cloud.append(str(item["clouds"])+' %')
              rain.append(str(int(item["pop"]*100))+'%')

              desc.append(item["weather"][0]["description"].title())

              
              d1=datetime.date.fromtimestamp(item["dt"])
              dates.append(d1.strftime('%d %b'))
            
              sunrise.append( datetime.datetime.utcfromtimestamp(item["sunrise"]).strftime('%H:%M'))
              sunset.append( datetime.datetime.utcfromtimestamp(item["sunset"]).strftime('%H:%M'))
              
              all_uvi.append(item["uvi"])
              
              #dates.append(item["dt"])
              #sunrise.append(item["sunrise"])
              #sunset.append(item["sunset"])
        
            
          
          def bargraph():
              fig=go.Figure(data=
                [
                go.Bar(name="Maximum",x=dates,y=maxtemp,marker_color='crimson'),
                go.Bar(name="Minimum",x=dates,y=mintemp,marker_color='navy')
                ])
              fig.update_layout(xaxis_title="Dates",yaxis_title="Temperature",barmode='group',margin=dict(l=70, r=10, t=80, b=80),font=dict(color="white"))
              st.plotly_chart(fig)
        
          def linegraph():
              fig = go.Figure()
              fig.add_trace(go.Scatter(x=dates, y=mintemp, name='Minimum '))
              fig.add_trace(go.Scatter(x=dates, y=maxtemp, name='Maximimum ',marker_color='crimson'))
              fig.update_layout(xaxis_title="Dates",yaxis_title="Temperature",font=dict(color="white"))
              st.plotly_chart(fig)
            
          icon=x["weather"][0]["icon"]
          current_weather=x["weather"][0]["description"].title()
        
          if unit=="Celsius":
              temp=str(round(x["main"]["temp"]-cel,2))
          else:
              temp=str(round((((x["main"]["temp"]-cel)*1.8)+32),2))
              
          #st.image(f"http://openweathermap.org/img/wn/{icon}@2x.png",width=70)
          placeholder = st.empty()
          
          with placeholder.container():
              col1, col2, col3 = st.columns(3)
              
              col1.metric(label="Current Temperature ",
                         value=temp+temp_unit)
              
              col2.metric(label="WEATHER",
                         value=current_weather)
              
              col3.metric(label="UVI",
                         value=all_uvi[0])
        
          st.subheader(" ")
        
          if graph=="Bar Graph":
              bargraph()
            
          elif graph=="Line Graph":
              linegraph()

         
          table1=go.Figure(data=[go.Table(header=dict(
                  values = [
                  '<b>DATES</b>',
                  '<b>MAX TEMP<br>(in'+temp_unit+')</b>',
                  '<b>MIN TEMP<br>(in'+temp_unit+')</b>',
                  '<b>CHANCES OF RAIN</b>',
                  '<b>CLOUD COVERAGE</b>',
                  '<b>HUMIDITY</b>', '<b>UVI<br>(UV Index)</b>'],
                  line_color='black', fill_color='royalblue',  font=dict(color='black', size=14),height=32),
            cells=dict(values=[dates,maxtemp,mintemp,rain,cloud,humd, all_uvi],
        line_color='black',fill_color=['paleturquoise',['palegreen', '#fdbe72']*7], font_size=14,height=32
            ))])

          table1.update_layout(margin=dict(l=10,r=10,b=10,t=10),height=328)
          st.write(table1)
        
          table2=go.Figure(data=[go.Table(columnwidth=[1,2,1,1,1,1],header=dict(values=['<b>DATES</b>','<b>WEATHER CONDITION</b>','<b>WIND SPEED</b>','<b>PRESSURE<br>(in hPa)</b>','<b>SUNRISE<br>(in UTC)</b>','<b>SUNSET<br>(in UTC)</b>', '<b>UVI<br>(UV Index)</b>']
                  ,line_color='black', fill_color='royalblue',  font=dict(color='black', size=14),height=36),
        cells=dict(values=[dates,desc,wspeed,pres,sunrise,sunset, all_uvi],
        line_color='black',fill_color=['paleturquoise',['palegreen', '#fdbe72']*7], font_size=14,height=36))])
        
          table2.update_layout(margin=dict(l=10,r=10,b=10,t=10),height=360)
          st.write(table2)
 
           
    
    
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

  
