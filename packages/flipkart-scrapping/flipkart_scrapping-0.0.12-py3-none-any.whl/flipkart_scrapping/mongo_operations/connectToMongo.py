import pymongo
from pathlib import Path
import os
import re
from bson.objectid import ObjectId

class connectMongo:

    def __init__(self):
        self.__config_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'config/mongo.cfg'))
        self.__username = None
        self.__password = None

    def setUser(self, username):
        self.__username = username    

    def getUserName(self):
        return self.__username

    def setPassword(self, password):
        self.__password = password

    def getPassword(self):
        return self.__password

    def getConfigFile(self):
        return self.__config_file

    def __get_mongo_config(self):
        config_file = self.getConfigFile()
        with open(config_file, "r") as config:
            line = config.read().strip()
            for _c, _f in zip(["USER", "PASSWORD"], [self.setUser, self.setPassword]):
                regex_p = re.compile(f"{_c}:(.*)")
                _f(regex_p.search(line).group(1))                      

    def connect(self, username = None, password = None):
        try:
            if username == None:
                self.__get_mongo_config()
                username, password = self.getUserName(), self.getPassword()
            print("Connecting to mongo client")
            conn_string = f"mongodb+srv://{username}:{password}@cluster0.ca04m.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            client = pymongo.MongoClient(conn_string)
            return client
        except Exception as e:
            print(str(e))

    def close(self, client):
        client.close()

