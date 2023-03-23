import functools
import json
import requests
import click

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('stock_data', __name__, url_prefix='/api/stockData')


@bp.route('/getPrice', methods=['POST'])
def get_stock_price():
    pass

@bp.route('/getData', methods=['POST'])
def get_stock_data():
    print("Get stock data")

    #FIXME: Temp API key
    av_api_key = "K46UF72V6O1K064L"
    click.echo(request.form)
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


