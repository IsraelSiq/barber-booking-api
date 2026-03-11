# 💈 Barber Booking API

> **REST API de agendamento para barbearia** — autenticação JWT, gerenciamento completo de clientes e agendamentos, documentação interativa automática.

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![Railway](https://img.shields.io/badge/Deploy-Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)](https://railway.app)
[![JWT](https://img.shields.io/badge/Auth-JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://jwt.io)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## 🌐 Deploy ao Vivo

| Recurso | URL |
|---|---|
| 🚀 API Base | https://web-production-e3626.up.railway.app |
| 📚 Swagger UI | https://web-production-e3626.up.railway.app/docs |
| 📖 ReDoc | https://web-production-e3626.up.railway.app/redoc |

---

## 🧠 Sobre o Projeto

Esta API foi construída com **FastAPI** e segue os princípios REST, oferecendo endpoints para autenticação segura, gerenciamento de clientes e controle de agendamentos em uma barbearia. Projetada para ser consumida por qualquer front-end — **React**, **React Native**, **Flutter** ou qualquer cliente HTTP.

Destaques técnicos:
- ⚡ **FastAPI** — performance próxima ao Node.js e Go, com tipagem estática Python
- 🔐 **JWT Bearer Token** — autenticação stateless e segura
- 🔒 **bcrypt** — hash de senhas com salt automático
- 🗃️ **SQLAlchemy ORM** — abstração do banco com modelos relacionais
- ✅ **Pydantic** — validação e serialização de dados na entrada e saída
- 📄 **Swagger/OpenAPI** — documentação gerada automaticamente

---

## 🚀 Rodando Localmente

```bash
# 1. Clone o repositório
git clone https://github.com/IsraelSiq/barber-booking-api.git
cd barber-booking-api

# 2. Crie e ative o ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Inicie o servidor de desenvolvimento
python -m uvicorn main:app --reload
```

✅ API disponível em: **http://localhost:8000**  
📚 Documentação interativa em: **http://localhost:8000/docs**

---

## 📡 Endpoints

### 🔐 Autenticação
| Método | Rota | Descrição | Auth |
|---|---|---|---|
| `POST` | `/auth/register` | Cadastrar novo cliente | ❌ |
| `POST` | `/auth/login` | Login e geração de token JWT | ❌ |

### 👤 Clientes
| Método | Rota | Descrição | Auth |
|---|---|---|---|
| `GET` | `/clientes/` | Listar todos os clientes | ✅ |
| `GET` | `/clientes/{id}` | Buscar cliente por ID | ✅ |

### 📅 Agendamentos
| Método | Rota | Descrição | Auth |
|---|---|---|---|
| `GET` | `/agendamentos/disponiveis?data=YYYY-MM-DD` | Horários disponíveis | ❌ |
| `POST` | `/agendamentos/` | Criar novo agendamento | ✅ |
| `GET` | `/agendamentos/meus` | Listar meus agendamentos | ✅ |
| `DELETE` | `/agendamentos/{id}` | Cancelar agendamento | ✅ |

---

## 📁 Estrutura do Projeto

```
barber-booking-api/
├── main.py              # Entrypoint — instância FastAPI e registro de rotas
├── auth.py              # Lógica de autenticação JWT
├── database.py          # Configuração SQLAlchemy + engine SQLite
├── models.py            # Modelos ORM (tabelas do banco)
├── schemas.py           # Schemas Pydantic (validação de entrada/saída)
├── routes/
│   ├── auth.py          # Rotas: register e login
│   ├── clientes.py      # Rotas: CRUD de clientes
│   └── agendamentos.py  # Rotas: criação, listagem e cancelamento
├── requirements.txt     # Dependências do projeto
└── README.md
```

---

## 🛠️ Stack Tecnológica

| Tecnologia | Função |
|---|---|
| **Python 3.11+** | Linguagem principal |
| **FastAPI** | Framework web ASGI de alta performance |
| **SQLAlchemy** | ORM para mapeamento objeto-relacional |
| **SQLite** | Banco de dados leve e sem configuração |
| **Pydantic v2** | Validação e serialização de dados |
| **python-jose** | Geração e validação de tokens JWT |
| **passlib + bcrypt** | Hash seguro de senhas |
| **Uvicorn** | Servidor ASGI para produção e desenvolvimento |
| **Railway** | Plataforma de deploy em nuvem |

---

## 🔗 Projetos Relacionados

- 🖥️ **Front-end Web:** [barber-booking-web](https://github.com/IsraelSiq/barber-booking-web) — interface React que consome esta API

---

## 👨‍💻 Autor

**Israel Siqueira**  
Desenvolvedor Python | FastAPI | React  
[![GitHub](https://img.shields.io/badge/GitHub-IsraelSiq-181717?style=flat&logo=github)](https://github.com/IsraelSiq)
