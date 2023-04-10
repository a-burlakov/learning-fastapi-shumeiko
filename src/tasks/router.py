from fastapi import APIRouter, BackgroundTasks, Depends

from auth.base_config import current_user

from .tasks import send_email_report_dashboard

router = APIRouter(prefix="/report")


@router.get("/dashboard")
def get_dashboard_report(background_tasks: BackgroundTasks):
    # 1400 ms - Клиент ждет
    # send_email_report_dashboard("Алексей")

    # 500 ms - Задача выполняется на фоне FastAPI в event loop'е или в другом треде
    # background_tasks.add_task(send_email_report_dashboard, "Алексей")

    # 600 ms - Задача выполняется воркером Celery в отдельном процессе
    # send_email_report_dashboard.delay("Алексей")

    send_email_report_dashboard.delay("Алексей Celery!")

    # В общем, чтобы закинуть таск в Celery, надо:
    # - сделать декоратор @celery.task на нужную функцию
    # - вызвать эту функцию через синтаксис [функция].delay([параметры])

    # В FastApi есть такая штука как BackgroundTasks - она позволяет просто без
    # мороки вызывать функции асинхронно. Это работает быстрее, чем при синхронном вызове,
    # но все равно не так быстро как через celery.
    # Также BackgroundTasks нельзя кастомизировать, назначать приоритеты и ограничения;
    # Также если сломается, то BackgroundTasks не сможет его запустить заново, а Celery может.

    return {"status": 200, "data": "Письмо отправлено", "details": None}
