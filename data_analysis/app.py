import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

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
    df['event_timestamp'] = pd.to_datetime(df['event_timestamp'])
    df.drop_duplicates(keep='first')

    df.set_index(df['event_timestamp'], inplace=True)
    return df
df = get_data()

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
df_filtered['Owner_Address'] = df['owner_address']
df_filtered['Event Type'] = df['event_type']

df_bayc = pd.DataFrame()
df_cc = pd.DataFrame()
df_mfers = pd.DataFrame()
df_azuki = pd.DataFrame()

# App Body
st.title('NFT Collection Data')

with st.form("Filters"):
    with st.sidebar:
        st.title('Collection Filter')

        start = st.date_input('Select Start Date').strftime('%Y-%m-%dT00:00:00')
        end = st.date_input('Select End Date').strftime('%Y-%m-%dT00:00:00')

        df_filtered = df_filtered.loc[start:end]


        event_filter = st.multiselect('Enter Event Name', event_name)
        df_filtered = df_filtered[(df_filtered['Event Type'].isin(event_filter))]

        st.write('Enter Collection Name')

        azuki = st.checkbox('Azuki', value=False)
        if (azuki):
            df_azuki = df_filtered[df_filtered['Collection Name'] == 'Azuki']
            df_azuki = df_azuki.resample('D').apply({'Owner_Address':'count'})

        bayc  = st.checkbox('BAYC')
        if (bayc):
            df_bayc = df_filtered[df_filtered['Collection Name'] == 'Bored Ape Yacht Club']
            df_bayc = df_bayc.resample('D').apply({'Owner_Address':'count'})

        mfers = st.checkbox('mfers')
        if (mfers):
            df_mfers = df_filtered[df_filtered['Collection Name'] == 'mfers']
            df_mfers = df_mfers.resample('D').apply({'Owner_Address':'count'})

        cc = st.checkbox('Crypto Coven')
        if (cc):
            df_cc = df_filtered[df_filtered['Collection Name'] == 'Crypto Coven']
            df_cc = df_cc.resample('D').apply({'Owner_Address':'count'})

        submitted = st.form_submit_button("Submit")

        # Progress Bar
        my_bar = st.progress(0)

        for percent_complete in range(100):
            time.sleep(0.1)
            my_bar.progress(percent_complete + 1)

fig = plt.figure(figsize=(1, 5))

if (len(df_azuki) > 0):
    plt.plot(df_azuki)
    df_filtered = df_filtered[df_filtered['Collection Name'] == 'Azuki']
if (len(df_bayc) > 0):
    plt.plot(df_bayc)
    df_filtered = df_filtered[df_filtered['Collection Name'] == 'Bored Ape Yacht Club']
if (len(df_mfers) > 0):
    plt.plot(df_mfers)
    df_filtered = df_filtered[df_filtered['Collection Name'] == 'mfers']
if (len(df_cc) > 0):
    plt.plot(df_cc)
    df_filtered = df_filtered[df_filtered['Collection Name'] == 'Crypto Coven']

st.plotly_chart(fig, use_container_width=True)

st.dataframe(df_filtered)

