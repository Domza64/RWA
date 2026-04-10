from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Tijelo POST /auth/login requesta."""
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1)


class RegisterRequest(BaseModel):
    """Tijelo POST /auth/register requesta."""
    username: str = Field(min_length=1, max_length=50)
    email: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=50)


class TokenResponse(BaseModel):
    """Odgovor s JWT tokenima nakon uspješnog logina ili refresha."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    """Tijelo POST /auth/refresh requesta."""
    refresh_token: str


class UserResponse(BaseModel):
    """Prikaz trenutnog korisnika (GET /auth/me)."""
    user_id: int
    username: str
    email: str

    model_config = {"from_attributes": True}
