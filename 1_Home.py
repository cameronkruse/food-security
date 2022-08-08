import cmath
from jupyter_client import run_kernel
import numpy as np
import pandas as pd
import streamlit as st
import requests
from datetime import date



# st.set_page_config(
# 	layout="centered",  # Can be "centered" or "wide". In the future also "dashboard", etc.
# 	initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
# 	page_title="USDA Data Explorer",  # String or None. Strings get appended with "• Streamlit". 
# 	page_icon="./assets/img/earthrise_logo.png",  # String, anything supported by st.image, or None.
# )

st.title("USDA Data Exploration Tool")