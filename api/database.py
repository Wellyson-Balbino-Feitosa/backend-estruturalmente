from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os
import ssl
import sys
import asyncio
from dotenv import load_dotenv

# No Windows, o aiomysql exige o SelectorEventLoop para funcionar corretamente
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Carrega as variáveis do arquivo .env para o ambiente local
load_dotenv()

# Estratégia de Arquitetura:
# Lemos a variável URL_DATABASE (do seu .env) ou DATABASE_URL.
raw_url = os.environ.get("URL_DATABASE") or os.environ.get("DATABASE_URL")

if not raw_url:
    raise ValueError("A variável de ambiente URL_DATABASE não foi encontrada. Verifique seu arquivo .env")

raw_url = raw_url.strip()

# O SQLAlchemy assíncrono precisa do driver '+aiomysql' na URL. 
# Como a Aiven (e outros DBaaS) fornecem a URL com 'mysql://', fazemos a adaptação automaticamente:
if raw_url.startswith("mysql://"):
    DATABASE_URL = raw_url.replace("mysql://", "mysql+aiomysql://", 1)
else:
    DATABASE_URL = raw_url

# Limpeza de parâmetros da URL que podem causar conflito com o aiomysql
if "?ssl-mode=REQUIRED" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("?ssl-mode=REQUIRED", "?ssl=true")

# Configuração do contexto SSL para aceitar o certificado da Aiven
# Sem isso, a Vercel/Local daria erro de 'self-signed certificate'
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Criação da engine assíncrona garantindo alta performance no I/O do banco de dados
engine = create_async_engine(
    DATABASE_URL, 
    echo=False,
    pool_pre_ping=True, # Recomendado para MySQL na nuvem para verificar conexões ativas
    pool_recycle=1800,  # Provedores em nuvem fecham conexões ociosas rápido. 1800s previne timeout.
    connect_args={"ssl": ssl_context} # Usa o contexto configurado acima
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
