# 💈 Barber Booking API

API REST para sistema de agendamento de barbearia. Permite cadastro de clientes, consulta de horários disponíveis e gerenciamento de agendamentos.

Desenvolvida com **FastAPI** e banco de dados **SQLite**, pronta para ser consumida por qualquer front-end (React Native, Flutter, web).

## 🖥️ Funcionalidades

- 👤 Cadastro e listagem de clientes
- 📅 Listar horários disponíveis por data
- ✅ Criar agendamento
- ❌ Cancelar agendamento
- 📚 Documentação automática em `/docs`

## 🚀 Como rodar

```bash
# 1. Clone o repositório
git clone https://github.com/Wallisbr/barber-booking-api.git
cd barber-booking-api

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Inicie o servidor
uvicorn main:app --reload
```

Acesse a documentação interativa em: **http://localhost:8000/docs**

## 📡 Endpoints

### Clientes
| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/clientes/` | Cadastrar novo cliente |
| `GET` | `/clientes/` | Listar todos os clientes |
| `GET` | `/clientes/{id}` | Buscar cliente por ID |

### Agendamentos
| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/agendamentos/disponíveis?data=2026-03-10` | Horários disponíveis |
| `POST` | `/agendamentos/` | Criar agendamento |
| `GET` | `/agendamentos/{id}` | Buscar agendamento |
| `DELETE` | `/agendamentos/{id}` | Cancelar agendamento |

## 📁 Estrutura

```
barber-booking-api/
├── main.py              # App principal FastAPI
├── database.py          # Conexão SQLite + SQLAlchemy
├── models.py            # Modelos do banco de dados
├── schemas.py           # Validação de dados (Pydantic)
├── routes/
│   ├── clientes.py      # Rotas de clientes
│   └── agendamentos.py  # Rotas de agendamentos
├── requirements.txt
└── README.md
```

## 🛠️ Tecnologias

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

- `FastAPI` — framework web moderno e rápido
- `SQLAlchemy` — ORM para manipulação do banco
- `Pydantic` — validação de dados
- `Uvicorn` — servidor ASGI
- `SQLite` — banco de dados local
