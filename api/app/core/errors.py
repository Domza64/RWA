# =============================================================
# errors.py — Bazni error tip i globalni exception handler
# =============================================================
# Razdvaja DOMAIN ERRORE (poslovna pravila) od HTTP ERRORA.
#
# Korištenje u serviceu:
#   raise AppError(code="deadline_passed", message="...", status_code=400)
#
# =============================================================

from fastapi import Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    """
    Bazni error za sve domenski/poslovne greške u aplikaciji.

    Atributi:
        code:        Strojno čitljiv kod (npr. "not_found", "forbidden").
                     Frontend može koristiti ovaj kod za prijevode ili logiku.
        message:     Ljudski čitljiv opis greške.
        status_code: HTTP status kod (default 400 — Bad Request).
    """

    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code


async def app_error_handler(_request: Request, exc: AppError) -> JSONResponse:
    """
    Globalni handler koji FastAPI poziva kad bilo koji endpoint baci AppError.

    Vraća dosljedan JSON format:
        {"code": "...", "message": "..."}

    Registriramo ga u main.py sa:
        app.add_exception_handler(AppError, app_error_handler)
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message},
    )
