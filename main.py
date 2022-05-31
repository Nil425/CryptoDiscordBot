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

API_KEY = 'PK5WY4MNLUVP77YF5XWR'
SECRET_KEY = 'pCF2WMotwJqhaOh9smGxcydGHerLfKk1e0CNpDgx'
rest_api = REST(API_KEY, SECRET_KEY, 'https://paper-api.alpaca.markets')


import os
import discord
import discord.ext
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check

TOKEN = 'OTQzMDg0MDIyMzYyNDM1NTg0.Ygt5cA.u01CL06HpgjF9PlF092zN3frJRg'

intents = discord.Intents.default()

client = discord.Client(Intents = intents)
client = commands.Bot(command_prefix = '!', case_insensitive=True) 

#to get the console to tell you when the bot is ready to use

def convertPlot(arg1):
  # retrieve daily bar data for SPY in a dataframe 
  d = datetime.today() - timedelta(days=180)
  d2 = datetime.today() - timedelta(days=2)
  dstr = d.strftime("20%y-%m-%d")
  d2str = d2.strftime("20%y-%m-%d")
  stock_bars = rest_api.get_bars(arg1, TimeFrame.Day, dstr, d2str).df
  
  df_sma20 = stock_bars.ta.ema(length=20)
  df_sma50 = stock_bars.ta.sma(length=50)
  df_sma80 = stock_bars.ta.sma(length=80)
  
  df_hma20 = stock_bars.ta.hma(length=20)
  df_hma50 = stock_bars.ta.hma(length=50)
  
  df_bbL20 = stock_bars.ta.accbands(length=20)

  df_macd = stock_bars.ta.macd()
  df_rsi = stock_bars.ta.rsi()
  
  
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
  
  fig, bx = plt.subplots()
  title = arg1 + ' Momentum'
  plt.title(title)
  bx.plot(df_macd, 'aquamarine', label="macd")
  bx.legend(loc="upper left")

  plt.savefig("output2.png") 
  
  fig, cx =  plt.subplots()
  title2 = arg1 + ' Relative Strength'
  plt.title(title2)
  cx.plot(df_rsi, 'salmon', label="RSI")
  cx.legend(loc="upper left")

  plt.savefig("output3.png") 




@client.event
async def on_ready():
	print('TA Plotter is ready')

@client.command()
async def GenPlot(ctx, ticker): 
  convertPlot(ticker)
  #await bot.send_file(ctx.message.channel, f['output.png'], f['output2.png'], f['output3.png'])
  #await ctx.send(file=discord.File('output.png'))
  await ctx.send(file=discord.File['output.png'], file1=discord.File['output2.png'], file2=discord.File['output3.png'])
  
                 

@client.command()
async def OrderByQuantity(ctx, ticker, qty): 
  rest_api.post_order(ticker, qty, null, buy, market)
  #await ctx.send('

@client.command()
async def OrderByPrice(ctx, ticker, price): 
  rest_api.post_order(ticker, price, type: buy, market)
  #await ctx.send('




client.run(TOKEN)
