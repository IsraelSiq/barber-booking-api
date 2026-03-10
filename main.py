from fastapi import FastAPI
from database import Base, engine
from routes import clientes, agendamentos, auth, admin

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Barber Booking API",
    description="API para agendamento de barbearia com autenticação JWT",
    version="2.0.0"
)

app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
app.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
app.include_router(agendamentos.router, prefix="/agendamentos", tags=["Agendamentos"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])


@app.get("/")
def root():
    return {"message": "Barber Booking API 💈", "docs": "/docs", "version": "2.0.0"}
