from fastapi import FastAPI
from auth.routes import router as auth_router
from users.routes import router as users_router
from tasks.routes import router as tasks_router
from starlette.middleware.base import BaseHTTPMiddleware
from auth.dependencies import get_authorized_user
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from users.models import User

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])


