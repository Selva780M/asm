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
	con1, con2 ,con3 = st.columns(3)
	with con1:
		st.markdown(f""" *_Date:_* {DATE}""")
	with con3:
		st.markdown(f""" *_Your Investment Rs.30000/-_* """)
	con10, con20  = st.columns(2)
	with con10:
		st.header('*_👋 Im :blue[_PAPER TRADE_] :sunglasses:_*')
	with con20:
		st.subheader('*_🙏 :green[_Mr.Selvakumar_].👉⏰_*')
		
try:
	alice.get_session_id()
except:
	st.error('Pls Login first aliceblue account after continue....')
	sleep(1)
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
		pm = round(df5['P_L'].sum(),1)
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
expiry = Contract()
#------------------------------------------
x = st.sidebar.radio('*_Main Page_*',("Order Placed","Report","Access File"))
if x =="Order Placed" :
	with st.form("opt_form"):				
		user_USER = st.radio('*_Strategy_*',("Price action","ORB Day","ORB 930","BTST","STBT","test"),horizontal=True,key=1)
		st.sidebar.write(f'<h1 style="color:#33ff33;font-size:30px;">{f" {user_USER} 👋"}</h1>', unsafe_allow_html=True)	
		col11, col22, col33 = st.columns(3)
		with col11:		
			user_STOCK = st.radio("*_Stock (Current strike)_*",("NIFTY","BANKNIFTY"), horizontal=True,key=2)
			user_OPTION = st.radio("*_Option_*",("call","put"), horizontal=True,key=3)
			ENTRY = st.form_submit_button('👉 *_Order Placed_*')			
		with col22:		
			user_LOT = st.number_input('*_Qty_*', min_value=25, max_value=1000, value=25, step=25, format=None, key=4)
			user_STOP = st.number_input('*_Stoploss_*', min_value=1, max_value=50, value=10, step=5, format=None,key=5)
			user_TARGET = st.number_input('*_Target_*', min_value=1, max_value=50, value=10, step=5, format=None, key=6)
		if ENTRY:		
			if user_STOCK == "NIFTY":			
				try:
					n = alice.get_scrip_info(alice.get_instrument_by_symbol("INDICES","NIFTY 50"))
					n_ltp = n['LTP']
				except:
					st.warning('*_Sorry, Market Open Time ⏰ Only Working..!!_*')
				spot = round((float(n_ltp)) / 50) * 50
				expiry_date = expiry[0]
				if user_OPTION == "call":
					call_strike = spot - (50)
					n_call = alice.get_instrument_for_fno(exch="NFO", symbol="NIFTY", expiry_date=expiry_date, is_fut=False,strike=call_strike, is_CE=True)				
					s = (alice.get_scrip_info(alice.get_instrument_by_symbol('NFO',n_call.name)))
					entry = float(s['LTP'])	
					new_data = {"DATE" : DATE ,"NAME": user_USER, "STOCK" : n_call.name,  "ENTRY" : int(entry), "QTY" : int(user_LOT), "STOPLOSS" : round((entry - user_STOP),1), "TARGET" : round((entry + user_TARGET),1) }
					df = df.append(new_data, ignore_index = True)	
					df.to_csv('token.csv',index = False)
				if  user_OPTION == "put":
					put_strike = spot + (50)
					n_put = alice.get_instrument_for_fno(exch="NFO", symbol="NIFTY", expiry_date=expiry_date, is_fut=False,strike=put_strike, is_CE=False)
					s = (alice.get_scrip_info(alice.get_instrument_by_symbol('NFO',n_put.name)))
					entry = float(s['LTP'])	
					new_data = {"DATE" : DATE ,"NAME": user_USER, "STOCK" : n_put.name,  "ENTRY" : int(entry), "QTY" : int(user_LOT), "STOPLOSS" : round((entry - user_STOP),1), "TARGET" : round((entry + user_TARGET),1)}
					df = df.append(new_data, ignore_index = True)
					df.to_csv('token.csv',index = False)
			if user_STOCK == "BANKNIFTY":
				try:
					b = alice.get_scrip_info(alice.get_instrument_by_symbol("INDICES","NIFTY BANK"))
					b_ltp = b['LTP']
				except:
					st.warning('*_Sorry, Market Open Time ⏰ Only Working..!!_*')
				spot = round((float(b_ltp)) / 100) * 100			
				expiry_date = expiry[0]
				if user_OPTION == "call":
					call_strike = spot - (100)
					b_call = alice.get_instrument_for_fno(exch="NFO", symbol="BANKNIFTY", expiry_date=expiry_date, is_fut=False,strike=call_strike, is_CE=True)				
					s = (alice.get_scrip_info(alice.get_instrument_by_symbol('NFO',b_call.name)))
					entry = float(s['LTP'])	
					new_data = {"DATE" : DATE ,"NAME": user_USER, "STOCK" : b_call.name,  "ENTRY" : int(entry), "QTY" : int(user_LOT), "STOPLOSS" : round((entry - user_STOP),1), "TARGET" : round((entry + user_TARGET),1)}
					df = df.append(new_data, ignore_index = True)
					df.to_csv('token.csv',index = False)
				if  user_OPTION == "put":
					put_strike = spot + (100)
					b_put = alice.get_instrument_for_fno(exch="NFO", symbol="BANKNIFTY", expiry_date=expiry_date, is_fut=False,strike=put_strike, is_CE=False)
					s = (alice.get_scrip_info(alice.get_instrument_by_symbol('NFO',b_put.name)))
					entry = float(s['LTP'])	
					new_data = {"DATE" : DATE ,"NAME": user_USER, "STOCK" : b_put.name,  "ENTRY" : int(entry), "QTY" : int(user_LOT), "STOPLOSS" : round((entry - user_STOP),1) , "TARGET" : round((entry + user_TARGET),1) }
					df = df.append(new_data, ignore_index = True)
					df.to_csv('token.csv',index = False)	
					
			h = st.empty()
			st.success('*_Your Trade Order Placed Pls Check in Report_*')
			time.sleep(0.5)
			h.empty()
			pass		
