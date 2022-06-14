import requests, time, os, json, logging, datetime
from dotenv import load_dotenv
from pymongo import MongoClient, mongo_client

load_dotenv()
API_KEY = os.getenv('API_KEY')

# Connect to databse
client = MongoClient('mongodb://localhost:27017')
db = client.witches_events
db.witch

# logging
logging.basicConfig(filename='tasks.log', level=logging.INFO)

# We want to get all events within the following dates: 12/1/21 - 6/1/22, the API takes dates in Unix Epoch
# The API also returns limited data so to get it all without exausting all requests we will need to use Cursor Pagination

def get_events(cursor, assetContract = '0x5180db8F5c931aaE63c74266b211F580155ecac8', eventType = 'successful', beforeDate = '1655061903', afterDate = '1636140303', **kwargs):
    url = f"https://api.opensea.io/api/v1/events?asset_contract_address={assetContract}&event_type={eventType}&occurred_before={beforeDate}&occurred_after={afterDate}&cursor={cursor}"

    headers = {
    "Accept": "application/json",
    "X-API-KEY": API_KEY
    }

    response = requests.get(url, headers=headers).text
    response = json.loads(response)
    return response

run = True
next = ''
i = 0

while run:
    response = get_events(cursor=next)
    db.azuki.insert_one(response)
    i += 1

# Add page logger so that we know where we left off
    print(f'Page {i} has been gotten')
    logging.info(f'Task {next} has been completed at {datetime.datetime.now()}')

    # Break Condition
    if response['next'] is None:
        run = False
        print(f'Completed at {datetime.datetime.now()}')
    else:
        next = response['next']
    time.sleep(.5)