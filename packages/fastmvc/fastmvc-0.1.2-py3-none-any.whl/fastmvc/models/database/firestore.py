from google.cloud import firestore
from fastmvc.models.database._base import BaseDataModel, DBModelMetaClass


class FirestoreModelMeta(DBModelMetaClass):

    @staticmethod
    def handle_db_property(cls):
        if cls._db:
            return cls._db
        cls._db = firestore.Client().collection(cls.__db_name__)
        return cls._db
    

class Firestore(BaseDataModel, metaclass=FirestoreModelMeta):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def __parsed(cls, record):
        r = record.to_dict()
        r.update({'key': record.id})
        return cls.parse_obj(r)

    @classmethod
    def get(cls, key):
        doc_ref = cls.__db__.document(key)
        doc = doc_ref.get()
        if doc.exists:
            return cls.__parsed(doc)
        else:
            return None
    
    @classmethod
    def get_all(cls):
        for record in cls.__db__.get():
            yield cls.__parsed(record)
    
    @classmethod
    def delete_key(cls, key):
        cls.__db__.document(key).delete()

    @classmethod 
    def query(cls, statement: dict):
        query = cls.__db__
        for k, v in statement.items():
            query = query.where(k, '==', v)
        for record in query.stream():
            yield cls.__parsed(record)
            
    @classmethod
    def _edit(cls, key, data):
        doc_ref = cls.__db__.document(key)
        return doc_ref.update(data)

    def update(self, update_data: dict):
        result = self._edit(key=self.key, data=update_data)

    @classmethod 
    def _put(cls, key, data):
        doc_ref = cls.__db__.document(key)
        doc_ref.set(data)
        return doc_ref.id
    
    def save(self):
        data = self.dict()
        key = data.pop('key', None)
        new_doc_id = self._put(key, data)
        self.key = new_doc_id
