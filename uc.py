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
df = pd.read_csv('./token.csv')
df5 = pd.read_csv('./trade.csv')
#------------------------------------------------------
placeholder1 = st.empty()	
with placeholder1.container():
	st.header('*_👋Hey, Im :blue[_ALGO PAPER TRADE_] :sunglasses:_*')
	time.sleep(2)
	st.subheader('*_Welcome!! :green[_Mr.Selvakumar_] lets go...👉⏰_*')	
	con1, con2 ,con3 = st.columns(3)
	with con1:
		st.markdown(f""" *_Date:_* {DATE}""")
	with con3:
		st.markdown(f""" *_Your Investment Rs.30000/-_* """)
try:
	alice.get_session_id()
except:
	st.error('Pls Login first aliceblue account after continue....')
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
def im():
	try :
		pm = round(df5.loc[df5['NAME'] == str(user_USER) , 'P_L'].sum(),1)
	except:
		pm = round(0.0,1)
	return pm

#Get Expiry-------------------------------------------
def Contract():
	placeholder00 = st.empty()
	success=False
	try:
		contract_master= pd.read_csv('NFO.csv')
		success=True
	except:
		with placeholder00.container():
			st.warning('*_Contract master fetch Error Wait 10 sec.._*')
		time.sleep(10)
		success=False
		idx = 1
		while not success:
			try:
				alice.get_contract_master('NFO')
				time.sleep(15)
				contract_master = pd.read_csv('NFO.csv')
				success=True
			except:
				with placeholder00.container():
					st.error(f"*_Connection lost Retrying {idx} times on contracts Master.._*")
				success=False
			time.sleep(10)
			idx += 1	
	all_contract = contract_master[contract_master['Symbol']=='NIFTY']
	expiry = all_contract['Expiry Date'].sort_values().drop_duplicates().reset_index(drop = True)
	return expiry
