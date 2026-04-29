from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class StimulusResponseOneCreate(BaseModel):
    """Schema de entrada para o Estímulo 1 (Introspecção Clássica)."""
    sensations: str = Field(..., description="Relato das sensações percebidas")
    feelings: str = Field(..., description="Relato dos sentimentos")
    mental_images: str = Field(..., description="Descrição das imagens mentais")

class StimulusResponseOneOut(StimulusResponseOneCreate):
    """Schema de saída para o Estímulo 1."""
    id: int
    timestamp: datetime
    class Config:
        from_attributes = True

class StimulusResponseTwoCreate(BaseModel):
    """Schema de entrada para o Estímulo 2 (Atributos Sensoriais)."""
    intensidade: str = Field(..., description="Intensidade da resposta")
    duracao: str = Field(..., description="Duração da resposta")
    textura: str = Field(..., description="Textura percebida")
    clareza: str = Field(..., description="Clareza percebida")
    tom_afetivo: str = Field(..., description="Tom afetivo")
    descricao_livre: str = Field(..., description="Descrição livre")

class StimulusResponseTwoOut(StimulusResponseTwoCreate):
    """Schema de saída para o Estímulo 2."""
    id: int
    timestamp: datetime
    class Config:
        from_attributes = True

