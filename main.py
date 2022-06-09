#SETUP
import pip
import asyncio
pip.main(['install', 'alpaca_trade_api'])
pip.main(['install', 'backtrader'])
pip.main(['install', 'matplotlib'])
pip.main(['install', 'plotly'])
pip.main(['install', 'talib-binary'])
pip.main(['install', 'pandas_ta'])

from alpaca_trade_api.rest import REST, TimeFrame
from alpaca_trade_api.stream import Stream

import pandas as pd
import pandas_ta as ta
from matplotlib import pyplot as plt
import matplotlib.colors 
from datetime import date
from datetime import datetime, timedelta

API_KEY = '***'
SECRET_KEY = '***'
rest_api = REST(API_KEY, SECRET_KEY, 'https://paper-api.alpaca.markets')


import os
import discord
import discord.ext
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check

TOKEN = '***'

intents = discord.Intents.default()

client = discord.Client(Intents = intents)
client = commands.Bot(command_prefix = '!', case_insensitive=True) 


#to get the console to tell you when the bot is ready to use
@client.event
async def on_ready():
    print('TA Plotter is ready')


def retrieve_data(arg1):
    # retrieve daily bar data for SPY in a dataframe
    d = datetime.today() - timedelta(days=180)
    d2 = datetime.today() - timedelta(days=2)
    dstr = d.strftime("20%y-%m-%d")
    d2str = d2.strftime("20%y-%m-%d")
    return rest_api.get_bars(arg1, TimeFrame.Day, dstr, d2str).df


#METHODS GENERRATING THE VARIOUS TECHNICAL PLOTS

def gen_moving_averages(arg1):
    stock_bars = retrieve_data(arg1)

    df_sma20 = stock_bars.ta.ema(length=20)
    df_sma50 = stock_bars.ta.sma(length=50)
    df_sma80 = stock_bars.ta.sma(length=80)

    df_hma20 = stock_bars.ta.hma(length=20)
    df_hma50 = stock_bars.ta.hma(length=50)

    df_bbL20 = stock_bars.ta.accbands(length=20)

    fig, ax = plt.subplots()
    plt.title(arg1.upper())

    ax.plot(stock_bars["close"], '-k')
    ax.plot(df_sma20, 'lightsteelblue', label="sma20")
    ax.plot(df_sma50, 'royalblue', label="sma50")
    ax.plot(df_sma80, 'violet', label="sma80")
    ax.plot(df_hma20, 'wheat', label="hma20")
    ax.plot(df_hma50, 'lightcoral', label="hma50")
    ax.plot(df_bbL20, 'rosybrown', label="BB20")
    ax.legend(loc="upper left")

    plt.savefig("output.png")


def gen_momentum(arg1):
    stock_bars = retrieve_data(arg1)

    df_macd = stock_bars.ta.macd()

    fig, bx = plt.subplots()
    title = arg1 + ' Momentum'
    plt.title(title)
    bx.plot(df_macd, 'aquamarine', label="macd")
    bx.legend(loc="upper left")

    plt.savefig("output2.png")


def gen_rsi(arg1):
    stock_bars = retrieve_data(arg1)

    df_rsi = stock_bars.ta.rsi()

    fig, cx = plt.subplots()
    title2 = arg1 + ' Relative Strength'
    plt.title(title2)
    cx.plot(df_rsi, 'salmon', label="RSI")
    cx.legend(loc="upper left")

    plt.savefig("output3.png")


#COMMANDS TO INVOKE VARIOUS TECHNICAL PLOTS


@client.command()
async def show_moving_averages(ctx, ticker):
    gen_moving_averages(ticker)
    #await bot.send_file(ctx.message.channel, f['output.png'], f['output2.png'], f['output3.png'])
    await ctx.send(file=discord.File('output.png'))
    #await ctx.send(file=discord.File['output.png'], file1=discord.File['output2.png'], file2=discord.File['output3.png'])


@client.command()
async def show_momentum(ctx, ticker):
    gen_momentum(ticker)
    await ctx.send(file=discord.File('output2.png'))


@client.command()
async def show_rsi(ctx, ticker):
    gen_rsi(ticker)
    await ctx.send(file=discord.File('output3.png'))


#COMMANDS TO PLACE ORDERS

@client.command()
async def market_buy_by_quantity(ctx, ticker, qty):
    rest_api.submit_order(symbol=ticker,
                          qty=qty,
                          type="market",
                          side="buy",
                          time_in_force="day")


@client.command()
async def market_buy_by_price(ctx, ticker, price):
    rest_api.submit_order(symbol=ticker,
                          notional=price,
                          type="market",
                          side="buy",
                          time_in_force="day")

@client.command()
async def limit_buy_by_quantity(ctx, ticker, qty, limitprice):
    rest_api.submit_order(symbol=ticker,
                          qty=qty,
                          type="limit",
                          side="buy",
                          time_in_force="day",
                          limit_price = limitprice)
  
@client.command()
async def limit_buy_by_price(ctx, ticker, price, limitprice):
    rest_api.submit_order(symbol=ticker,
                          notional=price,
                          type="limit",
                          side="buy",
                          time_in_force="day",
                          limit_price = limitprice)

@client.command()
async def sell_by_price(ctx, ticker, price):
    rest_api.submit_order(symbol=ticker,
                          notional=price,
                          type="market",
                          side="sell",
                          time_in_force="day")

  
@client.command()
async def sell_by_quantity(ctx, ticker, qty):
    rest_api.submit_order(symbol=ticker,
                          qty=qty,
                          type="market",
                          side="sell",
                          time_in_force="day")


@client.command()
async def limit_sell_by_quantity(ctx, ticker, qty, limitprice):
    rest_api.submit_order(symbol=ticker,
                          qty=qty,
                          type="limit",
                          side="sell",
                          time_in_force="day",
                          limit_price = limitprice)
  
@client.command()
async def limit_sell_by_price(ctx, ticker, price, limitprice):
    rest_api.submit_order(symbol=ticker,
                          notional=price,
                          type="limit",
                          side="sell",
                          time_in_force="day",
                          limit_price = limitprice)


client.run(TOKEN)
