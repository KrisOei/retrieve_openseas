import requests, time, os, json, logging, datetime
from dotenv import load_dotenv
from pymongo import MongoClient, mongo_client

load_dotenv()
API_KEY = os.getenv('API_KEY')

# Connect to databse
client = MongoClient('mongodb://localhost:27017')
db = client.BAYC_events
db.apes

# logging
logging.basicConfig(filename='tasks.log', level=logging.INFO)

def get_events(cursor, eventType, assetContract = '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D', **kwargs):
    url = f"https://api.opensea.io/api/v1/events?asset_contract_address={assetContract}&event_type={eventType}&cursor={cursor}"

    headers = {
    "Accept": "application/json",
    "X-API-KEY": API_KEY
    }

    response = requests.get(url, headers=headers).text
    response = json.loads(response)
    return response

# Openseas event types excluding offers since the data is too much
events = ['created', 'successful', 'cancelled', 'bid_entered', 'bid_withdrawn', 'transfer', 'approve']

# Gets data for event
def get_data(ev):
    run = True
    next = ''
    i = 0   
    while run:
        response = get_events(cursor=next, eventType=ev)
        db.apes.insert_one(response)
        i += 1

    # Add page logger so that we know where we left off
        print(f'Page {i} has been gotten')
        logging.info(f'Task {next} has been completed at {datetime.datetime.now()}')

    # Break Condition
        if response['next'] is None:
            run = False
            print(f'Task {ev} completed at {datetime.datetime.now()}')
        else:
            next = response['next']
        time.sleep(.33)

# Uses the get data function per event type
for ev in events:
    get_data(ev)

print('All tasks complete')