if x =="Report":
	placeholder01 = st.empty()
	placeholder12 = st.sidebar.empty()
	placeholder13 = st.sidebar.empty()
	placeholder100 = st.empty()
	placeholder101 = st.empty()	
	if len(df['STOCK']) > 0:
		while True:
			df.to_csv('token.csv',index = False)
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
				c['%'] = (c['P_L']/30000*100)   
				AAA = c.style.format(subset=["P_L","%"], formatter="{:.2f}").applymap(col)									
				st.info(f'_👉 Availble Cash\nRs.{round((30000+im()),1)}_')						
				col1, col2 = st.columns(2)
				with col1:
					st.success(f'_Availble Margin\n Rs.{round((30000+im())-sum(M),1)}_')						
				with col2:
					st.error(f'_Margin Used\nRs.{round(sum(M),1)}_')
			with placeholder13.container():
				st.write(f'<h1 style="color:#33ff33;font-size:25px;">{"Profit Loss"}</h1>', unsafe_allow_html=True)
				st.table(AAA)
				PL = round((df100['P_L'].sum()),1)
				col16, col7 = st.columns(2)
				with col16:
					st.metric("Rs", f"{im()}" , f"{PL}")						
				with col7:
					st.metric("%",f"{round(((im()/30000)*100),1)}%" , f"{round(((PL/30000)*100),1)}%")				
			for i in range(0,len(df100.index)):					
				if(df100.iloc[i,7]) > (df100.iloc[i,6]) and (df100.iloc[i,0] not in df5['DATE'].tolist()):
					df2 = {"DATE" : df100.iloc[i]['DATE'] ,"NAME": df100.iloc[i]['NAME'], "STOCK" : df100.iloc[i]['STOCK'],  "ENTRY" : df100.iloc[i]['ENTRY'], "QTY" : df100.iloc[i]['QTY'], "STOPLOSS" : df100.iloc[i]['STOPLOSS'], "TARGET" : df100.iloc[i]['TARGET'], "LTP" : df100.iloc[i]['LTP'],"P_L" :df100.iloc[i]['P_L']}						
					df5 = df5.append(df2, ignore_index = True)
					df5.to_csv('trade.csv',index = False)					
					df.drop([i], inplace = True)
					st.balloons()
					#time.sleep(1)
					#df.to_csv('token.csv',index = False)
				if(df100.iloc[i,7]) < (df100.iloc[i,5]) and (df100.iloc[i,0] not in df5['DATE'].tolist()):											
					df3 = {"DATE" : df100.iloc[i]['DATE'] ,"NAME": df100.iloc[i]['NAME'], "STOCK" : df100.iloc[i]['STOCK'],  "ENTRY" : df100.iloc[i]['ENTRY'], "QTY" : df100.iloc[i]['QTY'], "STOPLOSS" : df100.iloc[i]['STOPLOSS'], "TARGET" : df100.iloc[i]['TARGET'], "LTP" : df100.iloc[i]['LTP'],"P_L" :df100.iloc[i]['P_L']}
					df5 = df5.append(df3, ignore_index = True)
					df5.to_csv('trade.csv',index = False)
					df.drop([i], inplace = True)
					st.balloons()
					#time.sleep(1)
					#df.to_csv('token.csv',index = False)
			with placeholder01.container():
				col1, col2 = st.columns(2)
				with col1:
					n1 = alice.get_scrip_info(alice.get_instrument_by_symbol("INDICES","NIFTY 50"))
					n5 = n1['LTP']
					st.subheader(f'*_Nifty- 50 Spot Price :green[{n5}]_* ⏰')								
				with col2:
					b1= alice.get_scrip_info(alice.get_instrument_by_symbol("INDICES","NIFTY BANK"))						
					b5 = b1['LTP']
					st.subheader(f'*_BankNifty Spot Price :green[{b5}]_* ⏰')		
			with placeholder100.container():
				st.success('*_Current Position_*')
				#st.write(f'<h1 style="color:#33ff33;font-size:40px;">{f"Position"}</h1>', unsafe_allow_html=True)					
				if len(df100['STOCK']) < 0:
					st.title("No Position Order")					
				else:
					A = df100.style.format(subset=["ENTRY","QTY","STOPLOSS","TARGET","LTP","P_L" ], formatter="{:.2f}").applymap(col)
					st.table(A)
			with placeholder101.container():
				st.info('*_Paper Trade Result_*')
				#st.write(f'<h1 style="color:#33ff33;font-size:40px;">{f"Complete Trade"}</h1>', unsafe_allow_html=True)
				B = df5.style.format(subset=["ENTRY","QTY","STOPLOSS","TARGET","LTP","P_L" ], formatter="{:.2f}").applymap(col)					
				st.table(B)
			time.sleep(1)
