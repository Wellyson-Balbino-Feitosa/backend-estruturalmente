from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.sql import func
from .database import Base

class Response(Base):
    """
    Modelo SQLAlchemy representando a tabela de respostas do Simulador de Introspecção.
    Aplica separação de responsabilidades: este arquivo cuida apenas do mapeamento objeto-relacional.
    """
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, index=True)
    sensations = Column(Text, nullable=False)
    feelings = Column(Text, nullable=False)
    mental_images = Column(Text, nullable=False)
    # Timestamp automático gerenciado pelo banco de dados
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
