import re
import pymongo
import os
import re
import json
from bson.objectid import ObjectId
from connectToMongo import connectMongo
import datetime

class insertMongoDoc:

    def __init__(self, client):
        self.__client = client
        self.__config_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'config/mongo.cfg'))
        self.__database = None

    def getConfigFile(self):
        return self.__config_file

    def setDB(self, DB):
        self.__database = DB

    def getDB(self):
        return self.__database

    def __getClient(self):
        return self.__client

    def __get_db(self):
        config_file = self.getConfigFile()
        with open(config_file, "r") as config:
            line = config.read().strip()
            for _c, _f in zip(["DB"], [self.setDB]):
                regex_p = re.compile(f"{_c}:(.*)")
                _f(regex_p.search(line).group(1)) 
        return self.getDB()

    def __get_coll_obj(self, coll):
        db = self.__get_db()
        client = self.__getClient()
        #print(client, db)
        db = client[db]
        coll = db[coll]
        return coll


    def insertProduct(self, coll, doc):
        #if isinstance(doc) == 'str':
        #    doc = json.loads(doc)
        coll = self.__get_coll_obj(coll)
        #print(coll)
        doc['created_ts'] = datetime.datetime.now().isoformat()
        id = coll.insert_one(doc).inserted_id
        return id

    def f2(self, coll, id, doc):
        print("f2")
        return 1

    def updateDocs(self, coll, id, doc):
        if doc is None:
            return False
        if id is None:
            print("Inserting into DB")
            return self.insertProduct(coll, doc)
        print(f"Updating doc for id: {id}")
        #if isinstance(doc) == 'str':
        #    doc = json.loads(doc)
        coll = self.__get_coll_obj(coll)
        print("doc")
        print(doc)
        coll.update({'_id': ObjectId(f'{id}')}, {"$push": {"reviews" : {"$each" :doc}}})

