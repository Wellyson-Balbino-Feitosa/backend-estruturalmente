from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os

# Estratégia de Arquitetura:
# Em ambientes serverless (Vercel), o sistema de arquivos principal é read-only.
# Por isso, caso a variável VERCEL esteja definida, o SQLite é salvo em /tmp/.
# É importante notar que em serverless o /tmp é efêmero (dados são perdidos entre execuções).
# Para uso real contínuo e permanente, sugere-se trocar para um Postgres (ex: Supabase, Neon) no Vercel.
DB_PATH = "/tmp/estruturalmente.db" if os.environ.get("VERCEL") else "estruturalmente.db"
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

# Criação da engine assíncrona garantindo alta performance no I/O do banco de dados
engine = create_async_engine(
    DATABASE_URL, 
    echo=False,
    connect_args={"check_same_thread": False} # Necessário para SQLite em ambiente assíncrono/multithread
)

# Fabrica de sessões assíncronas para as transações no banco
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

Base = declarative_base()

async def get_db():
    """
    Dependency Injection para injeção da sessão de banco de dados nas rotas.
    Garante que a sessão será aberta e fechada de forma limpa.
    """
    async with AsyncSessionLocal() as session:
        yield session
