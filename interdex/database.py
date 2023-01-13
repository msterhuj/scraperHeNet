import pymongo
from . import get_config

_config = get_config()

client = pymongo.MongoClient(_config.get("mongodb_url"))
db = client[_config.get("mongodb_db")]
