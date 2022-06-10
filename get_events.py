import requests, dotenv, time, os, json, logging, datetime
from dotenv import load_dotenv
from pymongo import MongoClient, mongo_client

load_dotenv()
API_KEY = os.getenv('API_KEY')

contractAddress = '0x79FCDEF22feeD20eDDacbB2587640e45491b757f'

# Connect to databse
client = MongoClient('mongodb://localhost:27017')
db = client.mfers_collection
db.mfer

# Setup Logging
logging.basicConfig(filename='tasks.log', level=logging.INFO)

def get_event(token_id):
    url = f"https://api.opensea.io/api/v1/events?token_id={token_id}&asset_contract_address={contractAddress}&collection_slug=mfers&event_type=transfer"

    headers = { 
    "Accept": "application/json",
    "X-API-KEY": API_KEY
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    return data

for i in range(0, 10):
    time.sleep(1)
    token_id = i + 1
    data = get_event(token_id)
    db.mfer.insert_one(data)

    print(f'{token_id} tokens completed')
    logging.info(f'{token_id} finished at {datetime.datetime.now()}')
    
