from sqlalchemy.ext.asyncio import AsyncSession
from db_manager.orm_sql import SqlAlchemyBase
from db_manager.models.user import Users
from core.utils.security import hash_password


class UserProcess(SqlAlchemyBase[Users]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, Users)
    
    async def create_user(self, user_data: dict) -> Users:

        ##generate hash password
        user_data["password"] = hash_password(user_data["password"])
        return await self.create(user_data)
    
    async def get_user_by_email(self, email: str) -> Users:
        return await self.get_by_field("email", email)
    
    async def get_user_by_id(self, user_id: int) -> Users:
        return await self.get_by_field("id", user_id)
    
    async def get_all_users(self) -> list[Users]:
        return await self.get_many()
    
    async def update_user(self, user_id: int, user_data: dict) -> Users:
        return await self.update(user_id, user_data)
    
    async def delete_user(self, user_id: int) -> bool:
        return await self.delete(user_id)
