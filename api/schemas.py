from pydantic import BaseModel, Field
from datetime import datetime

class ResponseCreate(BaseModel):
    """
    Schema de validação Pydantic para os dados recebidos na requisição (Input).
    Garante validação rigorosa dos tipos e estrutura antes de chegar ao banco.
    """
    sensations: str = Field(..., description="Relato das sensações percebidas pelo usuário")
    feelings: str = Field(..., description="Relato dos sentimentos vivenciados")
    mental_images: str = Field(..., description="Descrição das imagens mentais evocadas")

class ResponseOut(ResponseCreate):
    """
    Schema de validação Pydantic para a resposta retornada pela API (Output).
    Extende o ResponseCreate adicionando campos gerados pelo banco de dados.
    """
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True # Permite leitura a partir de instâncias do ORM (SQLAlchemy)
