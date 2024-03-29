import os
import time
os.environ['TZ'] = 'Asia/Kolkata'
time.tzset()
import datetime as DT
import dateutil.relativedelta as REL
def w():
	today = DT.date.today() 
	rd = REL.relativedelta(days=0, weekday=REL.TH)
	e = (today + rd).strftime('%Y-%m-%d')
	return e
e = w()
#---------------------------------------------------
from pya3 import *
import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pytz import timezone 
import time
import requests
day = datetime.now(timezone("Asia/Kolkata"))
DATE = day.strftime('%d-%m-%Y %H:%M:%S')
alice = Aliceblue(user_id='775965',api_key='jFrYnBN1b2WmyWFttnF5iSq6FrHyPioEmcdc15eX1e9viWidrDIYGCnyzI0jNzPceS4QAQ2Bxr7EDOQN8TMajELaHjCgp4OBdRmKEPR31cp6xoXRyMH0ln5BcXRm2t8A')
df = pd.read_csv('./token1.csv')
df5 = pd.read_csv('./trade1.csv')
def temp():
	df.to_csv('token1.csv',index = False)
def save():
	df5.to_csv('trade1.csv',index = False)
#------------------------------------------------------
Investment = int(300000)
Na = str('Mr.Arun kumar')
st.sidebar.markdown(f""" *_Date:_* {DATE}""")
st.sidebar.markdown(f""" *_Your Investment Rs.{Investment}/-_* """)
placeholder1 = st.empty()	
with placeholder1.container():
	con10, con20  = st.columns(2)
	with con10:
		st.header('*_👋  :blue[_BOT Paper Trade_] :sunglasses:_*')
	with con20:
		st.subheader(f'*_🙏 :green[_{Na}_]👉⏰_*')
		
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
		alice.get_contract_master('NFO')
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
	#all_contract = contract_master[contract_master['Symbol'] =='NIFTY']
	#expiry = all_contract['Expiry Date'].sort_values().drop_duplicates().reset_index(drop = True)
	#return expiry
Contract()
#@st.experimental_memo
def loaddata():
	placeholder11 = st.empty()
	try:
		contract_master = pd.read_csv(XX+'.csv') 
		s = contract_master['Trading Symbol']
		sym = s.tolist()		
	except:
		alice.get_contract_master(XX)
		with placeholder11.container():
			with st.spinner(f"*_Loading..._*"):
				time.sleep(30)
		st.success('Done!')
		contract_master = pd.read_csv(XX+'.csv')
		s = contract_master['Trading Symbol']
		sym = s.tolist()				
	return sym
#TeleGram --------------------------------
bot_token = "5719015279:AAHTTTus2_dmsVvp9xTlO2QUFuHwtRmUfbY"
tele_auth_token = '5719015279:AAHTTTus2_dmsVvp9xTlO2QUFuHwtRmUfbY'
tel_group_id =  "Gold_Duck_Trade"
def send_msg_on_telegram(message):
	telegram_api_url = f"https://api.telegram.org/bot{tele_auth_token}/sendMessage?chat_id=@{tel_group_id}&text={message}"
	tel_resp = requests.get(telegram_api_url)
	if tel_resp.status_code == 200:
		print("Notification has been sent on Telegram")
	else:
		print ("Could not send on Telegram Message")
def send_sticker_on_telegram(message):
	telegram_api_url = f"https://api.telegram.org/bot{tele_auth_token}/sendSticker?chat_id=@{tel_group_id}&sticker={message}"
	tel_resp = requests.get(telegram_api_url)
	if tel_resp.status_code == 200:
		print("Notification has been sent on sticker msg Telegram")
	else:
		print("Could not send on Telegram sticker Message")
sad = "CAACAgIAAxkBAANIYxm-bLBDd1VugpzDrfK0eaKNYSYAAvMAA1advQpqG-vEx_qW_ikE"
happy = "CAACAgIAAxkBAANFYxmxaQFWhPkw80xf8NVJxapzwBEAAgMBAAJWnb0KAuXReIfl-k8pBA"


