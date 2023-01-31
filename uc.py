import streamlit as st

st.write("Paper Trading Simulation")

# initialize portfolio
portfolio = {'symbol': [], 'shares': [], 'price': [], 'total': []}

# add stocks to portfolio
def add_stock(symbol, shares, price):
    portfolio['symbol'].append(symbol)
    portfolio['shares'].append(shares)
    portfolio['price'].append(price)
    portfolio['total'].append(shares * price)

# remove stocks from portfolio
def remove_stock(symbol):
    idx = portfolio['symbol'].index(symbol)
    portfolio['symbol'].pop(idx)
    portfolio['shares'].pop(idx)
    portfolio['price'].pop(idx)
    portfolio['total'].pop(idx)

# calculate current portfolio value
def calculate_value():
    return sum(portfolio['total'])

# UI for adding stocks
if st.checkbox("Add Stock"):
    symbol = st.text_input("Symbol")
    shares = int(st.text_input("Shares"))
    price = float(st.text_input("Price"))
    add_stock(symbol, shares, price)

# UI for removing stocks
if st.checkbox("Remove Stock"):
    symbol = st.text_input("Symbol")
    remove_stock(symbol)

# display portfolio
st.write("Portfolio")
st.write(portfolio)
st.write("Value: $", calculate_value())
