from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


async def get_by_username(db: AsyncSession, username: str) -> User | None:
    """Dohvati korisnika po username-u (za login)."""
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def get_by_id(db: AsyncSession, user_id: int) -> User | None:
    """Dohvati korisnika po ID-u (za JWT verifikaciju)."""
    result = await db.execute(select(User).where(User.user_id == user_id))
    return result.scalar_one_or_none()


async def insert_user(db, username: str, email: str, password_hash: str):
    await db.execute(insert(User).values(username=username, email=email, password_hash=password_hash))
    await db.flush()
