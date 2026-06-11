from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import Base

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    data_nascimento = Column(String)
    sexo = Column(String)
    telefone = Column(String)
    email = Column(String)
    diagnostico = Column(Text)
    observacoes = Column(Text)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    sessoes = relationship("Sessao", back_populates="paciente")


class Sessao(Base):
    __tablename__ = "sessoes"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    movimento = Column(String, nullable=False)
    lado = Column(String, nullable=False)
    adm_max = Column(Float)
    adm_media = Column(Float)
    adm_min = Column(Float)
    adm_desvio = Column(Float)
    velocidade_pico = Column(Float)
    velocidade_media = Column(Float)
    total_reps = Column(Integer)
    duracao = Column(Float)
    fps = Column(Float)
    outliers_corrigidos = Column(Integer)
    filtro_q = Column(Float)
    filtro_r = Column(Float)
    hardware = Column(String)
    label_qualidade = Column(String)
    notas = Column(Text)
    sequencia_angulos = Column(Text)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    paciente = relationship("Paciente", back_populates="sessoes")
