from typing import List

import pymongo

from tubetone import constants
from tubetone.models import AnalysisToneTube

__mongo_client = pymongo.MongoClient(
    constants.DB_URL,
    connectTimeoutMS=5000, socketTimeoutMS=3000, tlsInsecure=True)


def get_playlist_tones(playlist_id: str) -> List[dict]:
    db = __mongo_client.get_database(constants.DB_NAME)
    videos_collection = db[constants.COLLECTION_VIDEOS]

    projection = {"tone": "$tone_analysis.tone", "publish_date": "$publish_date", "playlist_id": "$playlist_id",
                  "video_id": "$video_id", "views": "$views", "duration": "$duration"}

    vids = videos_collection.aggregate([{"$match": {
        "playlist_id": playlist_id
    }}, {"$project": projection}, {"$sort": {"publish_date": 1}}])

    return list(vids)


def get_playlist_videos_for_analysis(playlist_id: str) -> List[AnalysisToneTube]:
    """
    Returns playlist videos without texts itself.

    :param playlist_id:
    :return:
    """
    db = __mongo_client.get_database(constants.DB_NAME)
    videos_collection = db[constants.COLLECTION_VIDEOS]

    projection = dict(_id=0, full_text=0, transcripts=0)

    # TODO: if there is mych videos, this should be reworked, same for save
    vids = videos_collection. \
        find({"playlist_id": playlist_id}, projection). \
        sort([("publish_date", pymongo.ASCENDING)]).limit(5000)

    tubes = []
    for vid in vids:
        tbt: AnalysisToneTube = AnalysisToneTube.from_dict(vid)
        tubes.append(tbt)
    return tubes
