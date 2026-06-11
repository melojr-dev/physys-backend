from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# --- Paciente ---
class PacienteCreate(BaseModel):
    nome: str
    data_nascimento: Optional[str] = None
    sexo: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    diagnostico: Optional[str] = None
    observacoes: Optional[str] = None

class PacienteOut(PacienteCreate):
    id: int
    criado_em: datetime
    class Config:
        from_attributes = True

# --- Sessão ---
class SessaoCreate(BaseModel):
    paciente_id: int
    movimento: str
    lado: str
    adm_max: Optional[float] = None
    adm_media: Optional[float] = None
    adm_min: Optional[float] = None
    adm_desvio: Optional[float] = None
    velocidade_pico: Optional[float] = None
    velocidade_media: Optional[float] = None
    total_reps: Optional[int] = None
    duracao: Optional[float] = None
    fps: Optional[float] = None
    outliers_corrigidos: Optional[int] = None
    filtro_q: Optional[float] = None
    filtro_r: Optional[float] = None
    hardware: Optional[str] = None
    label_qualidade: Optional[str] = None
    notas: Optional[str] = None
    sequencia_angulos: Optional[str] = None

class SessaoOut(SessaoCreate):
    id: int
    criado_em: datetime
    class Config:
        from_attributes = True

# --- Análise ---
class AnaliseResult(BaseModel):
    angulos_brutos: List[float]
    angulos_filtrados: List[float]
    velocidades: List[float]
    total_reps: int
    fps: float
    adm_max: float
    adm_media: float
    adm_min: float
    adm_desvio: float
    velocidade_pico: float
    velocidade_media: float
    duracao: float
    outliers_corrigidos: int
    frames_b64: List[str]
