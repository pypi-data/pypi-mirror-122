from typing import Union, List

from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError
from pymongo.results import DeleteResult, UpdateResult, InsertOneResult, InsertManyResult
from src.pagination_utils import BasePaginator, BasePage

DEFAULT_ITEM_KEY = "_id"


def make_objectid() -> ObjectId:
    return ObjectId()


def get_client(db_host, db_port=27017) -> MongoClient:
    return MongoClient(host=db_host, port=db_port)


def get_database(client: MongoClient, db_name: str) -> Database:
    return client[db_name]


def get_collection(database: Database, collection: str) -> Collection:
    return database[collection]


def query_items(collection: Collection, query: dict) -> Cursor:
    return collection.find(query)


def scan_items(collection: Collection) -> Cursor:
    return collection.find()


def update_item(collection: Collection, item_id: Union[str, int], new_values: dict,
                item_key=DEFAULT_ITEM_KEY) -> UpdateResult:
    return collection.update_one(
        {
            f"{item_key}": item_id
        },
        {
            "$set": new_values
        }
    )


def add_item(collection: Collection, item: dict, key_id='_id') -> InsertOneResult:
    try:
        if not key_id == '_id':
            item['_id'] = item[key_id]

        return collection.insert_one(document=item)

    except DuplicateKeyError:
        raise


def delete_item(collection: Collection, item_id: Union[str, int], item_key=DEFAULT_ITEM_KEY) -> DeleteResult:
    return collection.delete_one(
        {
            f"{item_key}": item_id
        },

    )


def get_item(collection: Collection, item_id: Union[str, int], item_key=DEFAULT_ITEM_KEY) -> Cursor:
    return collection.find(
        {
            f"{item_key}": item_id
        }
    )


def get_page_from_collection(collection: Collection, query: dict, limit, last_item_id=None) -> BasePage:
    total_records = collection.find(query).count()

    if last_item_id:
        query.update({"_id": {"$gt": last_item_id}})

    cursor = collection.find(query).limit(limit)

    last_item_id = _get_last_id_from_cursor(cursor=cursor)

    return NewPage(
        cursor=cursor,
        last_id=last_item_id,
        total_items=total_records
    )


def get_pages_from_collection(collection: Collection, query: dict, page_size: int) -> BasePaginator:
    paginator = BasePaginator()
    items = collection.find(query)
    paginator.make_pages(items=items, page_size=page_size)
    return paginator


def _get_last_id_from_cursor(cursor):
    _cursor = clone_item(cursor)
    cursor_list = list(_cursor)
    try:
        return cursor_list[len(cursor_list) - 1].get("_id")

    except IndexError:
        return None


def _get_cursor_count(cursor):
    _cursor = clone_item(cursor)
    cursor_list = list(_cursor)
    return len(cursor_list)


def add_many_items(collection: Collection, items: List[dict], ordered: bool = True) -> InsertManyResult:
    return collection.insert_many(
        documents=items,
        ordered=ordered
    )


def check_for_items(collection: Collection):
    collection.aggregate()
