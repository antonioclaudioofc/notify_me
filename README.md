# Notify Me API

API em FastAPI para envio de notificações por e-mail em dois contextos:

- Contato do portfólio `Antonio Claudio Dev`
- Notificações transacionais do sistema `Arena Manager`

O projeto dispara os e-mails em segundo plano usando `BackgroundTasks`.

## Stack

- Python + FastAPI
- Pydantic (validação de dados)
- SMTP (`smtplib`) para envio de e-mails
- Deploy serverless na Vercel (`api/index.py`)

## Estrutura do projeto

```text
api/
  index.py                  # entrypoint para Vercel
app/
  main.py                   # criação da aplicação FastAPI
  core/
    config.py               # variáveis de ambiente
  modules/
    antonio_claudio_dev/    # rota + serviço de contato do portfólio
    arena_manager/          # rotas + serviços de notificações do sistema
  schemas/                  # contratos de entrada (Pydantic)
  tests/
    conftest.py             # fixtures compartilhadas e mocks de e-mail
    antonio_claudio_dev/
      test_antonio_claudio_dev_routes.py
    arena_manager/
      test_arena_manager_routes.py
```

## Instalação

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Variáveis de ambiente

Crie um arquivo `.env` na raiz com:

```env
SMTP_HOST=smtp.seu-provedor.com
SMTP_PORT=465
SMTP_USER=seu_usuario
SMTP_PASS=sua_senha
MAIL_TO=destinatario@dominio.com
MAIL_FROM_ANTONIOCLAUDIODEV=nao-responda@seudominio.com
MAIL_FROM_ARENAMANAGER=nao-responda@seudominio.com
FRONTEND_URL=https://seu-frontend.com
```

## Executando localmente

```bash
uvicorn app.main:app --reload
```

Aplicação disponível em `http://127.0.0.1:8000`.

## Endpoints

### Health

- `GET /`

Resposta:

```json
{
  "message": "Welcome to the Notify Me API"
}
```

### Contato do portfólio

- `POST /notifications/antonio-claudio-dev/contact/`

Body:

```json
{
  "name": "Antonio Claudio",
  "email": "antonio@email.com",
  "message": "Olá! Gostei muito do seu trabalho."
}
```

Validações:

- `name`: mínimo de 6 caracteres
- `email`: formato válido
- `message`: mínimo de 10 caracteres

### Arena Manager - verificação de e-mail

- `POST /notifications/arena-manager/verification`

Body:

```json
{
  "email": "user@email.com",
  "token": "token-de-verificacao"
}
```

### Arena Manager - promoção de dono de arena

- `POST /notifications/arena-manager/owner-promotion`

Body:

```json
{
  "user": {
    "id": 1,
    "name": "João",
    "email": "joao@email.com"
  },
  "arena": {
    "id": 10,
    "name": "Arena Centro"
  }
}
```

### Arena Manager - nova quadra criada

- `POST /notifications/arena-manager/new-court`

Body:

```json
{
  "user": {
    "id": 1,
    "name": "João",
    "email": "joao@email.com"
  },
  "arena": {
    "id": 10,
    "name": "Arena Centro"
  },
  "court": {
    "id": 25,
    "name": "Quadra 01"
  }
}
```

## Respostas esperadas

- `201 Created`: solicitação recebida e e-mail enfileirado em background
- `500 Internal Server Error`: falha ao processar envio

## Observações de SMTP

- Se `SMTP_PORT=465`, o envio usa `SMTP_SSL`
- Em outras portas (ex.: `587`), o envio usa `starttls()`

## Testes

O projeto possui testes de rotas com `pytest`, separados por módulo em `app/tests`.

Executar todos os testes:

```bash
pytest
```

Ou em modo resumido:

```bash
pytest -q
```
