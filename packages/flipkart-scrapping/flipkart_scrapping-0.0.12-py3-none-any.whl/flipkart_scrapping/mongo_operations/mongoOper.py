from connectToMongo import connectMongo
from insertIntoMongo import insertMongoDoc


class mongoOperations:

    def __init__(self) -> None:
        self._id = None
        self._connection = None
        self._insertMongoDoc = None
        self.coll = "PRODUCT_COLLECTION"
        self.__id = None

    def connect(self):
        self._connection = connectMongo().connect()
        self._insertMongoDoc = insertMongoDoc(self._connection)

    def insert(self, doc):
        self.__id = self._insertMongoDoc.updateDocs(coll=self.coll, id=None,  doc=doc)

    def update(self, doc):
        self._insertMongoDoc.updateDocs(coll=self.coll, id=self.__id,  doc=doc)

    def close(self):
        self._connection.close(self._connection)
    