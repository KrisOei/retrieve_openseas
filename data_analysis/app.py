import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib_venn import venn2

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
df_filtered['Owner_Address'] = df['owner_address']
df_filtered['Event Type'] = df['event_type']

# App Body
st.title('NFT Collection Data')

with st.form("Filters"):
    with st.sidebar:
        st.title('Collection Filter')

        event_filter = st.multiselect('Enter Event Name', event_name)
        df_filtered = df_filtered[(df_filtered['Event Type'].isin(event_filter))]

        collection_filter = st.multiselect('Enter Collection Name', collection_name)
        df_filtered = df_filtered[(df_filtered['Collection Name'].isin(collection_filter))]

        start = st.date_input('Select Start Date').strftime('%Y-%m-%dT00:00:00')
        end = st.date_input('Select End Date').strftime('%Y-%m-%dT00:00:00')

        df_filtered = df_filtered.loc[start:end]

        submitted = st.form_submit_button("Submit")

# Graph
df_ = df_filtered.resample('D').apply({'Owner_Address':'count'})

az = 'Azuki'
ba = 'Bored Ape Yacht Club'
mf = 'mfers'
cc = 'Crypto Coven'

az = df_filtered[df_filtered['Collection Name'] == az].Owner_Address.unique()
ba = df_filtered[df_filtered['Collection Name'] == ba].Owner_Address.unique()
mf = df_filtered[df_filtered['Collection Name'] == mf].Owner_Address.unique()
cc = df_filtered[df_filtered['Collection Name'] == cc].Owner_Address.unique()
iaz_count = az.shape[0]
iba_count = ba.shape[0]
imf_count = mf.shape[0]
icc_count = cc.shape[0]
a = df_filtered[df_filtered['Owner_Address'].isin(df_filtered['Owner_Address'].value_counts()[df_filtered['Owner_Address'].value_counts() > 1].index)].Owner_Address.unique()

df_a = pd.DataFrame()
mf_cc = list()
mf_ba = list()
mf_az = list()
cc_ba = list()
cc_az = list()
ba_az = list()

i = 0
I1 = 0
I2 = 0
I3 = 0
I4 = 0
I5 = 0
I6 = 0
 
for owner in a:
    temp = df_filtered[df_filtered['Owner_Address'] == a[i]]

    temp.reset_index(inplace=True)
    address = temp.Owner_Address[0]

    df_a = df_a.append(temp)

    mf_count = (temp[temp['Collection Name'] == 'mfers'].count())
    mf = mf_count['Collection Name']

    cc_count = (temp[temp['Collection Name'] == 'Crypto Coven'].count())
    cc = cc_count['Collection Name']

    ba_count = (temp[temp['Collection Name'] == 'Bored Ape Yacht Club'].count())
    ba = ba_count['Collection Name']

    az_count = (temp[temp['Collection Name'] == 'Azuki'].count())
    az = az_count['Collection Name']

    if ((mf > 0) & (cc > 0)):
        I1 += 1
        mf_cc.append(address)
    elif ((mf > 0) & (ba > 0)):
        I2 += 1
        mf_ba.append(address)
    elif ((mf > 0) & (az > 0)):
        I3 += 1
        mf_az.append(address)
    elif ((cc > 0) & (ba > 0)):
        I4 += 1
        cc_ba.append(address)
    elif ((cc > 0) & (az > 0)):
        I5 += 1
        cc_az.append(address)
    elif ((ba > 0) & (az > 0)):
        I6 += 1
        ba_az.append(address)
    i += 1

data = {'Azuki': iaz_count, 'Azuki & BAYC': I6 , 'Bored Ape Yacht Club': iba_count, 'BAYC & mfers':I2,'mfers': imf_count, 'mfers & Crypto Coven':I1, 'mfers & Azuki':I3 , 'Crypto Coven':icc_count, 'Crypto Coven & Azuki': I5, 'Crypto Coven & BAYC':I4 }
inter = [I1, I2, I3, I4, I5, I6]

intersection = 0

for el in inter:
    if el > 0:
        intersection = el

fig, ax = plt.subplots()
venn2(subsets = (data[collection_filter[0]], data[collection_filter[1]], intersection), set_labels = (collection_filter[0], collection_filter[1]))


fig2, ax = plt.subplots()
st.pyplot(fig2)
st.write(df_filtered)