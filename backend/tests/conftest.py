import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from main import app
from db.session import Base, get_async_session
from db.base import Base

TEST_DATABASE_URL = 'sqlite+aiosqlite:///./test.db'

engine = create_async_engine(TEST_DATABASE_URL, connect_args={'check_same_thread': False})
TestingSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def override_get_db() -> AsyncSession:
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_db


@pytest.fixture(scope='session')
async def async_client():
    """Initializing async client"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        yield client


@pytest.fixture(scope='session', autouse=True)
async def setup_and_teardown_db():
    """Setup and teardown test database"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
