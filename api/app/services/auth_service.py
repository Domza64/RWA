from jose import JWTError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import security
from app.core.errors import AppError
from app.core.jwt import create_access_token, create_refresh_token, decode_token
from app.core.security import verify_password
from app.models.user import User
from app.repositories import user_repo


async def authenticate_user(
    db: AsyncSession, username: str, password: str
) -> User:
    """
    Provjeri kredencijale i vrati korisnika.
    """
    user = await user_repo.get_by_username(db, username)
    if not user or not verify_password(password, user.password_hash):
        raise AppError("invalid_credentials", "Pogrešno korisničko ime ili lozinka", 401)
    return user


def create_tokens(user: User) -> tuple[str, str]:
    """Generiraj access + refresh token par za korisnika."""
    access = create_access_token(user.user_id, user.username)
    refresh = create_refresh_token(user.user_id)
    return access, refresh


async def refresh_tokens(db: AsyncSession, refresh_token: str) -> tuple[str, str]:
    """Validiraj refresh token i izdaj novi par tokena."""
    try:
        payload = decode_token(refresh_token)
    except JWTError:
        raise AppError("invalid_credentials", "Nevažeći refresh token", 401)

    if payload.get("type") != "refresh":
        raise AppError("invalid_credentials", "Token nije refresh tipa", 401)

    user = await user_repo.get_by_id(db, int(payload["sub"]))
    if not user:
        raise AppError("invalid_credentials", "Korisnik ne postoji", 401)

    return create_tokens(user)


async def create_user(db: AsyncSession, username: str, email: str, password: str):
    """Kreiraj novog korisnika"""
    if len(password) < 5:
        raise AppError("weak_password", "Lozinka mora sadržavati više od 5 znakova", 400)

    try:
        await user_repo.insert_user(db, username=username, email=email, password_hash=security.hash_password(password))
    except IntegrityError:
        raise AppError("already_exists", "Korisničko ime ili email već postoji", 409)