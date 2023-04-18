from fastapi import FastAPI, Depends

app = FastAPI()


async def get_async_session():
    print("Получение сессии")
    session = "session"
    yield session
    print("Уничтожение сессии")


def pagination_params(limit: int = 10, skip: int = 0):
    return {
        "limit": limit,
        "skip": skip,
    }


class Paginator:
    def __init__(self, limit: int = 10, skip: int = 0):
        self.limit = limit
        self.skip = skip


# depends - временные соединения с БД, redis и т.д.
# мы сначала получаем сессию, она в ендпоинт отдается, и только потом контроль в get_async_session возвращается, и сессия уничтожается
# если, кстати, в get_async_session поместить парамтер, то он будет требоваться при посылании сигнала на view


@app.get("/items")
async def get_items(session=Depends(get_async_session)):
    print(session)
    return [{"id": 1}]


# FastAPI, перед тем, как обрабатывать запрос опользователя, он все зависимости прогоняет.
# То есть берет функцию из Depends, и говорит: pagination_params = pagination_params()
@app.get("/subjects")
async def get_subjects(pagination_params: dict = Depends(pagination_params)):
    return [{"id": 1}]


# В Depends также можно прокидывать и создание экземпляра класса, а не только функции.
@app.get("/subjects_class")
async def get_subjects(pagination_params: Paginator = Depends(Paginator)):
    return [{"id": 1}]
