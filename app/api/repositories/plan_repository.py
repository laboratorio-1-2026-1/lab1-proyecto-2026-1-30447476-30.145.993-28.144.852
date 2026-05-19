from typing import List, Optional

from sqlalchemy.orm import Session

from app.api.models.plan import Plan


class PlanRepository:
    @staticmethod
    def get_by_id(db: Session, plan_id: int) -> Optional[Plan]:
        return db.query(Plan).filter(Plan.id == plan_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Plan]:
        return db.query(Plan).offset(skip).limit(limit).all()


plan_repository = PlanRepository()
