from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def health():
    """
    Health check — potvrđuje da API radi.

    Vraća: {"status": "ok"}
    """
    return {"status": "ok"}
