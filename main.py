from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine, get_db
from routes import clientes, agendamentos, auth, admin
from models import Cliente
from auth import hash_senha

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Barber Booking API",
    description="API para agendamento de barbearia com autenticação JWT",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
app.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
app.include_router(agendamentos.router, prefix="/agendamentos", tags=["Agendamentos"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])


@app.on_event("startup")
def criar_admin_padrao():
    db = next(get_db())
    existe = db.query(Cliente).filter(Cliente.email == "admin@barber.com").first()
    if not existe:
        admin_user = Cliente(
            nome="Admin",
            telefone="00000000000",
            email="admin@barber.com",
            senha=hash_senha("admin123"),
            role="admin"
        )
        db.add(admin_user)
        db.commit()


@app.get("/")
def root():
    return {"message": "Barber Booking API 💈", "docs": "/docs", "version": "2.0.0"}
