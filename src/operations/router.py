from typing import List

from fastapi import APIRouter, Depends
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


@router.get("/", response_model=List[Operation])
async def get_specific_operations(
    operation_type: str, session: AsyncSession = Depends(get_async_session)
):
    query = select(operation).where(operation.c.type == operation_type)

    result = await session.execute(query)
    resres = result.all()
    # resres = jsonable_encoder(resres)
    print(resres)
    return resres
