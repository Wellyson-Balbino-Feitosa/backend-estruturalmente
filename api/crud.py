from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas

async def create_response(db: AsyncSession, response: schemas.ResponseCreate):
    """
    Persiste uma nova resposta de introspecção no banco de dados.
    Operação totalmente assíncrona para não bloquear a thread principal.
    """
    db_response = models.Response(
        sensations=response.sensations,
        feelings=response.feelings,
        mental_images=response.mental_images
    )
    db.add(db_response)
    await db.commit()
    await db.refresh(db_response)
    return db_response

async def get_responses(db: AsyncSession, skip: int = 0, limit: int = 100):
    """
    Busca as respostas salvas no banco com paginação básica.
    Utiliza a API do SQLAlchemy 2.0 (select) para compatibilidade assíncrona.
    """
    result = await db.execute(select(models.Response).offset(skip).limit(limit))
    return result.scalars().all()
