from fastapi import FastAPI, Depends, HTTPException, APIRouter
from starlette.requests import Request

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


class AuthGuard:
    def __init__(self, name: str):
        pass

    def __call__(self, request: Request):
        # return True
        if "super_cookie" not in request.cookies:
            raise HTTPException(status_code=403, detail="Запрещено")
        else:
            # Проверяем, что в куках есть инфа о наличии прав
            return True


auth_guard_payments = AuthGuard("payments")

# FastAPI, перед тем, как обрабатывать запрос опользователя, он все зависимости прогоняет.
# То есть берет функцию из Depends, и говорит: pagination_params = pagination_params()
@app.get("/subjects")
async def get_subjects(pagination_params: dict = Depends(pagination_params)):
    return [{"id": 1}]


# В Depends также можно прокидывать и создание экземпляра класса, а не только функции.
@app.get("/subjects_class")
async def get_subjects(pagination_params: Paginator = Depends(Paginator)):
    return [{"id": 1}]


# Мы устанавливаем через Depends, что
# енд поинт имеет какую-то зависимость.
# Перед прогоном функции FastApi сначала прогонит все зависимости и убедится, что они не вызовут ошибки.
# Параметр в Depends должен быть вызываемый. В нем есть метод __call__.
# таким образом, мы сделали как бы кастомную вализацию.


# Можно помещать в параметр
# @app.get("/payments")
# def get_payments(auth_guard_payments: AuthGuard = Depends(auth_guard_payments)):
#     return "my payments"

# Если в параметре зависимости не нужны, то помещаем их прям в endpoint в аргумент
@app.get("/payments", dependencies=[Depends(auth_guard_payments)])
def get_payments():
    return "my payments"


# Мы можем на все ендпоинты одного роутера накинуть зависимость! <3
router = APIRouter(
    dependencies=[Depends(auth_guard_payments)],
)
