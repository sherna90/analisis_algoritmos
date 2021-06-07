import streamlit as st
import pandas as pd 

import json
import random
import pydeck as pdk

@st.cache(persist=True)
def load_nodes(path):
    df=pd.read_csv(path)
    df.rename({'X':'lon','Y':'lat'},axis='columns',inplace=True)
    return df

@st.cache(persist=True)
def load_data(path):
    df=pd.read_csv(path, encoding = 'utf-8',dtype={'InputID':'string','TargetID':'string','Distance':float}) 
    df['InputID'] = df['InputID'].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii'))
    df['TargetID'] = df['TargetID'].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii'))
    #df['TargetID']=df['TargetID'].astype('category')
    #df['InputID']=df['InputID'].astype('category')
    return df

with open('data/maule_caminos.geojson', 'r') as read_file:
    caminos_data = json.load(read_file)

dist_path='data/distancias_maule.csv'
edge_data=load_data(dist_path)
nodes_path='data/comunas_maule.csv'
node_data=load_nodes(nodes_path)

merged_data=edge_data.merge(node_data,left_on='InputID',right_on='Comuna')
merged_data=merged_data.merge(node_data,left_on='TargetID',right_on='Comuna')

merged_data=merged_data[['InputID','TargetID','lon_x','lat_x','lon_y','lat_y']]
merged_data['InputLoc']='['+merged_data['lon_x'].map(str)+','+merged_data['lat_x'].map(str)+']'
merged_data['TargetLoc']='['+merged_data['lon_y'].map(str)+','+merged_data['lat_y'].map(str)+']'
print(merged_data.head())

nodes_layer = pdk.Layer(
    "ScatterplotLayer",
    data=node_data[['lon','lat']],
    get_position="[lon, lat]",
    stroked=True,
    filled=True,
    radius_scale=10,
    radius_min_pixels=5,
    radius_max_pixels=60,
    line_width_min_pixels=1,
    get_fill_color=[252, 136, 3],
    get_line_color=[255,0,0],
    tooltip="test test",
)
geojson_layer = pdk.Layer(
        "GeoJsonLayer",
        data=caminos_data,
        stroked=False,
        filled=True,
        extruded=True,
        wireframe=True,
        get_line_color=[255,0,0],
    )

line_layer = pdk.Layer(
      "LineLayer",
      data= merged_data[['InputLoc','TargetLoc']],
      get_width=100,
      get_source_position= "InputLoc",
      get_target_position= "TargetLoc",
      highlight_color=[255, 255, 0],
      pickable=True
    )

# Set the viewport location
view_state = pdk.ViewState(
    longitude=node_data['lon'].mean(), latitude=node_data['lat'].mean(), zoom=7, min_zoom=1, max_zoom=20, pitch=40.5, bearing=-27.36
)
layers=[nodes_layer,line_layer]
# Combined all of it and render a viewport
r = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    layers=layers,
    initial_view_state=view_state
)
st.dataframe(edge_data)  # Same as st.write(df)
st.pydeck_chart(r)