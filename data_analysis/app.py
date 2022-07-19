import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

@st.cache
def get_data():
    path = 'fourCollections.csv'
    df = pd.read_csv(path, dtype={'collection_slug': 'str', 'asset_id': 'int', 'asset_name': 'str', 'owner_username': 'str', 'owner_address': 'str', 'event_type': 'str'})
    # Clean Data
    df.drop('Unnamed: 0.1', axis=1, inplace=True)
    df.drop('asset_id', axis=1, inplace=True)
    df.drop('Unnamed: 0', axis=1, inplace=True)
    df.drop('collection_slug', axis=1,inplace=True)
    df.drop('asset_contract_date', axis=1, inplace=True)
    df['event_timestamp'] = pd.to_datetime(df['event_timestamp']).dt.strftime('%m/%d/%Y %H:%M')
    df.drop_duplicates(keep='first')

    df.set_index(df['event_timestamp'], inplace=True)
    return df
df = get_data()

@st.cache
def collection_name():
    collection_name = {
        'Azuki': 'Azuki',
        'Bored Ape Yacht Club': 'Bored Ape Yacht Club',
        'mfers': 'mfers',
        'Crypto Coven': 'Crypto Coven'
    }
    return collection_name
collection_name = collection_name()

@st.cache
def event_name():
    event_name = {
        'created': 'created',
        'successful': 'successful',
        'cancelled': 'cancelled',
        'bid_entered': 'bid_entered',
        'bid_withdrawnn': 'bid_withdrawn',
        'transfer': 'transfer',
        'approve': 'approve',
        'offer_entered': 'offer_entered'
    }
    return event_name
event_name = event_name()

# Filter
df_filtered = pd.DataFrame()
df_filtered['Collection Name'] = df['collection_name']
df_filtered['Asset Name'] = df['asset_name']
df_filtered['Username'] = df['owner_username']
df_filtered['Owner Address'] = df['owner_address']
df_filtered['Event Type'] = df['event_type']

# App Body
st.title('NFT Collection Data')

with st.form("Filters"):
    with st.sidebar:

        event_filter = st.multiselect('Enter Event Name', event_name)
        df_filtered = df_filtered[(df_filtered['Event Type'].isin(event_filter))]

        collection_filter = st.multiselect('Enter Collection Name', collection_name)
        df_filtered = df_filtered[(df_filtered['Collection Name'].isin(collection_filter))]

        submitted = st.form_submit_button("Submit")

st.write(df_filtered)
st.write(df_filtered)
st.write(event_filter)
st.write(collection_filter)

#df = df[(df['event_timestamp'] > '2022-01-17T10:00:00') & (df['event_timestamp'] < '2022-02-17T12:00:00')]
#df = df[df['event_type'] == 'successful']
