from app.check.dto import Check as CheckDto
from app.db.dependencies.db import DbSession
from app.db.models.user import User


class CheckService:

    def __init__(
        self,
        db: DbSession,
    ):
        self.db = db

    async def create(self, check: CheckDto, user: User):
        
        return {"status": "ok"}
