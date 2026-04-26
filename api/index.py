from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from typing import List
import os

from . import models, schemas, crud
from .database import engine, get_db

# Gerenciamento de ciclo de vida assíncrono
# Cria as tabelas do banco de dados no momento em que a aplicação inicia
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield

# Inicialização da aplicação FastAPI
app = FastAPI(
    title="API EstruturalMente",
    description="Backend para o Simulador de Introspecção (Estruturalismo) construído de forma assíncrona e performática.",
    version="1.0.0",
    lifespan=lifespan
)

# Configuração de CORS - Habilita requisições do frontend
# Para produção idealmente devemos listar as origens específicas no allow_origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://estruturalmente.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health Check"])
async def root():
    """
    Endpoint simples para verificar se a API está online.
    """
    return {"status": "ok", "message": "API EstruturalMente operando normalmente."}

@app.post("/api/responses", response_model=schemas.ResponseOut, status_code=status.HTTP_201_CREATED, tags=["Responses"])
async def create_response(response: schemas.ResponseCreate, db: AsyncSession = Depends(get_db)):
    """
    Recebe os dados do formulário do frontend e armazena no banco de dados.
    Validação de dados automática através do schema ResponseCreate.
    """
    try:
        return await crud.create_response(db=db, response=response)
    except Exception as e:
        # Registra a falha, para debug na Vercel (disponível nos logs do servidor)
        print(f"Erro ao salvar: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao processar a resposta. Tente novamente mais tarde."
        )

@app.get("/api/responses", response_model=List[schemas.ResponseOut], tags=["Responses"])
async def read_responses(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Recupera o histórico das experiências de introspecção salvas no banco.
    Possui paginação via skip e limit.
    """
    try:
        return await crud.get_responses(db, skip=skip, limit=limit)
    except Exception as e:
        print(f"Erro ao buscar: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao buscar as respostas do servidor."
        )
