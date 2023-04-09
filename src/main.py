from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

import aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_users import fastapi_users, FastAPIUsers
from pydantic import BaseModel, Field

from fastapi import FastAPI, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationError
from fastapi.responses import JSONResponse

from src.auth.auth import auth_backend
from src.database import User
from src.auth.manager import get_user_manager
from src.auth.schemas import UserRead, UserCreate
from src.operations.router import router as router_operations

app = FastAPI(title="Trading App")

app.include_router(router_operations)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(
        "redis://localhost", encoding="utf8", decode_response=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
