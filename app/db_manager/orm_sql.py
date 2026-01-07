from typing import (
    Any,
    Dict,
    Generic,
    Iterable,
    List,
    Optional,
    Type,
    TypeVar,
)
from uuid import UUID

import logging
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)


class SqlAlchemyError(Exception):
    """Base exception for PostgreSQL errors"""


class SqlAlchemyBase(Generic[ModelType]):
    """
    Generic async repository for PostgreSQL using SQLAlchemy ORM.
    This class must NEVER contain business logic.
    """

    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self.session = session
        self.model = model

    # Read Operations

    async def get_by_id(self, id: UUID | Any) -> Optional[ModelType]:
        try:
            stmt = select(self.model).where(self.model.id == id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as exc:
            logger.info("DB error in get_by_id")
            raise SqlAlchemyError from exc

    async def get_one(self, filters: Dict[str, Any]) -> Optional[ModelType]:
        try:
            stmt = select(self.model)
            for field, value in filters.items():
                stmt = stmt.where(getattr(self.model, field) == value)

            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as exc:
            logger.info("DB error in get_one")
            raise SqlAlchemyError from exc

    async def get_many(
        self,
        filters: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[ModelType]:
        try:
            stmt = select(self.model)

            if filters:
                for field, value in filters.items():
                    if isinstance(value, Iterable) and not isinstance(value, str):
                        stmt = stmt.where(getattr(self.model, field).in_(value))
                    else:
                        stmt = stmt.where(getattr(self.model, field) == value)

            if offset:
                stmt = stmt.offset(offset)
            if limit:
                stmt = stmt.limit(limit)

            result = await self.session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as exc:
            logger.info("DB error in get_many")
            raise SqlAlchemyError from exc

    async def exists(self, filters: Dict[str, Any]) -> bool:
        record = await self.get_one(filters)
        return record is not None

    # Write Operations

    async def create(self, obj_in: Dict[str, Any]) -> ModelType:
        try:
            db_obj = self.model(**obj_in)
            self.session.add(db_obj)
            await self.session.commit()
            await self.session.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as exc:
            await self.session.rollback()
            logger.info("DB error in create")
            raise SqlAlchemyError from exc

    async def bulk_create(self, objs: List[Dict[str, Any]]) -> List[ModelType]:
        try:
            db_objs = [self.model(**obj) for obj in objs]
            self.session.add_all(db_objs)
            await self.session.commit()
            return db_objs
        except SQLAlchemyError as exc:
            await self.session.rollback()
            logger.info("DB error in bulk_create")
            raise SqlAlchemyError from exc

    async def update_by_id(
        self, id: UUID | Any, values: Dict[str, Any]
    ) -> Optional[ModelType]:
        try:
            stmt = (
                update(self.model)
                .where(self.model.id == id)
                .values(**values)
                .returning(self.model)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one_or_none()
        except SQLAlchemyError as exc:
            await self.session.rollback()
            logger.info("DB error in update_by_id")
            raise SqlAlchemyError from exc

    async def delete_by_id(self, id: UUID | Any) -> bool:
        try:
            stmt = delete(self.model).where(self.model.id == id)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.rowcount > 0
        except SQLAlchemyError as exc:
            await self.session.rollback()
            logger.info("DB error in delete_by_id")
            raise SqlAlchemyError from exc
