# from pya3 import *
# import streamlit as st
# from datetime import datetime, timedelta
# from pytz import timezone 
# import time
# day = datetime.now(timezone("Asia/Kolkata"))
# day = day.strftime('%Y-%m-%d %H:%M:%S')
# alice = Aliceblue(user_id='627742',api_key='BPk1mFAXB9ByTFFQnm87HhieLFo3Fy5J3PCaae2g252DiLCNB9BK7hF0LpSg3d9fNO698r32IAsEt0lWm3hmuZMWW9tJC6r6A7xGkZWGmY1Hcdys1q9ITC1pRjYaklRQ')
# alice.get_session_id()
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

import streamlit as st
import pyessl

def fetch_data_from_essl_device():
  # Connect to the ESSL biometric device
  biometric = pyessl.device('192.168.1.201', port=80)

  # Fetch data from the device
  data = biometric.get_data()

  return data

# Example Usage: Display the fetched data in a Streamlit app
st.title("ESSL Biometric Data")

data = fetch_data_from_essl_device()
st.write("Fetched data from ESSL biometric device:", data)
