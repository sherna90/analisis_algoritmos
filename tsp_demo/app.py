import streamlit as st
import pandas as pd 

import json
import random
import pydeck as pdk

@st.cache(persist=True)
def load_nodes(path):
    df=pd.read_csv(path,usecols=['X','Y','Comuna'])
    return df

@st.cache(persist=True)
def load_data(path):
    df=pd.read_csv(path, encoding = 'utf-8',dtype={'InputID':'string','TargetID':'string','Distance':float}) 
    df['InputID'] = df['InputID'].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii'))
    df['TargetID'] = df['TargetID'].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii'))
    #df['TargetID']=df['TargetID'].astype('category')
    #df['InputID']=df['InputID'].astype('category')
    return df

dist_path='data/distancias_maule.csv'
data=load_data(dist_path)
nodes_path='data/comunas_maule.csv'
node_data=load_nodes(nodes_path)

nodes_layer = pdk.Layer(
    "HexagonLayer",
    data=node_data[['X','Y']],
    get_position="[lon, lat]",
    auto_highlight=True,
    elevation_scale=50,
    pickable=True,
    elevation_range=[0, 100],
    extruded=True,
    coverage=0.5,
)

# Set the viewport location
view_state = pdk.ViewState(
    longitude=node_data['X'].mean(), latitude=node_data['Y'].mean(), zoom=5, min_zoom=1, max_zoom=15, pitch=40.5, bearing=-27.36
)
layers=[nodes_layer]
# Combined all of it and render a viewport
r = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    layers=layers,
    initial_view_state=view_state
)
st.dataframe(data)  # Same as st.write(df)
st.pydeck_chart(r)