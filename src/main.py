from fastapi import FastAPI, Depends

app = FastAPI()


async def get_async_session():
    print("Получение сессии")
    session = "session"
    yield session
    print("Уничтожение сессии")


# depends - временные соединения с БД, redis и т.д.
# мы сначала получаем сессию, она в ендпоинт отдается, и только потом контроль в get_async_session возвращается, и сессия уничтожается
# если, кстати, в get_async_session поместить парамтер, то он будет требоваться при посылании сигнала на view


@app.get("/items")
async def get_items(session=Depends(get_async_session)):
    print(session)
    return [{"id": 1}]


@app.get("/subjects")
async def get_subjects(limit: int = 10, skip: int = 0):
    return [{"id": 1}]
