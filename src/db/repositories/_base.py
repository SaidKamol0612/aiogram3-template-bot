import logging
from typing import (
    TypeVar,
    Generic,
    Type,
    Dict,
    Any,
    Optional,
    List,
)

from sqlalchemy import select, inspect, Select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


log = logging.getLogger(__name__)

# `M` represents a SQLAlchemy model class that inherits from Base
M = TypeVar("M", bound=DeclarativeBase)


class BaseRepository(Generic[M]):
    """Universal asynchronous repository for SQLAlchemy models."""

    OPS: Dict[str, Any] = {
        "eq": lambda c, v: c == v,
        "ne": lambda c, v: c != v,
        "lt": lambda c, v: c < v,
        "lte": lambda c, v: c <= v,
        "gt": lambda c, v: c > v,
        "gte": lambda c, v: c >= v,
        "like": lambda c, v: c.like(v),
        "ilike": lambda c, v: c.ilike(v),
        "in": lambda c, v: c.in_(v if isinstance(v, (list, tuple)) else [v]),
    }

    def __init__(
        self,
        model: Type[M],
        session: Optional[AsyncSession] = None,
    ):
        """
        Initialize repository.

        Args:
            model: SQLAlchemy model class (e.g. `User`, `Item`).
            session: Optional AsyncSession instance.
                You can pass it here or provide one at method call time.
        """

        self.model = model
        self._session = session

    def _get_session(self, session: Optional[AsyncSession]) -> AsyncSession:
        """
        Resolve the active session.

        If a session was bound at repository initialization,
        it will be used as default; otherwise a session
        must be explicitly passed to the method.
        """
        if session is not None:
            return session
        if self._session is not None:
            return self._session
        raise ValueError(
            f"{self.__class__.__name__} requires an active AsyncSession "
            "either passed at init or per method call."
        )

    async def create(
        self,
        data: Dict[str, Any],
        session: Optional[AsyncSession] = None,
        *,
        commit: bool = True,
        refresh: bool = True,
    ) -> M:
        """
        Create and persist a new record in the database.

        Args:
            data: Dictionary of model fields and values.
            session: Optional active AsyncSession (fallback to internal one if provided).
            commit: Whether to automatically commit after adding the record.
            refresh: Whether to refresh the instance after commit to load defaults.

        Returns:
            The newly created model instance.

        Raises:
            IntegrityError: If a database constraint is violated.
        """
        session = self._get_session(session)
        instance = self.model(**data)
        session.add(instance)

        try:
            if commit:
                await session.commit()
            if refresh:
                await session.refresh(instance)
            log.info("Created %s: %s", self.model.__name__, data)
            return instance

        except IntegrityError as e:
            await session.rollback()
            log.warning(
                "IntegrityError while creating %s: %s | Data: %s",
                self.model.__name__,
                e,
                data,
            )
            raise

    def _apply_filters(self, stmt: Select, filters: Optional[Dict[str, Any]]) -> Select:
        """
        Apply filters safely to a SQLAlchemy SELECT statement.
        Example filters:
            {"price__gte": 100, "name__ilike": "%Book%"}
        """
        if not filters:
            return stmt

        model_fields = set(inspect(self.model).columns.keys())

        for key, value in filters.items():
            field, *op = key.split("__")
            op = op[0] if op else "eq"

            if field not in model_fields:
                raise ValueError(f"Invalid field '{field}' for {self.model.__name__}")

            if op not in self.OPS:
                raise ValueError(f"Unsupported operator '{op}' for field '{field}'")

            column = getattr(self.model, field)
            stmt = stmt.where(self.OPS[op](column, value))

        return stmt

    def _build_query(
        self,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Select:
        """
        Build a SELECT statement with filters, sorting, and pagination.
        Automatically excludes soft-deleted rows if `is_deleted` exists.
        """
        stmt = select(self.model)

        # Skip deleted rows
        if hasattr(self.model, "is_deleted"):
            stmt = stmt.where(self.model.is_deleted.is_(False))  # type: ignore

        stmt = self._apply_filters(stmt, filters)

        # Sorting
        if order_by:
            desc = order_by.startswith("-")
            field = order_by.lstrip("-")
            if field not in inspect(self.model).columns:
                raise ValueError(
                    f"Invalid order_by field '{field}' for {self.model.__name__}"
                )
            column = getattr(self.model, field)
            stmt = stmt.order_by(column.desc() if desc else column.asc())

        # Pagination
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)

        return stmt

    async def get_all(
        self,
        filters: Optional[Dict[str, Any]] = None,
        session: Optional[AsyncSession] = None,
        *,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[M]:
        """
        Retrieve all records matching the given filters.

        Args:
            filters: Optional filtering dictionary.
            session: Active database session.
            order_by: Field to sort by (prefix with "-" for DESC).
            limit: Maximum number of records.
            offset: Number of records to skip.

        Returns:
            List of model instances.
        """
        session = self._get_session(session)
        stmt = self._build_query(filters, order_by, limit, offset)
        result = await session.scalars(stmt)
        return result.all()  # type: ignore

    async def get(
        self,
        filters: Optional[Dict[str, Any]] = None,
        session: Optional[AsyncSession] = None,
    ) -> Optional[M]:
        """
        Retrieve the first record matching filters.

        Args:
            filters: Dictionary of filtering conditions.
            session: Optional active AsyncSession.

        Returns:
            The first matching model instance or None.
        """
        session = self._get_session(session)
        stmt = self._build_query(filters, limit=1)
        result = await session.scalars(stmt)
        return result.first()

    async def update(
        self,
        model_id: int,
        data: Dict[str, Any],
        session: Optional[AsyncSession] = None,
    ) -> Optional[M]:
        """
        Update an existing record by its primary key ID.

        Args:
            model_id: The ID of the record to update.
            data: A dictionary of fields and values to update.
            session: Optional active AsyncSession.

        Returns:
            The updated model instance, or None if not found.

        Raises:
            IntegrityError: If database constraints are violated.
            ValueError: If attempting to update non-existent fields.
        """
        session = self._get_session(session)

        # Fetch instance by ID
        instance = await self.get({"id": model_id}, session=session)
        if not instance:
            log.info("No %s found with id=%s", self.model.__name__, model_id)
            return None

        model_fields = set(inspect(self.model).columns.keys())

        # Apply only valid fields
        for field, value in data.items():
            if field not in model_fields:
                raise ValueError(
                    f"Field '{field}' does not exist on {self.model.__name__}"
                )
            setattr(instance, field, value)

        try:
            await session.commit()
            await session.refresh(instance)
            log.info("Updated %s (id=%s)", self.model.__name__, model_id)
            return instance

        except IntegrityError as e:
            await session.rollback()
            log.warning(
                "IntegrityError while updating %s (id=%s): %s",
                self.model.__name__,
                model_id,
                e,
            )
            raise

    async def delete(
        self,
        model_id: int,
        *,
        session: Optional[AsyncSession] = None,
        soft: bool = False,
    ) -> bool:
        """
        Delete a record by its primary key ID.

        Supports both hard and soft deletion depending on the model and parameters.

        Args:
            model_id: Primary key of the record to delete.
            session: Optional active AsyncSession.
            soft: If True, mark record as deleted using 'is_deleted' instead of removing.

        Returns:
            True if deletion succeeded, False if record not found.

        Raises:
            AttributeError: If soft delete is requested but model lacks 'is_deleted' field.
            IntegrityError: If deletion violates foreign key or unique constraints.
        """
        session = self._get_session(session)

        # Step 1: Fetch instance
        instance = await self.get({"id": model_id}, session=session)
        if not instance:
            log.info("No %s found with id=%s", self.model.__name__, model_id)
            return False

        try:
            if soft:
                # Step 2a: Soft delete — mark as deleted
                if not hasattr(instance, "is_deleted"):
                    raise AttributeError(
                        f"{self.model.__name__} has no 'is_deleted' field for soft delete"
                    )
                instance.is_deleted = True  # type: ignore
                log.debug(
                    "Soft deleting %s (id=%s)",
                    self.model.__name__,
                    model_id,
                )
            else:
                # Step 2b: Hard delete — remove from DB
                log.debug(
                    "Hard deleting %s (id=%s)",
                    self.model.__name__,
                    model_id,
                )
                await session.delete(instance)

            # Step 3: Commit transaction
            await session.commit()

            # Step 4: Refresh only for soft delete (still exists in DB)
            if soft:
                await session.refresh(instance)

            log.info(
                "%s deleted (id=%s, soft=%s)",
                self.model.__name__,
                model_id,
                soft,
            )
            return True

        except IntegrityError as e:
            await session.rollback()
            log.warning(
                "IntegrityError while deleting %s (id=%s, soft=%s): %s",
                self.model.__name__,
                model_id,
                soft,
                e,
            )
            raise
