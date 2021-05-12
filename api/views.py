from django.shortcuts import render
from django.http import HttpResponse
import requests
import json 

from rest_framework.views import APIView 
from rest_framework import status 

from rest_framework import permissions 
from .models import InteractiveModels

from .serializers import InteractiveSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import FileResponse
import sweetviz
from pandas_profiling import ProfileReport
import plotly
import plotly.express as px

import math
import numpy as np 
import pandas as pd
import yfinance as yf
from plotly.offline import plot 
import seaborn as sns
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import LSTM, Dense
import matplotlib  
matplotlib.use('Agg')
import io
import urllib, base64





class InteractiveGraphAPIView(APIView):
    serializer_class =  InteractiveSerializer 


    def post(self , request , format = None):
    
        input_stock_ticker = request.data.get('companycode')
        data_stocks = yf.Ticker(input_stock_ticker)
        data_fetch = data_stocks.history(period='1d', interval='1m')
        raw_data = pd.DataFrame(data=data_fetch)
        raw_data = raw_data.drop(['Dividends','Stock Splits'], axis=1)
        #raw_data.to_csv(r'D:\Internship - LSCG\Stocks_Data\All Stocks.csv')
        data = raw_data.drop(['High','Low','Open','Volume'], axis=1)
        data.to_csv(r'D__\Internship - LSCG\Stocks_Data\Closing Stocks.csv',header=False)

        data = pd.read_csv(r'D__\Internship - LSCG\Stocks_Data\Closing Stocks.csv')
        data.columns = ['Datetime',input_stock_ticker]
        data.to_csv(r'D__\Internship - LSCG\Stocks_Data\Closing Stocks.csv',index=None)
        data_plot = pd.read_csv(r'D__\Internship - LSCG\Stocks_Data\Closing Stocks.csv')
        data_plot.plot(x='Datetime',y=[input_stock_ticker],style='-')
        data_plot.head()

        plt.title('Relative price change')
        plt.legend(loc='upper left', fontsize=12)
        plt.xticks(rotation=35)
        plt.tight_layout()
        plt.grid(True)
        fig = px.line(data_plot,x=data_plot['Datetime'],y=[input_stock_ticker],title='Interactive Stocks')
        fig.update_layout(template='plotly_dark')
        
        plt_div = plot(fig, output_type='div')
        return Response(plt_div)