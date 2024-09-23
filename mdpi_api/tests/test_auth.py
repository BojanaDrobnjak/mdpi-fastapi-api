import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


@pytest.mark.anyio
async def test_login_failure(
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests login failure with invalid credentials."""
    email = "user@test.com"
    password = "test_password"  # noqa: S105
    url = "/api/auth/token"
    response = await client.get(url, params={"email": email, "password": password})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, (
        f"Expected 401 but got {response.status_code}",
    )
    error_response = response.json()
    assert "message" in error_response, "Expected 'message' field in error response"
    assert "detail" in error_response, "Expected 'detail' field in error response"
    assert error_response["message"] == "Not authorized"
    assert error_response["detail"] == "Invalid credentials"
