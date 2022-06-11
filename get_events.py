import requests, dotenv, time, os, json, logging, datetime
from dotenv import load_dotenv
from pymongo import MongoClient, mongo_client

load_dotenv()
API_KEY = os.getenv('API_KEY')

contractAddress = '0x79FCDEF22feeD20eDDacbB2587640e45491b757f'
eventType = 'successful'

# Connect to databse
client = MongoClient('mongodb://localhost:27017')
db = client.mfers_collection
db.mfer

# Setup Logging
logging.basicConfig(filename='tasks.log', level=logging.INFO)

def get_event(token_id, dateTimeEpoch):
    url = f"https://api.opensea.io/api/v1/events?asset_contract_address={contractAddress}&event_type={eventType}&occurred_before={dateTimeEpoch}"

    headers = { 
    "Accept": "application/json",
    "X-API-KEY": API_KEY
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    return data

# Start at 12/1/21
def convertDate(year, month, day):
    dateTimeEpoch = datetime.datetime(year, month, day).timestamp()
    return dateTimeEpoch


for i in range(0, 10):
    time.sleep(1)
    token_id = i + 1
    d = convertDate(2021, 11, 30)
    data = get_event(token_id, d)
    db.mfer.insert_one(data)

    print(f'{token_id} tokens completed')
    logging.info(f'{token_id} finished at {datetime.datetime.now()}')
    
