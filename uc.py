import cv2
import streamlit as st
#st.write(f'<iframe src="http://www.google.com/custom?q=&btnG=Search" frameborder="0" scrolling="yes" webkitAllowFullScreen="true" mozallowfullscreen="true" allowFullScreen="true" height="1920" width="100%"></iframe>',unsafe_allow_html=True)
#st.write(f'<iframe id="if1" width="100%" height="254" style="visibility:visible" src="http://www.google.com/custom?q=&btnG=Search"></iframe>',unsafe_allow_html=True)
import sys
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication
 
app = QApplication(sys.argv)
 
web = QWebEngineView()
web.load(QUrl("https://stackoverflow.com/"))
web.show()
 
sys.exit(app.exec_())
