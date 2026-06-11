from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import engine, Base
from src.routers import pacientes, sessoes, relatorios, analise

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PhySys API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pacientes.router, prefix="/api/pacientes", tags=["Pacientes"])
app.include_router(sessoes.router, prefix="/api/sessoes", tags=["Sessões"])
app.include_router(relatorios.router, prefix="/api/relatorios", tags=["Relatórios"])
app.include_router(analise.router, prefix="/api/analise", tags=["Análise"])

@app.get("/")
def root():
    return {"status": "ok", "message": "PhySys API rodando"}
