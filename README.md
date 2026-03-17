# 💈 Barber Booking API

> **REST API de agendamento para barbearia** — autenticação JWT, login com Google OAuth2, gerenciamento completo de clientes, agendamentos, painel administrativo e recuperação de senha via email.

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Neon](https://img.shields.io/badge/Database-Neon-00E699?style=for-the-badge&logo=neon&logoColor=black)](https://neon.tech)
[![Railway](https://img.shields.io/badge/Deploy-Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)](https://railway.app)
[![JWT](https://img.shields.io/badge/Auth-JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://jwt.io)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## 🌐 Deploy ao Vivo

| Recurso | URL |
|---|---|
| 🚀 API Base | https://barber-booking-api.up.railway.app |
| 📚 Swagger UI | https://barber-booking-api.up.railway.app/docs |
| 📖 ReDoc | https://barber-booking-api.up.railway.app/redoc |

---

## 🧠 Sobre o Projeto

Esta API foi construída com **FastAPI** e segue os princípios REST, oferecendo endpoints para autenticação segura (email/senha e Google OAuth2), gerenciamento de clientes, controle de agendamentos e painel administrativo. O banco de dados é **PostgreSQL hospedado no Neon** — persistente entre deploys. Monitorada 24/7 via **Freshping** para garantir disponibilidade em produção.

Destaques técnicos:
- ⚡ **FastAPI** — performance próxima ao Node.js e Go, com tipagem estática Python
- 🔐 **JWT Bearer Token** — autenticação stateless e segura
- 🐈 **Google OAuth2** — login/cadastro via conta Google com validação do token no servidor
- 🔒 **bcrypt** — hash de senhas com salt automático
- 🗃️ **SQLAlchemy ORM** — abstração do banco com modelos relacionais
- ✅ **Pydantic v2** — validação e serialização de dados
- 📧 **Resend** — envio de emails transacionais (boas-vindas, reset de senha)
- 👑 **Roles (admin/cliente)** — controle de acesso por perfil
- 🐘 **Neon PostgreSQL** — banco externo persistente, dados nunca resetam em deploy
- 📄 **Swagger/OpenAPI** — documentação gerada automaticamente

---

## 🚀 Rodando Localmente

```bash
# 1. Clone o repositório
git clone https://github.com/IsraelSiq/barber-booking-api.git
cd barber-booking-api

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas credenciais

# 5. Inicie o servidor
python -m uvicorn main:app --reload
```

✅ API disponível em: **http://localhost:8000**  
📚 Documentação interativa em: **http://localhost:8000/docs**

> 💡 Localmente, se `DATABASE_URL` não estiver definida, a API usa SQLite automaticamente.

---

## 🔑 Variáveis de Ambiente

```env
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
SECRET_KEY=sua_chave_secreta_jwt
RESEND_API_KEY=re_sua_chave_resend
FRONTEND_URL=https://barber-booking-web.vercel.app
```

---

## 📡 Endpoints

### 🔐 Autenticação
| Método | Rota | Descrição | Auth |
|---|---|---|---|
| `POST` | `/auth/register` | Cadastrar novo cliente | ❌ |
| `POST` | `/auth/login` | Login e geração de token JWT | ❌ |
| `POST` | `/auth/google` | Login/cadastro via Google (id_token) | ❌ |
| `POST` | `/auth/google-token` | Login/cadastro via Google (access_token + userinfo) | ❌ |
| `GET` | `/auth/me` | Dados do usuário autenticado | ✅ |
| `PUT` | `/auth/me` | Atualizar dados do usuário | ✅ |
| `POST` | `/auth/forgot-password` | Solicitar redefinição de senha | ❌ |
| `GET` | `/auth/reset-password` | Validar token de redefinição | ❌ |
| `POST` | `/auth/reset-password` | Redefinir senha via token de email | ❌ |
| `POST` | `/auth/redefinir-senha` | Redefinir senha (primeiro acesso admin) | ✅ |

### 👤 Clientes
| Método | Rota | Descrição | Auth |
|---|---|---|---|
| `GET` | `/clientes/` | Listar todos os clientes | 👑 Admin |
| `GET` | `/clientes/{id}` | Buscar cliente por ID | ✅ |
| `PUT` | `/clientes/{id}` | Atualizar dados do cliente | ✅ |

### 📅 Agendamentos
| Método | Rota | Descrição | Auth |
|---|---|---|---|
| `GET` | `/agendamentos/disponiveis` | Horários disponíveis por data | ❌ |
| `POST` | `/agendamentos/` | Criar novo agendamento | ✅ |
| `GET` | `/agendamentos/meus` | Listar meus agendamentos | ✅ |
| `DELETE` | `/agendamentos/{id}` | Cancelar agendamento | ✅ |
| `GET` | `/agendamentos/admin` | Listar todos os agendamentos | 👑 Admin |
| `PATCH` | `/agendamentos/{id}/status` | Atualizar status do agendamento | 👑 Admin |

---

## 📁 Estrutura do Projeto

```
barber-booking-api/
├── main.py              # Entrypoint — instância FastAPI e registro de rotas
├── auth.py              # Lógica de autenticação JWT
├── database.py          # Configuração SQLAlchemy + engine PostgreSQL (Neon)
├── models.py            # Modelos ORM (tabelas do banco)
├── schemas.py           # Schemas Pydantic (validação de entrada/saída)
├── notifications.py     # Integração com Resend para envio de emails
├── routes/
│   ├── auth.py          # Rotas: register, login, google, google-token, reset-password
│   ├── clientes.py      # Rotas: CRUD de clientes
│   └── agendamentos.py  # Rotas: criação, listagem, cancelamento e admin
├── requirements.txt     # Dependências do projeto
├── Procfile             # Configuração de inicialização Railway
├── railway.json         # Configurações Railway
└── README.md
```

---

## 🛠️ Stack Tecnológica

| Tecnologia | Função |
|---|---|
| **Python 3.12** | Linguagem principal |
| **FastAPI** | Framework web ASGI de alta performance |
| **SQLAlchemy** | ORM para mapeamento objeto-relacional |
| **PostgreSQL + Neon** | Banco de dados relacional persistente em nuvem |
| **pg8000** | Driver PostgreSQL pure-Python (sem dependências de sistema) |
| **Pydantic v2** | Validação e serialização de dados |
| **python-jose** | Geração e validação de tokens JWT |
| **passlib + bcrypt** | Hash seguro de senhas |
| **httpx** | Validação do token Google OAuth2 |
| **Resend** | Envio de emails transacionais |
| **Uvicorn** | Servidor ASGI para produção e desenvolvimento |
| **Railway** | Plataforma de deploy em nuvem |
| **Freshping** | Monitoramento de disponibilidade 24/7 |

---

## 🔗 Projetos Relacionados

- 🖥️ **Front-end Web:** [barber-booking-web](https://github.com/IsraelSiq/barber-booking-web) — interface React que consome esta API

---

## 👨‍💻 Autor

**Israel Siqueira**  
Desenvolvedor Python | FastAPI | React  
[![GitHub](https://img.shields.io/badge/GitHub-IsraelSiq-181717?style=flat&logo=github)](https://github.com/IsraelSiq)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Israel_Siqueira-0077B5?style=flat&logo=linkedin)](https://linkedin.com/in/IsraelSiq)
