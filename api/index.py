from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from typing import List
import os

from . import models, schemas, crud
from .database import engine, get_db

# Gerenciamento de ciclo de vida assíncrono
# NOTA: Em ambientes Serverless (como Vercel), evite usar eventos de startup 
# (como criar tabelas com create_all) dentro da API, pois isso ocorre a cada "cold start",
# gerando múltiplas conexões simultâneas que esgotam o pool de threads e causam 
# o erro OSError: [Errno 16] Device or resource busy na resolução de DNS.

# Inicialização da aplicação FastAPI
app = FastAPI(
    title="API EstruturalMente",
    description="Backend para o Simulador de Introspecção (Estruturalismo) construído de forma assíncrona e performática.",
    version="1.0.0"
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
    return {"status": "ok", "message": "API EstruturalMente operando normalmente."}

# ==========================================
# ROTAS PARA O ESTÍMULO 1
# ==========================================

@app.post("/api/stimulus-1/responses", response_model=schemas.StimulusResponseOneOut, status_code=status.HTTP_201_CREATED, tags=["Estímulo 1"])
async def create_stimulus1(response: schemas.StimulusResponseOneCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.create_stimulus1_response(db=db, response=response)
    except Exception as e:
        print(f"Erro ao salvar estímulo 1: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar a resposta do Estímulo 1.")

@app.get("/api/stimulus-1/responses", response_model=List[schemas.StimulusResponseOneOut], tags=["Estímulo 1"])
async def read_stimulus1(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.get_stimulus1_responses(db, skip=skip, limit=limit)
    except Exception as e:
        print(f"Erro ao buscar estímulo 1: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao buscar as respostas do Estímulo 1.")

# ==========================================
# ROTAS PARA O ESTÍMULO 2
# ==========================================

@app.post("/api/stimulus-2/responses", response_model=schemas.StimulusResponseTwoOut, status_code=status.HTTP_201_CREATED, tags=["Estímulo 2"])
async def create_stimulus2(response: schemas.StimulusResponseTwoCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.create_stimulus2_response(db=db, response=response)
    except Exception as e:
        print(f"Erro ao salvar estímulo 2: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar a resposta do Estímulo 2.")

@app.get("/api/stimulus-2/responses", response_model=List[schemas.StimulusResponseTwoOut], tags=["Estímulo 2"])
async def read_stimulus2(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.get_stimulus2_responses(db, skip=skip, limit=limit)
    except Exception as e:
        print(f"Erro ao buscar estímulo 2: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao buscar as respostas do Estímulo 2.")
