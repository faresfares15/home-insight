import pandas as pd
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()


def get_data_frame(delete_id: bool = True, delete_index: bool = True) -> pd.DataFrame:
    try:
        # create a new client and connect to the server
        client = MongoClient(os.environ['MONGODB_URI'], server_api=ServerApi('1'))
        db = client['home-insight']
        print('connected to the db')
        collection = db['properties'].find({'Price': {'$gt': 0}})
        print('finished the query')
        df = pd.DataFrame(list(collection))
        if delete_id:
            del df['_id']
        if delete_index:
            del df['index']
        return df
    except Exception as e:
        print("Got a problem with mongoDB, " + e.__str__())


def save_csv(data_frame: pd.DataFrame, filename: str):
    data_frame.to_csv(filename, header=True, index=False, encoding='utf-8')


def save_to_db(data_frame: pd.DataFrame):
    # Save to the DB when you implement it
    client = MongoClient(os.environ['MONGODB_URI'], server_api=ServerApi('1'))

    db = client['home-insight']
    collection = db['properties']
    data_frame.reset_index(inplace=True)
    data_dict = data_frame.to_dict("records")
    collection.insert_many(data_dict)
