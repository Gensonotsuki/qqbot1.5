#!/home/qbprjENV/bin/python
import pymongo
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker


def link_local_mongo(host='127.0.0.1', port=27017):
    connectionObject = pymongo.MongoClient(host=host, port=port)
    return connectionObject


def linksqlengine():
    engine = create_engine('')
    session = sessionmaker(bind=engine, autocommit=True, autoflush=False)()
    return session


def savesth(sth):
    engine = create_engine('')
    meta = MetaData(engine)
    conn = engine.connect()
    savenikename = Table('nicename', meta, autoload=True)
    savenikename_insert = savenikename.insert()
    conn.execute(savenikename_insert, sth)
    return True


def xxxx(self):
    return


def xxxxx(self):
    return


def xxxxxx(self):
    return


def xxxxxxx(self):
    return
