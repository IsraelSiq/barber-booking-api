from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base
from datetime import datetime


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    role = Column(String, default="cliente")
    criado_em = Column(DateTime, default=datetime.utcnow)


class Endereco(Base):
    __tablename__ = "enderecos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    apelido = Column(String, nullable=False)  # "Casa", "Trabalho"
    rua = Column(String, nullable=False)
    numero = Column(String, nullable=False)
    bairro = Column(String, nullable=False)
    cidade = Column(String, nullable=False)
    complemento = Column(String, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)


class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, nullable=False)
    endereco_id = Column(Integer, ForeignKey("enderecos.id"), nullable=True)
    data_hora = Column(DateTime, nullable=False)
    servico = Column(String, default="Corte")
    status = Column(String, default="confirmado")
    criado_em = Column(DateTime, default=datetime.utcnow)
