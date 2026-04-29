from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.sql import func
from .database import Base

class Stimulus1Response(Base):
    """Modelo SQLAlchemy para a tabela de respostas do Estímulo 1"""
    __tablename__ = "stimulus_1_responses"

    id = Column(Integer, primary_key=True, index=True)
    sensations = Column(Text, nullable=False)
    feelings = Column(Text, nullable=False)
    mental_images = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class Stimulus2Response(Base):
    """Modelo SQLAlchemy para a tabela de respostas do Estímulo 2"""
    __tablename__ = "stimulus_2_responses"

    id = Column(Integer, primary_key=True, index=True)
    intensidade = Column(Text, nullable=False)
    duracao = Column(Text, nullable=False)
    textura = Column(Text, nullable=False)
    clareza = Column(Text, nullable=False)
    tom_afetivo = Column(Text, nullable=False)
    descricao_livre = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
