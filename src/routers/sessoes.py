from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src import models, schemas

router = APIRouter()

@router.post("/", response_model=schemas.SessaoOut)
def criar_sessao(sessao: schemas.SessaoCreate, db: Session = Depends(get_db)):
    db_sessao = models.Sessao(**sessao.dict())
    db.add(db_sessao)
    db.commit()
    db.refresh(db_sessao)
    return db_sessao

@router.get("/", response_model=List[schemas.SessaoOut])
def listar_sessoes(db: Session = Depends(get_db)):
    return db.query(models.Sessao).order_by(models.Sessao.criado_em.desc()).all()

@router.get("/paciente/{paciente_id}", response_model=List[schemas.SessaoOut])
def sessoes_por_paciente(paciente_id: int, db: Session = Depends(get_db)):
    return db.query(models.Sessao).filter(
        models.Sessao.paciente_id == paciente_id
    ).order_by(models.Sessao.criado_em.desc()).all()

@router.get("/{sessao_id}", response_model=schemas.SessaoOut)
def buscar_sessao(sessao_id: int, db: Session = Depends(get_db)):
    s = db.query(models.Sessao).filter(models.Sessao.id == sessao_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")
    return s

@router.delete("/{sessao_id}")
def deletar_sessao(sessao_id: int, db: Session = Depends(get_db)):
    s = db.query(models.Sessao).filter(models.Sessao.id == sessao_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")
    db.delete(s)
    db.commit()
    return {"ok": True}
