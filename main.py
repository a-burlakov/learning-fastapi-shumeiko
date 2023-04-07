from fastapi import FastAPI

app = FastAPI(title="Trading App")

fake_users = [
    {"id": 1, "role": "admin", "name": "bob"},
    {"id": 2, "role": "investor", "name": "john"},
    {"id": 3, "role": "trader", "name": "alex"},
]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/{user_id}")
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


@app.get("/trades")
def get_trades(offset: int = 0, limit: int = 10):
    return fake_trades[offset:][:limit]


fake_users_2 = [
    {"id": 1, "role": "admin", "name": "bob"},
    {"id": 2, "role": "investor", "name": "john"},
    {"id": 3, "role": "trader", "name": "alex"},
]


@app.post("/users/{users_id}")
def change_user_name(users_id: int, new_name: str):
    current_user = next(
        (user for user in fake_users_2 if user["id"] == users_id),
        fake_users_2[0],
    )

    current_user["name"] = new_name

    return current_user
