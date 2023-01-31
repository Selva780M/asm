from pya3 import *
import streamlit as st
from datetime import datetime, timedelta
from pytz import timezone 
import time
day = datetime.now(timezone("Asia/Kolkata"))
#day = day.strftime('%Y-%m-%d %H:%M:%S')
alice = Aliceblue(user_id='627742',api_key='BPk1mFAXB9ByTFFQnm87HhieLFo3Fy5J3PCaae2g252DiLCNB9BK7hF0LpSg3d9fNO698r32IAsEt0lWm3hmuZMWW9tJC6r6A7xGkZWGmY1Hcdys1q9ITC1pRjYaklRQ')
alice.get_session_id()
# exchange = "NFO"
# symbol = "NIFTY"
# st.write(day)
# ticker = ["NIFTY 50","NIFTY BANK"]
# def main():
#        try:
#               for i in ticker:
#                      m = alice.get_scrip_info(alice.get_instrument_by_symbol('INDICES',i))
#                      st.write(f"{i} : {m['LTP']} Change: {m['Change']} % {m['PerChange']}")
#        except Exception as e:              
#               st.write(f"Error",{e})       

import pandas as pd

instrument = alice.get_instrument_by_symbol("NSE","SBIN")
from_datetime = day - timedelta(days=5)
to_datetime = day 
interval = "1" 
indices = False
df = pd.DataFrame(alice.get_historical(instrument,from_datetime,to_datetime,interval,indices))  
df = df.set_index(pd.DatetimeIndex(df['datetime']))
df = df.groupby(pd.Grouper(freq='5Min')).agg({"open":"first","high":"max","low":"min","close":"last","volume":'sum'})
df.dropna(inplace=True)
data = df

st.dataframe(df)

# Create a function that implements your trading strategy
def trading_strategy(data):
    # Example strategy: buy when the 50-day moving average crosses above the 200-day moving average
    data['50_day_ma'] = data['close'].rolling(window=10).mean()
    data['200_day_ma'] = data['close'].rolling(window=50).mean()
    data['buy'] = (data['50_day_ma'] > data['200_day_ma']) & (data['50_day_ma'].shift(1) < data['200_day_ma'].shift(1))
    return data

# Apply the trading strategy to the data
traded_data = trading_strategy(data)

# Initialize variables to keep track of your simulated trades
cash = 10000
shares = st.number_input('Insert a number',1)
total_value = cash

# Create a dataframe to store the trade statements
trade_statements = pd.DataFrame(columns=['Date', 'Action', 'Shares', 'Price', 'Total Value'])

# Loop through the data and make trades based on your strategy
for index, row in traded_data.iterrows():
    if row['buy']:
        shares = cash / row['close']
        cash = 0
        total_value = shares * row['close']
        trade_statements = trade_statements.append({'Date': index, 'Action': 'Buy', 'Shares': shares, 'Price': row['close'], 'Total Value': total_value}, ignore_index=True)
    else:
        total_value = shares * row['close']
    trade_statements = trade_statements.append({'Date': index, 'Action': 'Hold', 'Shares': shares, 'Price': row['close'], 'Total Value': total_value}, ignore_index=True)

# Display the trade statements in a Streamlit app
st.write("TradeView Paper Trading Example")
st.write("Trade Statements:")
st.table(trade_statements)
