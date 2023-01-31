from pya3 import *
import streamlit as st
from datetime import datetime, timedelta
from pytz import timezone 
day = datetime.now(timezone("Asia/Kolkata"))
day = day.strftime('%Y-%m-%d %H:%M:%S')
alice = Aliceblue(user_id='627742',api_key='BPk1mFAXB9ByTFFQnm87HhieLFo3Fy5J3PCaae2g252DiLCNB9BK7hF0LpSg3d9fNO698r32IAsEt0lWm3hmuZMWW9tJC6r6A7xGkZWGmY1Hcdys1q9ITC1pRjYaklRQ')
alice.get_session_id()
exchange = "NFO"
symbol = "NIFTY"
st.write(day)
ticker = "NIFTY 50","BANK NIFTY"
def main():
       try:
              for i in ticker:
                     m = alice.get_scrip_info(alice.get_instrument_by_symbol('INDICES', i))
                     st.write(f"Nifty50:{m['LTP']}Change:{m['Change']} %{m['PerChange']}")
       except Exception as e:              
              st.write(f"Error",{e})
       sleep(1)


def get_ltp(symbol):
    # Get the current price of the stock
    m=alice.get_scrip_info(alice.get_instrument_by_symbol('INDICES', symbol))
    stock = m['LTP']
    return stock

def paper_trade():
    st.title("Paper Trading Simulator")

    # Define the symbol
    symbol = st.text_input("Enter the symbol of the stock you want to trade:")

    # Get the LTP
    ltp = get_ltp(symbol)

    st.write(f"The LTP of {symbol} is {ltp}")

    # Define the number of shares
    shares = st.number_input("Enter the number of shares you want to buy:",int(2))

    # Calculate the cost of the trade
    cost = float(float(ltp) * float(shares))

    st.write(f"The cost of the trade is {cost}")

    # Define the action
    action = st.selectbox("What action do you want to take?", ["Buy", "Sell"])

    # Check if the action is Buy or Sell
    if action == "Buy":
        # Get the current account balance
        balance = float(st.text_input("Enter your current account balance:"))

        # Check if the balance is sufficient
        if balance < cost:
            st.write("Insufficient funds.")
        else:
            st.write("The trade has been executed successfully.")
            # Update the balance
            balance -= cost
            st.write(f"Your new balance is {balance}")
    else:
        # Get the current number of shares
        current_shares = float(st.text_input("Enter your current number of shares:"))

        # Check if the shares are sufficient
        if current_shares < shares:
            st.write("Insufficient shares.")
        else:
            st.write("The trade has been executed successfully.")
            # Update the shares
            current_shares -= shares
            st.write(f"Your new number of shares is {current_shares}")

if __name__ == "__main__":
    #paper_trade()
    main()