#------------------------------------------
x = st.sidebar.radio('*_Main Page_*',("Order Placed","Report","Access File"),key=10)
if x =="Order Placed" :
	user = st.radio('*_Choose the Stock_*',("Auto","Manual"),horizontal=True,key=1)	
	if user == "Manual":
		XX = st.radio("*_Select Exchange_*",("NFO","NSE","CDS","MCX"),horizontal=True,key=3)
	with st.form("opt_form"):				
		user_USER = st.radio('*_Strategy_*',("Price action","ORB Day","ORB 930","BTST","STBT","Hedging","test"),horizontal=True,key=2)
		st.sidebar.write(f'<h1 style="color:#33ff33;font-size:30px;">{f" {user_USER} 👋"}</h1>', unsafe_allow_html=True)
		st.sidebar.subheader(f'*_Exp. Date 👉 :green[_{e}_]_*')
		col11, col22, col33 = st.columns(3)				
	if user == "Auto":
		MAN = "asn"
		with col11:
			user_STOCK = st.radio("*_Stock (Current strike)_*",("NIFTY","BANKNIFTY"), horizontal=True,key=3)
			user_OPTION = st.radio("*_Option_*",("call","put"), horizontal=True,key=4)			
			ENTRY = st.form_submit_button('👉 *_Order Placed_*')
		with col22:
			user_LOT = st.number_input('*_Qty_*', min_value=25, max_value=1000, value=25, step=25, format=None, key=5)
			user_STOP = st.number_input('*_Stoploss_*', min_value=1, max_value=50, value=10, step=5, format=None,key=6)
			user_TARGET = st.number_input('*_Target_*', min_value=1, max_value=50, value=10, step=5, format=None, key=7)	
	if user == "Manual":
		MAN = "AAUTO"
		with col11:			
			if XX == "NSE":
				user_STOCK = st.selectbox("*_Select Stock_*",(loaddata()))
			if XX == "NFO":
				user_STOCK = st.selectbox("*_Select Stock_*",(loaddata()))			
			if XX == "CDS":
				user_STOCK = st.selectbox("*_Select Stock_*",(loaddata()))			
			if XX == "MCX":
				user_STOCK = st.selectbox("*_Select Stock_*",(loaddata()))
			Tradd = st.radio("*_Trade_*",("Buy","Sell"), horizontal=True,key=4)
			ENTRY = st.form_submit_button('👉 *_Order Placed_*')
		with col22:		
			user_LOT = st.number_input('*_Qty_*', min_value=25, max_value=1000, value=25, step=25, format=None, key=5)
			user_STOP = st.number_input('*_Stoploss_*', min_value=1, max_value=50, value=10, step=5, format=None,key=6)
			user_TARGET = st.number_input('*_Target_*', min_value=1, max_value=50, value=10, step=5, format=None, key=7)
	if ENTRY:		
		if user_STOCK == "NIFTY":			
			try:
				n = alice.get_scrip_info(alice.get_instrument_by_symbol("INDICES","NIFTY 50"))
				n_ltp = n['LTP']
			except:
				st.warning('*_Sorry, Market Open Time ⏰ Only Working..!!_*')
			spot = round((float(n_ltp)) / 50) * 50			
			if user_OPTION == "call":
				call_strike = spot - (50)
				n_call = alice.get_instrument_for_fno(exch="NFO", symbol="NIFTY", expiry_date = e, is_fut=False,strike=call_strike, is_CE=True)								
				s = (alice.get_scrip_info(alice.get_instrument_by_symbol('NFO',n_call.name)))				
				entry = float(s['LTP'])	
				new_data = {"DATE" : DATE ,"NAME": user_USER, "STOCK" : n_call.name, "EXCH" : "NFO" , "TRADE" :"B" ,  "ENTRY" : int(entry), "QTY" : int(user_LOT), "STOPLOSS" : round((entry - user_STOP),1), "TARGET" : round((entry + user_TARGET),1) }
				df = df.append(new_data, ignore_index=True)	
				temp()
			if  user_OPTION == "put":
				put_strike = spot + (50)
				n_put = alice.get_instrument_for_fno(exch="NFO", symbol="NIFTY", expiry_date= e , is_fut=False,strike=put_strike, is_CE=False)
				s = (alice.get_scrip_info(alice.get_instrument_by_symbol('NFO',n_put.name)))
				entry = float(s['LTP'])	
				new_data = {"DATE" : DATE ,"NAME": user_USER, "STOCK" : n_put.name, "EXCH" : "NFO" , "TRADE" :"B"  ,"ENTRY" : int(entry), "QTY" : int(user_LOT), "STOPLOSS" : round((entry - user_STOP),1), "TARGET" : round((entry + user_TARGET),1)}
				df = df.append(new_data, ignore_index = True)
				temp()
		if user_STOCK == "BANKNIFTY":
			try:
				b = alice.get_scrip_info(alice.get_instrument_by_symbol("INDICES","NIFTY BANK"))
				b_ltp = b['LTP']
			except:
				st.warning('*_Sorry, Market Open Time ⏰ Only Working..!!_*')
			spot = round((float(b_ltp)) / 100) * 100						
			if user_OPTION == "call":
				call_strike = spot - (100)
				b_call = alice.get_instrument_for_fno(exch="NFO", symbol="BANKNIFTY", expiry_date =e, is_fut=False,strike=call_strike, is_CE=True)				
				s = (alice.get_scrip_info(alice.get_instrument_by_symbol('NFO',b_call.name)))
				entry = float(s['LTP'])	
				new_data = {"DATE" : DATE ,"NAME": user_USER, "STOCK" : b_call.name, "EXCH" : "NFO" ,"TRADE" :"B" , "ENTRY" : int(entry), "QTY" : int(user_LOT), "STOPLOSS" : round((entry - user_STOP),1), "TARGET" : round((entry + user_TARGET),1)}
				df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
				temp()
			if  user_OPTION == "put":
				put_strike = spot + (100)
				b_put = alice.get_instrument_for_fno(exch="NFO", symbol="BANKNIFTY", expiry_date= e , is_fut=False,strike=put_strike, is_CE=False)
				s = (alice.get_scrip_info(alice.get_instrument_by_symbol('NFO',b_put.name)))
				entry = float(s['LTP'])	
				new_data = {"DATE" : DATE ,"NAME": user_USER, "STOCK" : b_put.name, "EXCH" : "NFO" ,"TRADE" : "B" ,"ENTRY" : int(entry), "QTY" : int(user_LOT), "STOPLOSS" : round((entry - user_STOP),1) , "TARGET" : round((entry + user_TARGET),1) }
				df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
				temp()	
		if MAN  == "AAUTO":
			try:
				b = alice.get_scrip_info(alice.get_instrument_by_symbol(XX,user_STOCK))
				entry = float(b['LTP'])				
			except:
				st.warning('*_Sorry, Market Open Time ⏰ Only Working..!!_*')
			if Tradd =="Buy":
				new_data = {"DATE" : DATE ,"NAME": user_USER, "STOCK" : user_STOCK, "EXCH" : XX , "TRADE" : "B" ,"ENTRY" : int(entry), "QTY" : int(user_LOT), "STOPLOSS" : round((entry - user_STOP),1), "TARGET" : round((entry + user_TARGET),1)}
				df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
				temp()
			if Tradd =="Sell":
				new_data = {"DATE" : DATE ,"NAME": user_USER, "STOCK" : user_STOCK, "EXCH" : XX , "TRADE" : "S" ,"ENTRY" : int(entry), "QTY" : int(user_LOT), "STOPLOSS" : round((entry + user_STOP),1), "TARGET" : round((entry - user_TARGET),1)}
				df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
				temp()
		h = st.empty()
		st.sidebar.success('*_Your Trade Order Placed Pls Check in Report_*')
		time.sleep(0.5)
		h.empty()
		pass		
