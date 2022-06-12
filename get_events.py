import requests, time, os, json, logging, datetime
from dotenv import load_dotenv
from pymongo import MongoClient, mongo_client

load_dotenv()
API_KEY = os.getenv('API_KEY')

# Connect to databse
client = MongoClient('mongodb://localhost:27017')
db = client.azuki_events
db.azuki

# logging
logging.basicConfig(filename='tasks.log', level=logging.INFO)

# We want to get all events within the following dates: 12/1/21 - 6/1/22, the API takes dates in Unix Epoch
# The API also returns limited data so to get it all without exausting all requests we will need to use Cursor Pagination

def get_events(cursor, assetContract = '0xED5AF388653567Af2F388E6224dC7C4b3241C544', eventType = 'successful', beforeDate = '1655042474', afterDate = '1641171674', **kwargs):
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
result = list()
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
    time.sleep(1)