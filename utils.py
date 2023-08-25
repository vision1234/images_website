import redis
from pymongo import MongoClient
import os
from config import *





def get_conn():
    connection_string = f"mongodb://{username}:{password}@{hostname}:{port}/"
    conn = MongoClient(connection_string)
    return conn


def get_collect(conn, coll_name):
    return conn.get_database(database).get_collection(coll_name)


def add_one_data(coll, data: dict):
    coll.insert_one(data)


def select_by_cate(coll, cate, one=False):
    if one:
        return coll.find_one({'cate': cate})
    else:
        return list(coll.find({'cate': cate}).sort('create_time', -1))


def select_by_tag(coll, tag, one=False):
    if one:
        return coll.find_one({'cate': tag})
    else:
        return list(coll.find({'tag': tag}))


def random_img(coll, num):
    num_documents_to_get = num

    # 使用聚合框架进行随机抽样
    pipeline = [
        {"$sample": {"size": num_documents_to_get}}
    ]

    # 执行聚合查询并获取随机抽样的文档
    random_documents = list(coll.aggregate(pipeline))
    return random_documents


def get_redis_cates():
    redis_client = redis.Redis(host=hostname, port=r_port, db=r_db, password=r_password)
    data = [k.decode('utf-8') for k in list(redis_client.lrange(r_cate_key, 0, -1))]
    return data


def get_redis_tags():
    redis_client = redis.Redis(host=hostname, port=r_port, db=r_db, password=r_password)
    data = list(redis_client.smembers(r_tag_key))
    return data


def add_redis_tags(data):
    redis_client = redis.Redis(host=hostname, port=r_port, db=r_db, password=r_password)
    for d in data:
        redis_client.sadd(r_tag_key, d)