if x == "Access File":
	with st.form("opt_form"):		
		st.success('*_Access Current Position File_*')		
		col1, col2, col3 = st.columns(3)
		with col1:
			num = st.number_input('*_Enter Row No_*', min_value=0, max_value=1000, value=len(df.index), step=1, format=None,key=7)
		with col2:
			cr = st.form_submit_button('*_👉Clear Row_*')
		with col3:
			cl  = st.form_submit_button('*_👉Clear ALL_*')
		st.download_button(label='📥 Download File', data=df5.to_csv(), file_name="PaperTrade.csv", mime='csv',key=8)
		if cr:
			df.drop([num], inplace = True)
			df.to_csv('token.csv',index = False)
		if cl:
			for i in range(0,len(df.index)):
				df.drop([i], inplace = True)
			df.to_csv('token.csv',index = False)	
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				

# def on_button_click():
#     st.session_state.error_message = ''
#     st.session_state.result_message = ''
#     if not str(st.session_state.user_name):
#         st.session_state.error_message = "Input your name please~"
#     else:
#         st.session_state.result_message = f"Hello~ {str(st.session_state.user_name)}"


# st.title("Streamlit Test")

# input_user_name = st.text_input(label="User Name", key='user_name', value="")


# checkbox = st.checkbox('agree')
# st.button("Confirm", key='confirm_btn', disabled=(checkbox is False), on_click=on_button_click)

# con = st.container()
# con.caption("Result")
# if 'error_message' in st.session_state and st.session_state.error_message:
#     con.error(st.session_state.error_message)
# if 'result_message' in st.session_state and st.session_state.result_message:
#     con.write(st.session_state.result_message)				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
	
