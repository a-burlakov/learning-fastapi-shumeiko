from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

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