if x =="Report":
	placeholder01 = st.empty()
	placeholder12 = st.sidebar.empty()
	placeholder13 = st.sidebar.empty()
	placeholder100 = st.empty()
	placeholder101 = st.empty()	
	if (len(df5['STOCK']) > -1) | (len(df['STOCK']) > -1):
		while True:
			temp()
			em = []
			tr = []
			try:
				for i in range(0,len(df.index)):					
					if df.loc[i,'TRADE'] == "B":
						m = alice.get_scrip_info(alice.get_instrument_by_symbol(df.loc[i,'EXCH'],df.loc[i,'STOCK']))				
						lt = float(m['LTP'])
						pl = float((lt - df.loc[i,'ENTRY']) * df.loc[i,'QTY'])
					if df.loc[i,'TRADE'] == "S":
						m = alice.get_scrip_info(alice.get_instrument_by_symbol(df.loc[i,'EXCH'],df.loc[i,'STOCK']))				
						lt = float(m['LTP'])
						pl = float((df.loc[i,'ENTRY'] - lt)  * df.loc[i,'QTY'])
					tr.append(pl)
					em.append(lt)					
			except Exception as e:
				st.write(f"Er.",{e})									
			frame = {'LTP': em,'P_L': tr}
			df1 = pd.DataFrame(frame)
			#df1 = pd.Series(em,name='LTP')
			df100 = pd.concat([df,df1],axis=1)							
			#df100['P_L']  = ((df100['LTP'] - df100['ENTRY']) * df100['QTY'])
			M = df100['ENTRY'] * df100['QTY']	
			with placeholder12.container():					
				c = df100.groupby(['NAME'])['P_L'].sum().reset_index()					
				c['%'] = (c['P_L']/Investment*100)   
				AAA = c.style.format(subset=["P_L","%"], formatter="{:.2f}").applymap(col)									
				st.info(f'_👉 Availble Cash\nRs.{round((Investment+im()),1)}_')						
				col1, col2 = st.columns(2)
				with col1:
					st.success(f'_Availble Margin\n Rs.{round((Investment+im())-sum(M),1)}_')						
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
					st.metric("%",f"{round(((im()/Investment)*100),1)}%" , f"{round(((PL/Investment)*100),1)}%")				
			for i in range(0,len(df100.index)):
				if(df100.iloc[i,9]) > (df100.iloc[i,8]) and (df100.iloc[i,0] not in df5['DATE'].tolist()):
					if (df100.iloc[i,4]) == "B":
						df2 = {"DATE" : df100.iloc[i]['DATE'] ,"NAME": df100.iloc[i]['NAME'], "STOCK" : df100.iloc[i]['STOCK'], "EXCH":df100.iloc[i]['EXCH'], "TRADE": df100.iloc[i]['TRADE'],"ENTRY" : df100.iloc[i]['ENTRY'], "QTY" : df100.iloc[i]['QTY'], "STOPLOSS" : df100.iloc[i]['STOPLOSS'], "TARGET" : df100.iloc[i]['TARGET'], "LTP" : df100.iloc[i]['LTP'],"P_L" :df100.iloc[i]['P_L']}						
						#df5 = df5.append(df2, ignore_index = True)
						df5 = pd.concat([df2, pd.DataFrame([new_data])], ignore_index=True)
						save()					
						df.drop([i], inplace = True)
						st.balloons()						
						send_sticker_on_telegram(happy)
						send_msg_on_telegram(f"Hi {Na}, \nYour Trade  {df100.iloc[i]['NAME']} Completed, Profit in Rs.{round(df100.iloc[i]['P_L'],1)}\nDATE : {df100.iloc[i]['DATE']} \nSTOCK : {df100.iloc[i]['STOCK']} \nTRADE: {df100.iloc[i]['TRADE']} \nEntry Price: {df100.iloc[i]['ENTRY']}\nQTY: {df100.iloc[i]['QTY']}\nSTOPLOSS : {df100.iloc[i]['STOPLOSS']}\nTARGET : {df100.iloc[i]['TARGET']}\nProfit_Loss : {round(df100.iloc[i]['P_L'],1)}")						
				if (df100.iloc[i,9]) < (df100.iloc[i,7]) and (df100.iloc[i,0] not in df5['DATE'].tolist()):
					if (df100.iloc[i,4]) == "B":
						df3 = {"DATE" : df100.iloc[i]['DATE'] ,"NAME": df100.iloc[i]['NAME'], "STOCK" : df100.iloc[i]['STOCK'],"EXCH":df100.iloc[i]['EXCH'], "TRADE": df100.iloc[i]['TRADE'],"ENTRY" : df100.iloc[i]['ENTRY'], "QTY" : df100.iloc[i]['QTY'], "STOPLOSS" : df100.iloc[i]['STOPLOSS'], "TARGET" : df100.iloc[i]['TARGET'], "LTP" : df100.iloc[i]['LTP'],"P_L" :df100.iloc[i]['P_L']}
						#df5 = df5.append(df3, ignore_index = True)
						df5 = pd.concat([df3, pd.DataFrame([new_data])], ignore_index=True)
						save()
						df.drop([i], inplace = True)
						st.balloons()						
						send_sticker_on_telegram(sad)						
						send_msg_on_telegram(f"Hi {Na}, \nYour Trade {df100.iloc[i]['NAME']} Completed, Lose in Rs.{round(df100.iloc[i]['P_L'],1)}\nDATE : {df100.iloc[i]['DATE']} \nSTOCK : {df100.iloc[i]['STOCK']} \nTRADE: {df100.iloc[i]['TRADE']} \nEntry Price: {df100.iloc[i]['ENTRY']}\nQTY: {df100.iloc[i]['QTY']}\nSTOPLOSS : {df100.iloc[i]['STOPLOSS']}\nTARGET : {df100.iloc[i]['TARGET']}\nProfit_Loss : {round(df100.iloc[i]['P_L'],1)}")
				if(df100.iloc[i,9]) < (df100.iloc[i,8]) and (df100.iloc[i,0] not in df5['DATE'].tolist()):
					if (df100.iloc[i,4]) == "S":
						df2 = {"DATE" : df100.iloc[i]['DATE'] ,"NAME": df100.iloc[i]['NAME'], "STOCK" : df100.iloc[i]['STOCK'], "EXCH":df100.iloc[i]['EXCH'], "TRADE": df100.iloc[i]['TRADE'],"ENTRY" : df100.iloc[i]['ENTRY'], "QTY" : df100.iloc[i]['QTY'], "STOPLOSS" : df100.iloc[i]['STOPLOSS'], "TARGET" : df100.iloc[i]['TARGET'], "LTP" : df100.iloc[i]['LTP'],"P_L" :df100.iloc[i]['P_L']}						
						#df5 = df5.append(df2, ignore_index = True)
						df5 = pd.concat([df2, pd.DataFrame([new_data])], ignore_index=True)
						save()					
						df.drop([i], inplace = True)
						st.balloons()						
						send_sticker_on_telegram(happy)
						send_msg_on_telegram(f"Hi {Na}, Your Trade {df100.iloc[i]['NAME']} Completed, Profit in Rs.{round(df100.iloc[i]['P_L'],1)}")						
				if (df100.iloc[i,9]) > (df100.iloc[i,7]) and (df100.iloc[i,0] not in df5['DATE'].tolist()):
					if (df100.iloc[i,4]) == "S":
						df3 = {"DATE" : df100.iloc[i]['DATE'] ,"NAME": df100.iloc[i]['NAME'], "STOCK" : df100.iloc[i]['STOCK'],"EXCH":df100.iloc[i]['EXCH'], "TRADE": df100.iloc[i]['TRADE'],"ENTRY" : df100.iloc[i]['ENTRY'], "QTY" : df100.iloc[i]['QTY'], "STOPLOSS" : df100.iloc[i]['STOPLOSS'], "TARGET" : df100.iloc[i]['TARGET'], "LTP" : df100.iloc[i]['LTP'],"P_L" :df100.iloc[i]['P_L']}
						#df5 = df5.append(df3, ignore_index = True)
						df5 = pd.concat([df3, pd.DataFrame([new_data])], ignore_index=True)
						save()
						df.drop([i], inplace = True)
						st.balloons()						
						send_sticker_on_telegram(sad)
						send_msg_on_telegram(f"Sorry {Na}, Your Trade  {df100.iloc[i]['NAME']}  Completed Lose in Rs.{round(df100.iloc[i]['P_L'],1)}")			
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
				st.warning('*_Paper Trade Chart_*')
				chart_data = df100[["NAME","P_L"]]
				chart_data = chart_data.set_index('NAME')
				st.write(f'<iframe src="https://nifty50signal.streamlit.app/" frameborder="0" scrolling="no" webkitAllowFullScreen="true" mozallowfullscreen="true" allowFullScreen="true" height="400" width="100%"></iframe>',unsafe_allow_html=True)
				st.bar_chart(chart_data)
			time.sleep(1)
if x == "Access File":
	st.sidebar.download_button(label='📥 Download File', data=df5.to_csv(), file_name="PaperTrade.csv", mime='csv',key=8)
	with st.form("opt_form"):		
		st.success('*_Access Current Position File_*')		
		col1, col2, col3 = st.columns(3)
		with col1:
			num = st.number_input('*_Enter Row No_*', min_value=0, max_value=1000, value=len(df.index)-1, step=1, format=None,key=9)
			cr = st.form_submit_button('*_👉Clear Row_*')
		with col3:
			cl  = st.form_submit_button('*_👉Clear ALL_*')	
		if cr:
			df.drop([num], inplace = True)
			temp()
		if cl:
			for i in range(0,len(df.index)):
				df.drop([i], inplace = True)
			temp()		
		A = df.style.format(subset=["ENTRY","QTY","STOPLOSS","TARGET"], formatter="{:.2f}").applymap(col)
		st.table(A)	
