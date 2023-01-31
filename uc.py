import streamlit as st

st.write("Paper Trading Account User Simulation")

# initialize portfolios
portfolios = {'user': [], 'portfolio': []}

# add user and portfolio
def add_user(user, portfolio):
    portfolios['user'].append(user)
    portfolios['portfolio'].append(portfolio)

# remove user and portfolio
def remove_user(user):
    idx = portfolios['user'].index(user)
    portfolios['user'].pop(idx)
    portfolios['portfolio'].pop(idx)

# initialize portfolio
def init_portfolio():
    return {'symbol': [], 'shares': [], 'price': [], 'total': []}

# add stocks to portfolio
def add_stock(portfolio, symbol, shares, price):
    portfolio['symbol'].append(symbol)
    portfolio['shares'].append(shares)
    portfolio['price'].append(price)
    portfolio['total'].append(shares * price)

# remove stocks from portfolio
def remove_stock(portfolio, symbol):
    idx = portfolio['symbol'].index(symbol)
    portfolio['symbol'].pop(idx)
    portfolio['shares'].pop(idx)
    portfolio['price'].pop(idx)
    portfolio['total'].pop(idx)

# calculate current portfolio value
def calculate_value(portfolio):
    return sum(portfolio['total'])

# UI for adding users
if st.checkbox("Add User"):
    user = st.text_input("Username")
    portfolio = init_portfolio()
    add_user(user, portfolio)

# UI for removing users
if st.checkbox("Remove User"):
    user = st.text_input("Username")
    remove_user(user)

# UI for adding stocks
if st.checkbox("Add Stock"):
    user = st.text_input("Username")
    idx = portfolios['user'].index(user)
    portfolio = portfolios['portfolio'][idx]
    symbol = st.text_input("Symbol")
    shares = int(st.text_input("Shares"))
    price = float(st.text_input("Price"))
    add_stock(portfolio, symbol, shares, price)

# UI for removing stocks
if st.checkbox("Remove Stock"):
    user = st.text_input("Username")
    idx = portfolios['user'].index(user)
    portfolio = portfolios['portfolio'][idx]
    symbol = st.text_input("Symbol")
    remove_stock(portfolio, symbol)

# display portfolios
st.write("Portfolios")
for i in range(len(portfolios['user'])):
    user = portfolios['user'][i]
    portfolio = portfolios['portfolio'][i]
    st.write("User:", user)
    st.write(portfolio)
    st.write("Value: $", calculate_value(portfolio))
