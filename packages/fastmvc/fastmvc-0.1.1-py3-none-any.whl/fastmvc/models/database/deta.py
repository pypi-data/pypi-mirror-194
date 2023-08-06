from deta import Deta
from fastmvc.models.database._base import BaseDataModel, DBModelMetaClass


class DetaModelMeta(DBModelMetaClass):

    @staticmethod
    def handle_db_property(cls):
        if cls._db:
            return cls._db
        cls._db = Deta().Base(cls.__db_name__)
        return cls._db
    

class DetaBase(BaseDataModel, metaclass=DetaModelMeta):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def get(cls, key):
        item = cls.__db__.get(key)
        return cls.parse_obj(item)
    
    @classmethod
    def get_all(cls):
        for record in cls.__db__.fetch().items:
            yield cls.parse_obj(record)
    
    @classmethod
    def delete_key(cls, key):
        cls.__db__.delete(key)

    @classmethod
    def query(cls, statement):
        for record in cls.__db__.fetch(statement).items:
            yield cls.parse_obj(record)

    def update(self, update_data: dict):
        for k, v in update_data.items():
            if k in self.__dict__:
                setattr(self, k, v)
        self.save()
    
    @classmethod
    def _db_put(cls, data, expire_in, expire_at):
        return cls.__db__.put(data, expire_in=expire_in, expire_at=expire_at)
    
    def save(self, expire_in: int or None = None, expire_at: int or None = None):
        """Saves the record to the database. Behaves as upsert, will create
        if not present. Database key will then be set on the object."""
        saved = self._db_put(self.dict(), expire_in, expire_at)
        self.key = saved["key"]
