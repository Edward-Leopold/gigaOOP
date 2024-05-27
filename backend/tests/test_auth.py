import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(async_client: AsyncClient):
    response = await async_client.post(
        "/auth/register",
        json={
            "email": "user@example.com",
            "password": "password",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "name": "Test User",
            "status": 0,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "user@example.com"


@pytest.mark.asyncio
async def test_login_user(async_client: AsyncClient):
    response = await async_client.post(
        "/auth/jwt/login", data={"username": "user@example.com", "password": "password"}
    )
    assert response.status_code == 204
