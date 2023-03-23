import functools
import json
import requests
import pandas as pd
import click


from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

from .six_api import FinancialDataAPI

bp = Blueprint('playground', __name__, url_prefix='/api/playground')


@bp.route('/getData', methods=['POST'])
def get_playground_data():
    click.echo("Getting wallet data")

    username=request.form['username']

    db = get_db()
    c = db.cursor()
    c.execute('SELECT * FROM wallet WHERE author_id = (SELECT id FROM user WHERE username = ?)', (username,))
    rows = c.fetchall()
    if rows:
        wallet_list = []
        for row in rows:
            wallet_dict = {'id': row[0], 'ticker_symbol': row[1], 'value_bought': row[2], 'volume_bought': row[3]}
            wallet_list.append(wallet_dict)

        return jsonify(wallet_list)
    else:
        return 'No wallets found for user {}'.format(username)




@bp.route('/modifyWallet', methods=['POST'])
def create_wallet():
    click.echo("Creating wallet")
    # data = request.get_json()
    username = request.form['username']
    # ticker_symbol = data['ticker_symbol']
    # value_bought = data['value_bought']
    # volume_bought = data['volume_bought']
    ticker_symbol = "GOOG"
    value_bought = 100
    volume_bought = -10

    # conn = get_db()
    # cur = conn.cursor()
    # cur.execute('select id from user where username = ?', (username,))
    # user_id = cur.fetchone()

    # if user_id:
    #     cur.execute('select * from wallet where author_id = ?', (user_id[0],))
    #     existing_wallet = cur.fetchone()

    #     # if existing_wallet:
    #     #     conn.close()
    #     #     return 'wallet already exists for user {}'.format(username), 400
    #     click.echo("appending wallet data for user id: "+ str(user_id[0]))
    #     cur.execute('insert into wallet (ticker_symbol, value_bought, volume_bought, author_id) values (?, ?, ?, ?)', (ticker_symbol, value_bought, volume_bought, user_id[0]))
    #     conn.commit()
    #     conn.close()
    #     return 'data added for user {}'.format(username), 201
    # else:
    #     conn.close()
    #     return 'user {} does not exist'.format(username), 400
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id FROM user WHERE username=?", (username,))
    user_id = c.fetchone()[0]
    c.execute("SELECT * FROM wallet WHERE author_id=? AND ticker_symbol=?", (user_id, ticker_symbol))
    row = c.fetchone()
    if row:
        # If a row already exists for the user and ticker symbol, update it
        new_value = row[3] + value_bought
        new_volume = row[4] + volume_bought
        if(new_volume <0):
            #bad request
            return json.dumps({'error': 'total volume cannot be < 0','status':400})
        c.execute("UPDATE wallet SET value_bought=?, volume_bought=? WHERE id=?", (new_value, new_volume, row[0]))
    else:
        # If no row exists for the user and ticker symbol, add a new one
        c.execute("INSERT INTO wallet (author_id, ticker_symbol, value_bought, volume_bought) VALUES (?, ?, ?, ?)", (user_id, ticker_symbol, value_bought, volume_bought))
    conn.commit()
    conn.close()

    return "updated wallet info"