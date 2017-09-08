# -*- coding: utf-8 -*-
"""
Created on Wed Sep 06 15:35:55 2017

@author: Hualong
"""

from flask import Flask, render_template, request, redirect
import numpy as np
import pandas as pd
from bokeh.plotting import figure, save
import datetime
import quandl

my_app_lulu = Flask(__name__)

my_app_lulu.prices = []

def create_plot(stock, prices):
    quandl.ApiConfig.api_key = "yseKufW_TvSK1q3xkaus"
    df = quandl.get('WIKI/' + stock, start_date = '2017-08-01')
    stock_dates = np.array(df.index, dtype = np.datetime64)
    current = np.datetime64(datetime.datetime.today())
    one_month_ago = current - np.timedelta64(31, 'D')
    mask = (stock_dates > one_month_ago) & (stock_dates <= current)
    stock_dates = stock_dates[mask]
    
    p = figure(width = 1200, height = 500, x_axis_type = 'datetime')
    p.title.text = 'Stock price for ' + stock + ' over last month'
    p.legend.location= 'top_left'
    p.grid.grid_line_alpha = 0
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    p.ygrid.band_fill_color = 'olive'
    p.ygrid.band_fill_alpha = 0.1
    
    if 'close' in prices:
        closing_prices = np.array(df['Close'])[mask]
        p.line(stock_dates, closing_prices, color = 'darkblue', legend = 'Closing')
    
    if 'adj_close' in prices:
        adj_closing_prices = np.array(df['Adj. Close'])[mask]
        p.line(stock_dates, adj_closing_prices, color = 'crimson', legend = 'Adjusted closing')
    
    if 'open' in prices:
        opening_prices = np.array(df['Open'])[mask]
        p.line(stock_dates, opening_prices, color = 'purple', legend = 'Opening')
    
    if 'adj_open' in prices:
        adj_opening_prices = np.array(df['Adj. Open'])[mask]
        p.line(stock_dates, adj_opening_prices, color = 'limegreen', legend = 'Adjusted opening')
    
    save(p, filename = 'templates/stocks3.html', title='Stock price test')
    return

@my_app_lulu.route('/index_lulu', methods = ['GET', 'POST'])
def index_lulu():
    if request.method == 'GET':
        return render_template('price_choices.html')
    else :
        my_app_lulu.prices = request.form.getlist('prices')
        stock = request.form['ticker']
        create_plot(stock, my_app_lulu.prices)
        return render_template('stocks3.html')

if __name__ == '__main__':
    my_app_lulu.run(host = '0.0.0.0')
