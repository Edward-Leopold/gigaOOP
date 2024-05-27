import uuid

from fastapi import Depends, FastAPI
from fastapi_users import FastAPIUsers

from fastapi.middleware.cors import CORSMiddleware
import logging

from api.routers.user import current_active_user, fastapi_users, get_user_manager
from core.auth import auth_backend
from core.config import settings
from db.schemas.user import UserCreate, UserRead, UserUpdate
from db.models.user import User
from api.routers import course
from api.routers import theme
from api.routers import quiz


# Настройка логирования
logging.basicConfig(level=logging.DEBUG)


fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)


app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


app.include_router(course.router, prefix="/courses", tags=["courses"])
app.include_router(theme.router, prefix="/themes", tags=["themes"])
app.include_router(quiz.router, prefix="/quizzes", tags=["quizzes"])


origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET, POST, PATCH, DELETE, OPTIONS, PUT"],
    allow_headers=["*"],
)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}
