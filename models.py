from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    endereco = Column(String, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)


class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, nullable=False)
    data_hora = Column(DateTime, nullable=False)
    servico = Column(String, default="Corte")
    status = Column(String, default="confirmado")
    criado_em = Column(DateTime, default=datetime.utcnow)
