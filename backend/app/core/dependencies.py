from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import SessionLocal

import logging

logger = logging.getLogger(__name__)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.exception(f"Database transaction rolled back: {e}")
            raise
        finally:
            await session.close()


DBDependency = Annotated[AsyncSession, Depends(get_db)]
