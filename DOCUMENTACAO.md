# Documentação Técnica - Notify Me API

## 1. Visão geral

O `Notify Me API` é um serviço HTTP em FastAPI responsável por enviar notificações por e-mail para dois domínios:

- `Antonio Claudio Dev`: mensagens de contato do portfólio
- `Arena Manager`: e-mails de verificação e notificações operacionais

Os envios são executados em segundo plano com `BackgroundTasks`, reduzindo latência da resposta HTTP.

---

## 2. Arquitetura do projeto

```text
api/index.py
  └── expõe app FastAPI para deploy (Vercel)

app/main.py
  ├── inicializa FastAPI
  ├── configura CORS
  └── registra routers

app/core/config.py
  └── carrega variáveis de ambiente via BaseSettings

app/modules/antonio_claudio_dev/
  ├── router.py
  └── service.py

app/modules/arena_manager/
  ├── router.py
  └── service.py

app/schemas/
  ├── contact.py
  ├── email_verification.py
  ├── user.py
  ├── arena.py
  └── court.py

app/tests/
  ├── conftest.py
  ├── antonio_claudio_dev/
  │   └── test_antonio_claudio_dev_routes.py
  └── arena_manager/
      └── test_arena_manager_routes.py
```

### Responsabilidades

- `router.py`: define endpoints, valida input e agenda tarefas de envio
- `service.py`: monta e envia e-mails (texto + HTML)
- `schemas/`: define contratos de entrada e validações
- `config.py`: centraliza parâmetros de infraestrutura (SMTP e URLs)

---

## 3. Configuração e ambiente

### Dependências principais

- `fastapi`
- `uvicorn`
- `pydantic`
- `pydantic-settings`
- `email-validator`
- `pytz`

### Variáveis de ambiente obrigatórias

| Variável                      | Descrição                                  |
| ----------------------------- | ------------------------------------------ |
| `SMTP_HOST`                   | Host SMTP                                  |
| `SMTP_PORT`                   | Porta SMTP (ex.: 465 ou 587)               |
| `SMTP_USER`                   | Usuário SMTP                               |
| `SMTP_PASS`                   | Senha/credencial SMTP                      |
| `MAIL_TO`                     | Destinatário padrão do portfólio           |
| `MAIL_FROM_ANTONIOCLAUDIODEV` | Remetente dos e-mails do portfólio         |
| `MAIL_FROM_ARENAMANAGER`      | Remetente dos e-mails do Arena Manager     |
| `FRONTEND_URL`                | URL base do frontend (link de verificação) |

### Comportamento de conexão SMTP

- Porta `465`: conexão segura com `SMTP_SSL`
- Outras portas: conexão com `SMTP` + `starttls()`

---

## 4. Endpoints e contratos

## 4.1 `GET /`

Retorna mensagem de boas-vindas.

**Response**

```json
{
  "message": "Welcome to the Notify Me API"
}
```

## 4.2 `POST /notifications/antonio-claudio-dev/contact/`

Envia mensagem de contato para o e-mail configurado em `MAIL_TO`.

**Request (`RequestContact`)**

```json
{
  "name": "Antonio Claudio",
  "email": "antonio@email.com",
  "message": "Olá! Gostaria de conversar sobre um projeto."
}
```

**Validações**

- `name`: mínimo 6 caracteres
- `email`: formato válido (`EmailStr`)
- `message`: mínimo 10 caracteres

## 4.3 `POST /notifications/arena-manager/verification`

Envia e-mail de verificação de conta com link contendo token.

**Request (`RequestEmailVerification`)**

```json
{
  "email": "user@email.com",
  "token": "token-de-verificacao"
}
```

**Detalhe do link gerado**

`{FRONTEND_URL}/auth/verify-email?token={token}`

## 4.4 `POST /notifications/arena-manager/owner-promotion`

Envia notificação de promoção para dono da arena.

**Request**

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

## 4.5 `POST /notifications/arena-manager/new-court`

Envia notificação de nova quadra criada.

**Request**

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

### Respostas padrão dos POSTs

- `201 Created`: e-mail agendado para envio em background
- `500 Internal Server Error`: falha ao enviar e-mail

---

## 5. Fluxos internos

## 5.1 Fluxo HTTP -> envio

1. Requisição chega ao endpoint
2. FastAPI valida payload via schema Pydantic
3. Endpoint agenda método de serviço em `BackgroundTasks`
4. Resposta `201` é retornada sem aguardar envio efetivo
5. Serviço monta `EmailMessage` (texto + HTML)
6. Serviço conecta no SMTP e dispara `send_message`

## 5.2 Segurança de conteúdo

- Conteúdos interpolados em HTML usam `html.escape` para evitar injeção no template HTML do e-mail.

## 5.3 Fuso horário

- As mensagens formatam data/hora em `America/Sao_Paulo` com base em horário UTC.

---

## 6. Deploy

## 6.1 Ambiente serverless

- `api/index.py` exporta o objeto `app` para execução em plataformas como Vercel.

## 6.2 Checklist para produção

- Configurar todas as variáveis de ambiente
- Garantir credenciais SMTP válidas
- Definir `FRONTEND_URL` correto do ambiente
- Validar política de CORS conforme frontend oficial

---

## 7. Testes automatizados

Os testes automatizados usam `pytest` e cobrem as rotas principais da API.

### Organização

- `app/tests/conftest.py`: fixtures compartilhadas (`client`, `sent_emails`) e mocks dos serviços de envio de e-mail
- `app/tests/antonio_claudio_dev/test_antonio_claudio_dev_routes.py`: testes das rotas do módulo Antonio Claudio Dev
- `app/tests/arena_manager/test_arena_manager_routes.py`: testes das rotas do módulo Arena Manager

### Cobertura atual

- `GET /` (health/home)
- `POST /notifications/antonio-claudio-dev/contact/` (sucesso + validação 422)
- `POST /notifications/arena-manager/verification` (sucesso + validação 422)
- `POST /notifications/arena-manager/owner-promotion` (sucesso)
- `POST /notifications/arena-manager/new-court` (sucesso)

### Execução

```bash
pytest
```

Ou:

```bash
pytest -q
```

---

## 8. Melhorias recomendadas

- Adicionar logs estruturados para rastrear tentativas/falhas de envio
- Padronizar tratamento de exceções por tipo de erro SMTP
- Ampliar cobertura de testes para cenários de erro interno (`500`) e contratos de resposta detalhados
- Restringir `CORS` para domínios confiáveis em produção
