from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, ValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

app = FastAPI(
    title="Trading App",
)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


fake_users = [
    {"id": 1, "role": ["abc"], "name": ["bob"]},
    {"id": 2, "role": "investor", "name": "john"},
    {"id": 3, "role": "trader", "name": "alex"},
    {
        "id": 4,
        "role": "investor",
        "name": "Homer",
        "degree": [
            {"id": 1, "created_at": "2020-01-01T00:00:00", "type_degree": "expert"}
        ],
    },
]


@app.get("/")
async def root():
    return {"message": "Hello World"}


class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]]


@app.get("/users/{user_id}", response_model=List[User])
async def root(user_id: int):
    return [user for user in fake_users if user.get("id") == int(user_id)]


fake_trades = [
    {
        "id": 1,
        "user_id": 1,
        "currency": "BTC",
        "side": "buy",
        "price": 123,
        "amount": 2.12,
    },
    {
        "id": 2,
        "user_id": 1,
        "currency": "BTC",
        "side": "sell",
        "price": 123,
        "amount": 2.12,
    },
]


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float


@app.post("/trades")
def add_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return {"status": 200, "data": fake_trades}
