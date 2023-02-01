from pya3 import *
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from pytz import timezone 
import time
day = datetime.now(timezone("Asia/Kolkata"))
DATE = day.strftime('%Y-%m-%d %H:%M:%S')
alice = Aliceblue(user_id='627742',api_key='BPk1mFAXB9ByTFFQnm87HhieLFo3Fy5J3PCaae2g252DiLCNB9BK7hF0LpSg3d9fNO698r32IAsEt0lWm3hmuZMWW9tJC6r6A7xGkZWGmY1Hcdys1q9ITC1pRjYaklRQ')
alice.get_session_id()


# def main():
#        try:
#               for i in ticker:
#                      m = alice.get_scrip_info(alice.get_instrument_by_symbol('INDICES',i))
#                      st.write(f"{i} : {m['LTP']} Change: {m['Change']} % {m['PerChange']}")
#        except Exception as e:              
#               st.write(f"Error",{e})       

placeholder1 = st.empty()	
with placeholder1.container():
	st.success(f"Welcome !!!!⏰⏰")
	con1, con2 ,con3 = st.columns(3)
	with con1:
		st.markdown(f""" *_Date:_* {DATE}""")
	with con3:
		st.markdown(f""" *_ALGO PAPER TRADE:_* """)
		
#Get Expiry-------------------------------------------
try:
	contract_master= pd.read_csv('NFO.csv')
except:
	alice.get_contract_master('NFO')
	contract_master = pd.read_csv('NFO.csv')
all_contract=contract_master[contract_master['Symbol']=='NIFTY']
expiry = all_contract['Expiry Date'].sort_values().drop_duplicates().reset_index(drop = True)
#------------------------------------------
with st.form("opt_form"):
	col11, col22, col33 = st.columns(3)		
	user_USER = st.sidebar.radio('USER',('ARUN','SELVA','VIJAY','VASANTH'))
	if user_USER:
		st.sidebar.write(f'<h1 style="color:#33ff33;font-size:40px;">{f"Hi 👋 {user_USER}"}</h1>', unsafe_allow_html=True)
		st.sidebar.write(f'<h1 style="color:#33ff33;font-size:30px;">{f"Enter Data 👉"}</h1>', unsafe_allow_html=True)
	with col11:		
		user_STOCK = st.radio("Stock",("NIFTY","BANKNIFTY"), horizontal=True)
		user_OPTION = st.radio("Option",("call","put"), horizontal=True)
		user_LOT = st.number_input('Qty', min_value=25, max_value=1000, value=25, step=25, format=None, key=None)
	with col22:		
		user_STOP = st.number_input('Stoploss', min_value=5, max_value=50, value=10, step=5, format=None, key=None)
		user_TARGET = st.number_input('Target', min_value=5, max_value=50, value=10, step=5, format=None, key=None)		
		ENTRY = st.form_submit_button('👉 Order Placed')
	if ENTRY:
		#new_data = {"DATE" : op ,"NAME": user_name, "VEHICLE NO" : user_vehicleNo,  "FUEL" : user_fuel, "LITER" : float(user_Liter), "AMOUNT" : float(user_amount), "DEPT" : user_Dept, "REASON" : user_reason}
		#df = df.append(new_data, ignore_index = True)
		#df.to_csv('token.csv',index = False)
		st.write('pass')
		if user_STOCK == "NIFTY":			
			n = alice.get_scrip_info(alice.get_instrument_by_symbol("INDICES","NIFTY 50"))
			n_ltp = n['LTP']
			spot = round((float(n_ltp)) / 50) * 50
			expiry_date = expiry[0]
			if user_OPTION == "call":
				call_strike = spot - (50)
				n_call = alice.get_instrument_for_fno(exch="NFO", symbol="NIFTY", expiry_date=expiry_date, is_fut=False,strike=call_strike, is_CE=True)
				st.write(n_call.name)
				st.balloons()
			if  user_OPTION == "put":
				put_strike = spot + (50)
				n_put = alice.get_instrument_for_fno(exch="NFO", symbol="NIFTY", expiry_date=expiry_date, is_fut=False,strike=put_strike, is_CE=False)
				st.write(n_put.name)
				st.balloons()			
		if user_STOCK == "BANKNIFTY":
			b = alice.get_scrip_info(alice.get_instrument_by_symbol("INDICES","NIFTY BANK"))
			b_ltp = b['LTP']
			spot = round((float(b_ltp)) / 100) * 100			
			expiry_date = expiry[0]
			if user_OPTION == "call":
				call_strike = spot - (100)
				b_call = alice.get_instrument_for_fno(exch="NFO", symbol="BANKNIFTY", expiry_date=expiry_date, is_fut=False,strike=call_strike, is_CE=True)
				st.write(b_call.name)
				st.balloons()
			if  user_OPTION == "put":
				put_strike = spot + (100)
				b_put = alice.get_instrument_for_fno(exch="NFO", symbol="BANKNIFTY", expiry_date=expiry_date, is_fut=False,strike=put_strike, is_CE=False)
				st.write(b_put.name)
				st.balloons()
		
