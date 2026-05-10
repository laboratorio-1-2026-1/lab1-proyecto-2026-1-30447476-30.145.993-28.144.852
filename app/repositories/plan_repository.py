from app.models.plan import Plan 
from app.repositories.base_repository import BaseRepository 
 
class PlanRepository(BaseRepository): 
    def __init__(self): 
        super().__init__(Plan) 
