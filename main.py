from fastapi import FastAPI
from database import Base, engine
from routes import clientes, agendamentos

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Barber Booking API",
    description="API para agendamento de barbearia",
    version="1.0.0"
)

app.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
app.include_router(agendamentos.router, prefix="/agendamentos", tags=["Agendamentos"])


@app.get("/")
def root():
    return {"message": "Barber Booking API 💈", "docs": "/docs"}
