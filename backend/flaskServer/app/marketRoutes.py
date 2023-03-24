import functools
import json
import requests
import pandas as pd
import click


from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

from .six_api import FinancialDataAPI

bp = Blueprint('stock_data', __name__, url_prefix='/api/stockData')


# @bp.route('/getPrice', methods=['POST'])
# def get_stock_price():

#     findata = FinancialDataAPI()

#     ticker_symbol = request.form.get('ticker_symbol')
#     start_date = request.form.get('start_date')

#     # six_url = '"TICKER_BC", ["{}"], "{}"'.format(ticker_symbol, start_date)
#     # click.echo(six_url)
#     # print(ticker_symbol)
#     symbol_list = []
#     symbol_list.append(ticker_symbol)
#     click.echo(ticker_symbol)
#     click.echo(symbol_list)
#     click.echo(type(start_date))
#     data = findata.listing_EoDTimeseries("TICKER_BC",symbol_list,str(start_date)) #"TICKER_BC", ["AAPL_67"], "2023-02-17", "2023-02-20"
#     ts_df = pd.json_normalize(data['data']['listings'][0]['marketData']['eodTimeseries'])
#     high_std = ts_df[['high']].std() 
#     # r = requests.get(six_url)
#     # data = r.json()
#     click.echo(high_std)
#     return json.dumps({"priceList":[],"datesList":[],"std":high_std.to_list()})

@bp.route('/getPrice', methods=['POST'])
def get_stock_price():

    findata = FinancialDataAPI()

    ticker_symbol = request.form.get('ticker_symbol')
    start_date = request.form.get('start_date')

    # six_url = '"TICKER_BC", ["{}"], "{}"'.format(ticker_symbol, start_date)
    # click.echo(six_url)
    # print(ticker_symbol)
    symbol_list = []
    symbol_list.append(ticker_symbol)
    click.echo(ticker_symbol)
    click.echo(symbol_list)
    click.echo(type(start_date))
    data = findata.listing_EoDTimeseries("TICKER_BC",symbol_list,str(start_date)) #"TICKER_BC", ["AAPL_67"], "2023-02-17", "2023-02-20"
    ts_df = pd.json_normalize(data['data']['listings'][0]['marketData']['eodTimeseries'])
    # high_std = ts_df[['opening']] 
    high_std = ts_df[['high']].std()
    # r = requests.get(six_url)
    # data = r.json()
    click.echo(high_std)
    return json.dumps({"priceList":[],"datesList":[],"std":high_std.to_list()})

@bp.route('/getData', methods=['POST'])
def get_stock_data():
    print("Get stock data")

    #FIXME: Temp API key
    av_api_key = "K46UF72V6O1K064L"
    ticker_symbol = request.form.get('ticker_symbol')

    #Get current price information from SIX API
    six_url = ""
    click.echo(six_url)

    #Get financial statatements from AV API
    va_url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol={}&apikey={}'.format(ticker_symbol, av_api_key)
    click.echo(va_url)
    r = requests.get(va_url)
    data = r.json()
    click.echo(data)

    returnObj = {}
    returnObj["status"] = ""
    returnObj["description"] = ""
    returnObj["pe_ratio"] = 0 #price to earnings ratio
    returnObj["fwd_pe_ratio"] = 0
    returnObj["trail_pe_ratio"] = 0
    returnObj["eps"] = 0 #earnings per share
    returnObj["div_yield"] = 0 #divident yield
    returnObj["market_cap"] = 0
    returnObj["q_earn_growth"] = 0 #YoY
    returnObj["q_rev_growth"] = 0 #YoY
    if data:
        #not empty result from VA
        returnObj["status"] = "success"
        returnObj["description"] = data['Description']
        returnObj["pe_ratio"] = data['PERatio']
        returnObj["fwd_pe_ratio"] = data['ForwardPE']
        returnObj["trail_pe_ratio"] = data['TrailingPE']
        returnObj["eps"] = data['EPS']
        returnObj["div_yield"] = data["DividendYield"]
        returnObj["market_cap"] = data["MarketCapitalization"]
        returnObj["q_earn_growth"] = data["QuarterlyEarningsGrowthYOY"]
        returnObj["q_rev_growth"] = data["QuarterlyRevenueGrowthYOY"]

        #define parameters (valuation, growth, dividents, risk)
        
    else:
        returnObj["status"] = "fail"


    #Calculate fundamental indicators based on SIX API and AV API data

    return json.dumps(returnObj)