Contract()
#------------------------------------------
with st.form("opt_form"):	
	col11, col22, col33 = st.columns(3)	
	user_USER = st.sidebar.radio('*_Strategy_*',("Price action","ORB Day","ORB 915"))
	st.sidebar.write(f'<h1 style="color:#33ff33;font-size:30px;">{f" {user_USER} 👋"}</h1>', unsafe_allow_html=True)	
	with col11:		
		user_STOCK = st.radio("*_Stock (Current strike)_*",("NIFTY","BANKNIFTY"), horizontal=True)
		user_OPTION = st.radio("*_Option_*",("call","put"), horizontal=True)
		st.write('')
		st.write('')
		st.write('')
		ENTRY = st.form_submit_button('👉 *_Order Placed_*')		
	with col22:		
		user_LOT = st.number_input('*_Qty_*', min_value=25, max_value=1000, value=25, step=25, format=None, key=None)
		user_STOP = st.number_input('*_Stoploss_*', min_value=10, max_value=50, value=10, step=10, format=None, key=None)
		user_TARGET = st.number_input('*_Target_*', min_value=10, max_value=50, value=10, step=10, format=None, key=None)			
	with col33:
		placeholder01 = st.empty()		
	if ENTRY:
		if user_STOCK == "NIFTY":			
			try:
				n = alice.get_scrip_info(alice.get_instrument_by_symbol("INDICES","NIFTY 50"))
			except:
				st.warning('*_Sorry, Market Open Time ⏰ Only Working..!!_*')
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
			if  user_OPTION == "put":
				put_strike = spot + (50)
				n_put = alice.get_instrument_for_fno(exch="NFO", symbol="NIFTY", expiry_date=expiry_date, is_fut=False,strike=put_strike, is_CE=False)
				s = (alice.get_scrip_info(alice.get_instrument_by_symbol('NFO',n_put.name)))
				entry = float(s['LTP'])	
				new_data = {"DATE" : DATE ,"NAME": user_USER, "STOCK" : n_put.name,  "ENTRY" : round(entry,1), "QTY" : int(user_LOT), "STOPLOSS" : round((entry - user_STOP),1), "TARGET" : round((entry + user_TARGET),1)}
				df = df.append(new_data, ignore_index = True)											
		if user_STOCK == "BANKNIFTY":
			try:
				b = alice.get_scrip_info(alice.get_instrument_by_symbol("INDICES","NIFTY BANK"))
			except:
				st.warning('*_Sorry, Market Open Time ⏰ Only Working..!!_*')			
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
			if  user_OPTION == "put":
				put_strike = spot + (100)
				b_put = alice.get_instrument_for_fno(exch="NFO", symbol="BANKNIFTY", expiry_date=expiry_date, is_fut=False,strike=put_strike, is_CE=False)
				s = (alice.get_scrip_info(alice.get_instrument_by_symbol('NFO',b_put.name)))
				entry = float(s['LTP'])	
				new_data = {"DATE" : DATE ,"NAME": user_USER, "STOCK" : b_put.name,  "ENTRY" : round(entry,1), "QTY" : int(user_LOT), "STOPLOSS" : round((entry - user_STOP),1) , "TARGET" : round((entry + user_TARGET),1)}
				df = df.append(new_data, ignore_index = True)								
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
				M = df100['ENTRY'] * df100['QTY']				
				with placeholder12.container():					
					c = df100.groupby(['NAME'])['P_L'].sum().reset_index()
					AAA = c.style.format(subset=["P_L" ], formatter="{:.2f}").applymap(col)					
					st.table(AAA)
					st.info(f'_👉 Availble Cash\nRs.{round((30000+im()),1)}_')						
					col1, col2 = st.columns(2)
					with col1:
						st.success(f'_Availble Margin\n Rs.{round((30000+im())-sum(M),1)}_')						
					with col2:
						st.error(f'_Margin Used\nRs.{round(sum(M),1)}_')
					
					col16, col7 = st.columns(2)
					st.write(f'<h1 style="color:#33ff33;font-size:25px;">{"Profit Loss"}</h1>', unsafe_allow_html=True)
					PL = round((df100.loc[df100['NAME'] == str(user_USER) , 'P_L'].sum()),1)
					with col6:
						st.metric("Rs", f"{im()}" , f"{PL}")						
					with col7:
						st.metric("%",f"{round(((im()/30000)*100),1)}%" , f"{round(((PL/30000)*100),1)}%")
				for i in range(0,len(df100.index)):					
					if(df100.iloc[i,7]) > (df100.iloc[i,6]) and (df100.iloc[i,0] not in df5['DATE'].tolist()):
						df2 = {"DATE" : df100.iloc[i]['DATE'] ,"NAME": df100.iloc[i]['NAME'], "STOCK" : df100.iloc[i]['STOCK'],  "ENTRY" : df100.iloc[i]['ENTRY'], "QTY" : df100.iloc[i]['QTY'], "STOPLOSS" : df100.iloc[i]['STOPLOSS'], "TARGET" : df100.iloc[i]['TARGET'], "LTP" : df100.iloc[i]['LTP'],"P_L" :df100.iloc[i]['P_L']}						
						df5 = df5.append(df2, ignore_index = True)
						df5.to_csv('trade.csv',index = False)
						st.balloons()
						df.drop([i], inplace = True)
					if(df100.iloc[i,7]) < (df100.iloc[i,5]) and (df100.iloc[i,0] not in df5['DATE'].tolist()):											
						df3 = {"DATE" : df100.iloc[i]['DATE'] ,"NAME": df100.iloc[i]['NAME'], "STOCK" : df100.iloc[i]['STOCK'],  "ENTRY" : df100.iloc[i]['ENTRY'], "QTY" : df100.iloc[i]['QTY'], "STOPLOSS" : df100.iloc[i]['STOPLOSS'], "TARGET" : df100.iloc[i]['TARGET'], "LTP" : df100.iloc[i]['LTP'],"P_L" :df100.iloc[i]['P_L']}
						df5 = df5.append(df3, ignore_index = True)
						df5.to_csv('trade.csv',index = False)
						st.balloons()
						df.drop([i], inplace = True)
				with col33:
					with placeholder01.container():
						n5 = alice.get_scrip_info(alice.get_instrument_by_symbol("INDICES","NIFTY 50"))
						bn = alice.get_scrip_info(alice.get_instrument_by_symbol("INDICES","NIFTY BANK"))
						st.write(f'<h1 style="color:#33ff33;font-size:25px;">{f"Nifty- 50 Spot Price : {round(n5},1)"}</h1>', unsafe_allow_html=True)
						st.write(f'<h1 style="color:#33ff33;font-size:25px;">{f"BakkNifty Spot Price : {round(bn,1)}"}</h1>', unsafe_allow_html=True)
				with placeholder100.container():
					st.write(f'<h1 style="color:#33ff33;font-size:40px;">{f"Position"}</h1>', unsafe_allow_html=True)					
					A = df100.style.format(subset=["ENTRY","QTY","STOPLOSS","TARGET","LTP","P_L" ], formatter="{:.2f}").applymap(col)
					st.table(A)							
				with placeholder101.container():
					st.write(f'<h1 style="color:#33ff33;font-size:40px;">{f"Complete Trade"}</h1>', unsafe_allow_html=True)
					B = df5.style.format(subset=["ENTRY","QTY","STOPLOSS","TARGET","LTP","P_L" ], formatter="{:.2f}").applymap(col)					
					st.table(B)
					col11, col22, col33,col44 = st.columns(4)					
					with col11:
						cl = st.button('👉 *_Delete Row_*')
					with col22:
						num = st.number_input('*_EnterRow No_*', min_value=0, max_value=len(df5.index), value=1, step=1, format=None, key=None)					
					with col44:
						dl  = st.button('👉 *_Reset_*')
				if cl:
					df100.drop([num], inplace = True)
					df100.to_csv('trade.csv',index = False)
				if dl :
					for i in range(0,len(df5.index)):
						df100.drop([i], inplace = True)
					df100.to_csv('trade.csv',index = False)
				df.to_csv('token.csv',index = False)
				time.sleep(1)
		
