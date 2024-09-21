from pydantic import BaseModel


class TokenResponse(BaseModel):
    """
    DTO for auth models.

    It returned when attempt to log in.
    """

    access_token: str
    refresh_token: str


class DecodedTokenResponse(BaseModel):
    """DTO for decoded token."""

    sub: str
    jti: str
    expires: float
    token_type: str
