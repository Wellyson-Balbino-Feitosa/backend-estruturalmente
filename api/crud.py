from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas

# ---- ESTÍMULO 1 ----
async def create_stimulus1_response(db: AsyncSession, response: schemas.StimulusResponseOneCreate):
    db_response = models.Stimulus1Response(**response.model_dump())
    db.add(db_response)
    await db.commit()
    await db.refresh(db_response)
    return db_response

async def get_stimulus1_responses(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Stimulus1Response).offset(skip).limit(limit))
    return result.scalars().all()

# ---- ESTÍMULO 2 ----
async def create_stimulus2_response(db: AsyncSession, response: schemas.StimulusResponseTwoCreate):
    db_response = models.Stimulus2Response(**response.model_dump())
    db.add(db_response)
    await db.commit()
    await db.refresh(db_response)
    return db_response

async def get_stimulus2_responses(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Stimulus2Response).offset(skip).limit(limit))
    return result.scalars().all()
