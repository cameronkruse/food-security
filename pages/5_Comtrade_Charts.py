import streamlit as st
import pandas as pd
import requests
from datetime import date
import plotly.figure_factory as ff
import plotly.express as px
import numpy as np


color_dict = {
            "(?)":"white",
            "Animals; live":"#807E5B",
            "Meat and edible meat offal":"#C9938B",
            "Dairy produce; birds' eggs; natural honey; edible products of animal origin, not elsewhere specified or included":"#99B7CF",
            "Animal originated products; not elsewhere specified or included":"#7D7E7D",
            "Vegetables and certain roots and tubers; edible":"#57633C",
            "Fruits and nuts; edible":"#98A552",
            "Cereals":"#B99A7A",
            "Coffee, tea, mate and spices":"#5F4737",
            "Fruit and nuts, edible; peel of citrus fruit or melons":"#C66562",
            "Products of the milling industry; malt, starches, inulin, wheat gluten":"#8D8D8E",
            "Oil seeds and oleaginous fruits; miscellaneous grains, seeds and fruit, industrial or medicinal plants; straw and fodder":"#F3E18F",
            "Lac; gums, resins and other vegetable saps and extracts":"#B5A6C8",
            "Animal or vegetable fats and oils and their cleavage products; prepared animal fats; animal or vegetable waxes":"#EAAC55",
            "Sugars and sugar confectionery":"#EBE5D9",
            "Preparations of cereals, flour, starch or milk; pastrycooks' products":"#662C69",
            "Fish and crustaceans, molluscs and other aquatic invertebrates":"#A3AAA5",
            "Meat, fish or crustaceans, molluscs or other aquatic invertebrates; preparations thereof":"#3B768C",
            "Preparations of vegetables, fruit, nuts or other parts of plants":"#E95F85"
            }

def get_comtrade_data(endpoint_url):
     request = requests.get(url=endpoint_url)
     print (request)
     length = len(request.json()["dataset"])
     print ("length is " + str(length))
     if length > 1998:
           print ("Data may be truncated in graphs due to API limit")
     return (pd.json_normalize(request.json()["dataset"]))

def make_treegraph (dataframe, Year, Type):
     fig = px.treemap(dataframe, path=[px.Constant("all"), "cmdDescE", 'ptTitle'], values='TradeValue', color='cmdDescE', color_discrete_map=color_dict)
     fig.update_layout(margin = dict(t=50, l=0, r=0, b=0))
     fig.update_layout(title_text=f'{Type} by Commodity and Partner in {Year}')
     # remove outline color
     fig.update_traces(marker_line_color='rgb(0,0,0)', marker_line_width=.1)
     return(fig)

def commodity_charts(country_code):
    year = "2021"
    multiyear_string = "2021%2C2020%2C2019%2C2018%2C2017"
    # this is a string of all the two digit commodity codes that I consider to be food
    food_code_string = "01%2C02%2C03%2C04%2C05%2C07%2C08%2C09%2C10%2C11%2C12%2C13%2C15%2C16%2C17%2C19%2C20"
    import_url = f"http://comtrade.un.org/api/get?max=1999&type=C&freq=A&px=HS&ps={year}&r={country_code}&p=all&rg=1&cc={food_code_string}"
    export_url = f"http://comtrade.un.org/api/get?max=1999&type=C&freq=A&px=HS&ps={year}&r={country_code}&p=all&rg=2&cc={food_code_string}"
    import_df = get_comtrade_data(import_url)
    import_df = import_df[import_df['ptTitle'].str.match('World') == False]
    export_df = get_comtrade_data(export_url)
    export_df = export_df[export_df['ptTitle'].str.match('World') == False]
    
    import_treegraph = make_treegraph(import_df, year, "Imports")
    export_treegraph = make_treegraph(export_df, year, "Exports")
    return [import_treegraph, export_treegraph]
    
page_title = st.sidebar.empty()
page_title.header("Comtrade Data Overviews")
st.title("Comtrade Data Overviews")

# Endpoints
country_url = "https://comtrade.un.org/Data/cache/reporterAreas.json"

country_request = requests.get(url=country_url)
country_request.encoding='utf-8-sig'
country_df = pd.json_normalize(country_request.json()["results"])
# st.write(country_df)


# year_list = [item for item in range(2000, date.today().year+1)]

region = st.selectbox(
     'Region of Interest',
     (country_df["text"]))

country_code = country_df.loc[country_df['text'] == region, 'id'].item()

charts = commodity_charts(country_code)
st.plotly_chart(charts[0], use_container_width=True)
st.plotly_chart(charts[1], use_container_width=True)

# # todo run on button click
# if year_string and country_code and commodity_code:
#      if impex == "Imports":
#           request_url = f"https://comtrade.un.org/api/get?max=50000&type=C&freq=A&px=HS&ps={year_string}r={country_code}&p=all&rg=1&cc={commodity_code}"
#      elif impex == "Exports":
#           request_url = f"https://comtrade.un.org/api/get?max=50000&type=C&freq=A&px=HS&ps={year_string}r=all&p={country_code}&rg=1&cc={commodity_code}"

#      print (request_url)
     
#      if impex == "Imports":
#           prep1 = " to "
#           prep2 = " from "
#           region_title = "ptTitle"
#      else: 
#           prep1 = " from "
#           prep2 = " to "
#           region_title = "rtTitle"

#      chart_df = get_comtrade_data(request_url)
#      if len(chart_df) > 0:
#           chart_df = chart_df[["period", region_title, "TradeValue"]]
#           chart_df.set_index(region_title, inplace=True)
#           chart_df.sort_values(by="TradeValue", ascending=[False], inplace=True)
#           st.header(str(commodity_string)+" "+str(impex)+prep1+str(region)+prep2+"the world")
#           st.write(chart_df)
#      else:
#           st.write("No data found for this query")
