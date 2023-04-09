from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder

from src.auth.schemas import Operation
from src.database import get_async_session
from src.operations.models import operation

router = APIRouter(
    prefix="/operations",
    tags=["Operations"],
)


@router.get(
    "/",
    # response_model=List[Operation],
)
async def get_specific_operations(
    operation_type: str, session: AsyncSession = Depends(get_async_session)
):
    # Желательно всегда ставить exception, потому что все может пойти не так.
    try:
        query = select(operation).where(operation.c.type == operation_type)

        result = await session.execute(query)
        resres = result.all()
        x = 1 / 0
        print(resres)
        return resres
    except ZeroDivisionError:
        return HTTPException(
            status_code=500,
            detail={
                "status": "dividing to zero",
                "data": None,
                "details": "fatal overkill",
            },
        )

    except:
        return {
            "status": "error",
            "data": None,
            "details": None,
        }
