# 💈 Barber Booking API

API REST para sistema de agendamento de barbearia. Permite cadastro de clientes, consulta de horários disponíveis e gerenciamento de agendamentos com autenticação JWT.

Desenvolvida com **FastAPI** e banco de dados **SQLite**, pronta para ser consumida por qualquer front-end (React Native, Flutter, web).

## 🌐 Demo ao vivo

> **API online:** https://web-production-e3626.up.railway.app
>
> **Documentação interativa:** https://web-production-e3626.up.railway.app/docs

## 🖥️ Funcionalidades

- 🔐 Autenticação JWT (register, login e token Bearer)
- 👤 Cadastro de clientes com senha criptografada (bcrypt)
- 📅 Listar horários disponíveis por data
- ✅ Criar agendamento autenticado
- 🗓️ Ver meus agendamentos
- ❌ Cancelar agendamento
- 📚 Documentação automática em `/docs`

## 🚀 Como rodar localmente

```bash
# 1. Clone o repositório
git clone https://github.com/IsraelSiq/barber-booking-api.git
cd barber-booking-api

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Inicie o servidor
python -m uvicorn main:app --reload
```

Acesse a documentação interativa em: **http://localhost:8000/docs**

## 📡 Endpoints

### Autenticação
| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/auth/register` | Cadastrar novo cliente |
| `POST` | `/auth/login` | Login e geração de token JWT |

### Clientes
| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/clientes/` | Listar todos os clientes |
| `GET` | `/clientes/{id}` | Buscar cliente por ID |

### Agendamentos
| Método | Rota | Descrição | Auth |
|---|---|---|---|
| `GET` | `/agendamentos/disponiveis?data=YYYY-MM-DD` | Horários disponíveis | ❌ |
| `POST` | `/agendamentos/` | Criar agendamento | ✅ |
| `GET` | `/agendamentos/meus` | Meus agendamentos | ✅ |
| `DELETE` | `/agendamentos/{id}` | Cancelar agendamento | ✅ |

## 📁 Estrutura

```
barber-booking-api/
├── main.py              # App principal FastAPI
├── auth.py              # Lógica JWT e autenticação
├── database.py          # Conexão SQLite + SQLAlchemy
├── models.py            # Modelos do banco de dados
├── schemas.py           # Validação de dados (Pydantic)
├── routes/
│   ├── auth.py          # Rotas de registro e login
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
- `python-jose` — geração e validação de tokens JWT
- `passlib + bcrypt` — criptografia de senhas
- `Uvicorn` — servidor ASGI
- `SQLite` — banco de dados local
