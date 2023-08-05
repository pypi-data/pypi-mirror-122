from dataclasses import asdict

import pymongo
from tubetone import constants
from tubetone import models

__mongo_client = pymongo.MongoClient(
    constants.DB_URL,
    connectTimeoutMS=5000, socketTimeoutMS=3000, tlsInsecure=True)


def clear_playlist_data(playlist_id: str):
    db = __mongo_client.get_database(constants.DB_NAME)
    videos_collection = db[constants.COLLECTION_VIDEOS]
    videos_collection.delete_many({"playlist_id": playlist_id})


def save_video_data(data: models.ToneTube):
    db = __mongo_client.get_database(constants.DB_NAME)
    videos_collection = db[constants.COLLECTION_VIDEOS]

    print(f'saving {data.title}...')
    result = videos_collection.update_one({'video_id': data.video_id},
                                          {'$set': asdict(data)},
                                          upsert=True)
    # videos_collection.insert_one(data)
    print(f'done saving {data.title}...{result}')
