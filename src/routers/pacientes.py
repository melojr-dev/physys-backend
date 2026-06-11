from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src import models, schemas

router = APIRouter()

@router.post("/", response_model=schemas.PacienteOut)
def criar_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = models.Paciente(**paciente.dict())
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

@router.get("/", response_model=List[schemas.PacienteOut])
def listar_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).order_by(models.Paciente.criado_em.desc()).all()

@router.get("/{paciente_id}", response_model=schemas.PacienteOut)
def buscar_paciente(paciente_id: int, db: Session = Depends(get_db)):
    p = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return p

@router.put("/{paciente_id}", response_model=schemas.PacienteOut)
def atualizar_paciente(paciente_id: int, dados: schemas.PacienteCreate, db: Session = Depends(get_db)):
    p = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    for k, v in dados.dict().items():
        setattr(p, k, v)
    db.commit()
    db.refresh(p)
    return p

@router.delete("/{paciente_id}")
def deletar_paciente(paciente_id: int, db: Session = Depends(get_db)):
    p = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    db.delete(p)
    db.commit()
    return {"ok": True}
