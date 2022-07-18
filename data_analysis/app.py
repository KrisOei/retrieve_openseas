import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

df = pd.read_csv('fourCollections.csv', dtype={'collection_slug': 'str', 'asset_id': 'int', 'asset_name': 'str', 'owner_username': 'str', 'owner_address': 'str', 'event_type': 'str'})

# Clean Data
df.drop('Unnamed: 0.1', axis=1, inplace=True)
df.drop('Unnamed: 0', axis=1, inplace=True)
df.drop('collection_slug', axis=1,inplace=True)
df.drop('asset_contract_date', axis=1, inplace=True)
df['event_timestamp'] = pd.to_datetime(df['event_timestamp']).dt.strftime('%m/%d/%Y %H:%M')
df.drop_duplicates(keep='first')
df = df[df['event_type'] == 'successful']

df.set_index(df['event_timestamp'], inplace=True)

# Filter
df = df[(df['event_timestamp'] > '2022-01-17T10:00:00') & (df['event_timestamp'] < '2022-02-17T12:00:00')]

collection_name = {
    'Azuki': 'Azuki',
    'BAYC': 'Bored Ape Yacht Club',
    'mfers': 'mfers',
    'Crypto Coven': 'Crypto Coven'
}

st.title('NFT Collection Data by Kris Oei')

with st.sidebar:

    date_filter = st.slider('Date', 0, 500001, 10000)

    collection_filter = st.selectbox('Enter Collection Name', collection_name)