import asyncio
import os
import sys

# Adiciona a raiz do projeto ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.database import engine
from api.models import Base
from sqlalchemy import text

async def reset_db():
    print("Iniciando a limpeza do banco de dados...")
    try:
        async with engine.begin() as conn:
            # 1. Apaga as tabelas antigas que possam ter ficado pra trás (como a "responses")
            print("Apagando tabelas antigas e residuais...")
            await conn.execute(text("DROP TABLE IF EXISTS responses;"))
            
            # 2. Apaga as tabelas atuais mapeadas no SQLAlchemy
            print("Apagando tabelas estruturais atuais...")
            await conn.run_sync(Base.metadata.drop_all)
            
            # 3. Recria todas as tabelas novamente com a estrutura limpa
            print("Recriando as tabelas com a nova estrutura...")
            await conn.run_sync(Base.metadata.create_all)
            
        print("[SUCESSO] Banco de dados resetado e limpo com sucesso!")
    except Exception as e:
        print(f"[ERRO] Erro ao resetar banco de dados: {e}")
    finally:
        await engine.dispose()
        print("Conexão encerrada.")

if __name__ == "__main__":
    asyncio.run(reset_db())
