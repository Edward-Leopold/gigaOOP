import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_course(async_client: AsyncClient):
    response = await async_client.post(
        "/courses/",
        json={
            "title": "Introduction to FastAPI",
            "description": "Learn the basics of FastAPI framework.",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Introduction to FastAPI"
    assert data["description"] == "Learn the basics of FastAPI framework."


@pytest.mark.asyncio
async def test_read_course(async_client: AsyncClient):
    response = await async_client.post(
        "/courses/",
        json={"title": "Advanced FastAPI", "description": "Deep dive into FastAPI."},
    )
    assert response.status_code == 200
    course_id = response.json()["id"]

    response = await async_client.get(f"/courses/{course_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Advanced FastAPI"
    assert data["description"] == "Deep dive into FastAPI."


@pytest.mark.asyncio
async def test_get_courses(async_client: AsyncClient):
    response = await async_client.get("/courses/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_update_course(async_client: AsyncClient):
    response = await async_client.post(
        "/courses/",
        json={
            "title": "Intermediate FastAPI",
            "description": "Learn intermediate concepts of FastAPI.",
        },
    )
    assert response.status_code == 200
    course_id = response.json()["id"]

    response = await async_client.put(
        f"/courses/{course_id}",
        json={
            "title": "Intermediate FastAPI Updated",
            "description": "Updated intermediate concepts of FastAPI.",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Intermediate FastAPI Updated"
    assert data["description"] == "Updated intermediate concepts of FastAPI."


@pytest.mark.asyncio
async def test_delete_course(async_client: AsyncClient):
    response = await async_client.post(
        "/courses/",
        json={"title": "Delete Me", "description": "This course will be deleted."},
    )
    assert response.status_code == 200
    course_id = response.json()["id"]

    response = await async_client.delete(f"/courses/{course_id}")
    assert response.status_code == 200

    response = await async_client.get(f"/courses/{course_id}")
    assert response.status_code == 404
