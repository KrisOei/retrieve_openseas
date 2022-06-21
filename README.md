# retrieve_openseas

1) Create a .env with 'API_KEY'
2) Open get_events.py
3) Enter the following information as it pretains to the information trying to be retreived: 'assetContract' - This will fetch the following events ['created', 'successful', 'cancelled', 'bid_entered', 'bid_withdrawn', 'transfer', 'approve']
4) Once completed to get the first 100+ offer information for each day you will need to run a seperate file named get_offers.ipybn
5) Enter the following information into the file: start_date, end_date, assetContract
6) Running the file witll retreive all information within the specified date range using pagination for the first 10 pages
