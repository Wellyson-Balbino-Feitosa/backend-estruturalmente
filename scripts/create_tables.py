import asyncio
import os
import sys

# Adiciona a raiz do projeto ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.database import engine
from api.models import Base

async def init_db():
    print("Iniciando a criação das tabelas no banco de dados...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
    finally:
        await engine.dispose()
        print("Conexão com o banco encerrada.")

if __name__ == "__main__":
    asyncio.run(init_db())
