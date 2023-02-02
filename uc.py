from pya3 import *
import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pytz import timezone 
import time
day = datetime.now(timezone("Asia/Kolkata"))
DATE = day.strftime('%d-%m-%Y %H:%M:%S')
alice = Aliceblue(user_id='627742',api_key='BPk1mFAXB9ByTFFQnm87HhieLFo3Fy5J3PCaae2g252DiLCNB9BK7hF0LpSg3d9fNO698r32IAsEt0lWm3hmuZMWW9tJC6r6A7xGkZWGmY1Hcdys1q9ITC1pRjYaklRQ')
alice.get_session_id()
df = pd.read_csv('./token.csv')
df5 = pd.read_csv('./trade.csv')
#------------------------------------------------------
placeholder1 = st.empty()	
with placeholder1.container():
	st.success(f"Welcome !!!!⏰⏰")
	con1, con2 ,con3 = st.columns(3)
	with con1:
		st.markdown(f""" *_Date:_* {DATE}""")
	with con3:
		st.markdown(f""" *_ALGO PAPER TRADE_* """)
#--------------------------------------------
def col(val):
	try:
		if val > 0:
			color = 'green'
		elif val < 0 :
			color = 'red'				
		else:			
			color = 'white'
	except:
		color = 'white'
	
	return 'color: %s' % color


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
	user_USER = 'SELVA' #st.sidebar.write('*_SELVA_*')
	st.sidebar.write(f'<h1 style="color:#33ff33;font-size:30px;">{f"Hi 👋 {user_USER}"}</h1>', unsafe_allow_html=True)
	st.sidebar.write(f'<h1 style="color:#33ff33;font-size:20px;">{f"Pls Enter Details 👉"}</h1>', unsafe_allow_html=True)
	with col11:		
		user_STOCK = st.radio("*_Stock (Current strike)_*",("NIFTY","BANKNIFTY"), horizontal=True)
		user_OPTION = st.radio("*_Option_*",("call","put"), horizontal=True)
		st.write('')
		st.write('')
		st.write('')
		ENTRY = st.form_submit_button('👉 *_Order Placed_*')
	with col22:		
		user_LOT = st.number_input('*_Qty_*', min_value=25, max_value=1000, value=25, step=25, format=None, key=None)
		user_STOP = st.number_input('*_Stoploss_*', min_value=1, max_value=50, value=10, step=5, format=None, key=None)
		user_TARGET = st.number_input('*_Target_*', min_value=1, max_value=50, value=10, step=5, format=None, key=None)			
	with col33:
		placeholder01 = st.empty()
	if ENTRY:
		if user_STOCK == "NIFTY":			
			n = alice.get_scrip_info(alice.get_instrument_by_symbol("INDICES","NIFTY 50"))
			n_ltp = n['LTP']
			spot = round((float(n_ltp)) / 50) * 50
			expiry_date = expiry[0]
			if user_OPTION == "call":
				call_strike = spot - (50)
				n_call = alice.get_instrument_for_fno(exch="NFO", symbol="NIFTY", expiry_date=expiry_date, is_fut=False,strike=call_strike, is_CE=True)				
				s = (alice.get_scrip_info(alice.get_instrument_by_symbol('NFO',n_call.name)))
				entry = float(s['LTP'])	
				new_data = {"DATE" : DATE ,"NAME": user_USER, "STOCK" : n_call.name,  "ENTRY" : round(entry,1), "QTY" : int(user_LOT), "STOPLOSS" : round((entry - user_STOP),1), "TARGET" : round((entry + user_TARGET),1)}
				df = df.append(new_data, ignore_index = True)
				df.to_csv('token.csv',index = False)				
			if  user_OPTION == "put":
				put_strike = spot + (50)
				n_put = alice.get_instrument_for_fno(exch="NFO", symbol="NIFTY", expiry_date=expiry_date, is_fut=False,strike=put_strike, is_CE=False)
				s = (alice.get_scrip_info(alice.get_instrument_by_symbol('NFO',n_put.name)))
				entry = float(s['LTP'])	
				new_data = {"DATE" : DATE ,"NAME": user_USER, "STOCK" : n_put.name,  "ENTRY" : round(entry,1), "QTY" : int(user_LOT), "STOPLOSS" : round((entry - user_STOP),1), "TARGET" : round((entry + user_TARGET),1)}
				df = df.append(new_data, ignore_index = True)
				df.to_csv('token.csv',index = False)							
		if user_STOCK == "BANKNIFTY":
			b = alice.get_scrip_info(alice.get_instrument_by_symbol("INDICES","NIFTY BANK"))
			b_ltp = b['LTP']
			spot = round((float(b_ltp)) / 100) * 100			
			expiry_date = expiry[0]
			if user_OPTION == "call":
				call_strike = spot - (100)
				b_call = alice.get_instrument_for_fno(exch="NFO", symbol="BANKNIFTY", expiry_date=expiry_date, is_fut=False,strike=call_strike, is_CE=True)				
				s = (alice.get_scrip_info(alice.get_instrument_by_symbol('NFO',b_call.name)))
				entry = float(s['LTP'])	
				new_data = {"DATE" : DATE ,"NAME": user_USER, "STOCK" : b_call.name,  "ENTRY" : round(entry,1), "QTY" : int(user_LOT), "STOPLOSS" : round((entry - user_STOP),1), "TARGET" : round((entry + user_TARGET),1)}
				df = df.append(new_data, ignore_index = True)
				df.to_csv('token.csv',index = False)				
			if  user_OPTION == "put":
				put_strike = spot + (100)
				b_put = alice.get_instrument_for_fno(exch="NFO", symbol="BANKNIFTY", expiry_date=expiry_date, is_fut=False,strike=put_strike, is_CE=False)
				s = (alice.get_scrip_info(alice.get_instrument_by_symbol('NFO',b_put.name)))
				entry = float(s['LTP'])	
				new_data = {"DATE" : DATE ,"NAME": user_USER, "STOCK" : b_put.name,  "ENTRY" : round(entry,1), "QTY" : int(user_LOT), "STOPLOSS" : round((entry - user_STOP),1) , "TARGET" : round((entry + user_TARGET),1)}
				df = df.append(new_data, ignore_index = True)
				df.to_csv('token.csv',index = False)				
		placeholder12 = st.sidebar.empty()
		placeholder100 = st.empty()
		placeholder101 = st.empty()
		if len(df['STOCK']) > 0:
			while True:
				em = []
				try:
					for i in df['STOCK']:
						m = alice.get_scrip_info(alice.get_instrument_by_symbol('NFO',i))				
						lt = float(m['LTP'])								
						em.append(lt)
				except Exception as e:
					st.write(f"Er.",{e})					
				df100 = pd.DataFrame()
				df1 = pd.Series(em,name='LTP')
				df100 = pd.concat([df,df1],axis=1)
				df100['P_L']  = ((df100['LTP'] - df100['ENTRY']) * df100['QTY'])
				#PL = round((df100.loc[df100['NAME'] == str(user_USER) , 'P_L'].sum()),1
				with placeholder12.container():								
					col0, col11 ,col12 = st.columns(3)
					with col11:
						st.info(f'Availble\nMargin')
						st.write('Rs.10000')
					col1, col2 = st.columns(2)
					with col1:
						st.success('Availble Cash\n _Rs.10000_')
						st.write('Rs.10000')
					with col2:
						st.error('Margin Used')
						st.write('Rs.5500')					
				for i in range(0,len(df100.index)):					
					if(df100.iloc[i,6]) < (df100.iloc[i,7]) and (df100.iloc[i,1] not in df5['NAME'].tolist()) and (df100.iloc[i,2] not in df5['STOCK'].tolist()):						
						df2 = {"DATE" : df100.iloc[i]['DATE'] ,"NAME": df100.iloc[i]['NAME'], "STOCK" : df100.iloc[i]['STOCK'],  "ENTRY" : df100.iloc[i]['ENTRY'], "QTY" : df100.iloc[i]['QTY'], "STOPLOSS" : df100.iloc[i]['STOPLOSS'], "TARGET" : df100.iloc[i]['TARGET'], "LTP" : df100.iloc[i]['LTP'],"P_L" :df100.iloc[i]['P_L']}						
						df5 = df5.append(df2, ignore_index = True)
						df5.to_csv('trade.csv',index = False)
						st.balloons()
						#df100 = df100.drop(df.index[i])						
					if(df100.iloc[i,5]) > (df100.iloc[i,7]) and (df100.iloc[i,1] not in df5['NAME'].tolist()) and (df100.iloc[i,2] not in df5['STOCK'].tolist()):						
						df3 = {"DATE" : df100.iloc[i]['DATE'] ,"NAME": df100.iloc[i]['NAME'], "STOCK" : df100.iloc[i]['STOCK'],  "ENTRY" : df100.iloc[i]['ENTRY'], "QTY" : df100.iloc[i]['QTY'], "STOPLOSS" : df100.iloc[i]['STOPLOSS'], "TARGET" : df100.iloc[i]['TARGET'], "LTP" : df100.iloc[i]['LTP'],"P_L" :df100.iloc[i]['P_L']}
						df5 = df5.append(df3, ignore_index = True)
						df5.to_csv('trade.csv',index = False)
						st.balloons()
						#df100 = df100.drop(df.index[i])					
				with col33:
					with placeholder01.container():
						st.write(f'<h1 style="color:#33ff33;font-size:25px;">{"(Profit/Loss)"}</h1>', unsafe_allow_html=True)
						PL = round((df100.loc[df100['NAME'] == str(user_USER) , 'P_L'].sum()),1)
						def im():
							try :
								pm = round(df5.loc[df5['NAME'] == str(user_USER) , 'P_L'].sum(),1)
							except:
								pm = round(0.0,1)
							return pm
						st.metric("Rs", f"{im()}" , f"{PL}")
				with placeholder100.container():
					st.write(f'<h1 style="color:#33ff33;font-size:40px;">{f"Position"}</h1>', unsafe_allow_html=True)					
					A = df100.style.format(subset=["ENTRY","QTY","STOPLOSS","TARGET","LTP","P_L" ], formatter="{:.2f}").applymap(col)
					st.table(A)							
				with placeholder101.container():
					st.write(f'<h1 style="color:#33ff33;font-size:40px;">{f"Complete Trade"}</h1>', unsafe_allow_html=True)
					B = df5.style.format(subset=["ENTRY","QTY","STOPLOSS","TARGET","LTP","P_L" ], formatter="{:.2f}").applymap(col)					
					st.table(B)	
				time.sleep(1)
		
