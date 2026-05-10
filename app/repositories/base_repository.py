from app.core.database import SessionLocal 
 
class BaseRepository: 
    def __init__(self, model): 
        self.model = model 
 
    def _get_db(self): 
        return SessionLocal() 
 
    def create(self, **kwargs): 
        db = self._get_db() 
        try: 
            instance = self.model(**kwargs) 
            db.add(instance) 
            db.commit() 
            db.refresh(instance) 
            return instance 
        finally: 
            db.close() 
 
    def get_by_id(self, id): 
        db = self._get_db() 
        try: 
            return db.query(self.model).filter(self.model.id == id).first() 
        finally: 
            db.close() 
 
    def get_all(self, skip=0, limit=100): 
        db = self._get_db() 
        try: 
            return db.query(self.model).offset(skip).limit(limit).all() 
        finally: 
            db.close() 
 
    def update(self, id, **kwargs): 
        db = self._get_db() 
        try: 
            instance = db.query(self.model).filter(self.model.id == id).first() 
            if instance: 
                for key, value in kwargs.items(): 
                    setattr(instance, key, value) 
                db.commit() 
                db.refresh(instance) 
            return instance 
        finally: 
            db.close() 
 
    def delete(self, id): 
        db = self._get_db() 
        try: 
            instance = db.query(self.model).filter(self.model.id == id).first() 
            if instance: 
                db.delete(instance) 
                db.commit() 
                return True 
            return False 
        finally: 
            db.close() 
