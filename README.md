# Tasks API

API REST para gerenciamento de tarefas, construída com **FastAPI**, **SQLAlchemy** e **PostgreSQL**, rodando em containers Docker.

---

## Tecnologias

| Camada         | Ferramenta            |
| -------------- | --------------------- |
| Framework web  | FastAPI               |
| Servidor ASGI  | Uvicorn               |
| ORM            | SQLAlchemy            |
| Banco de dados | PostgreSQL            |
| Configuração   | pydantic-settings     |
| Infra          | Docker / Docker Compose |

---

## Estrutura do projeto

```
tasks_api/
├── app/
│   ├── __init__.py
│   ├── main.py          # Cria a aplicação e registra os routers
│   ├── database.py      # Conexão com o banco e sessão
│   ├── models.py        # Tabelas do banco (SQLAlchemy)
│   ├── schemas.py       # Validação de entrada/saída (Pydantic)
│   └── routers/
│       └── task.py      # Endpoints de tarefas
|
├── docker-compose.yml   # Orquestra API + PostgreSQL
├── DockerFile           # Imagem da API
├── requirements.txt     # Dependências Python
├── .env                 # Variáveis de ambiente (não versionar)
└── .env.example         # Exemplo de configuração
```

---

## Como rodar o projeto

### 1. Configurar as variáveis de ambiente

Copie o arquivo de exemplo e preencha os valores:

```bash
cp .env.example .env
```

O `.env` deve conter:

```env
DATABASE_HOSTNAME=postgres
DATABASE_PORT=5432
DATABASE_NAME=nome do banco
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=sua senha
```

### 2. Subir com Docker Compose 

```bash
docker compose up --build
```

Isso irá:

- Construir a imagem da API a partir do `DockerFile`;
- Subir o PostgreSQL;
- Iniciar o Uvicorn em modo `--reload` na porta `8000`.

Acesse:

- API: http://localhost:8000
- Documentação interativa (Swagger UI): http://localhost:8000/docs
- Documentação alternativa (ReDoc): http://localhost:8000/redoc

Para parar:

```bash
docker compose down
```

Para parar e apagar também os dados do banco:

```bash
docker compose down -v
```

---

## Códigos de status HTTP

Cada resposta usa um código que indica **o que aconteceu** na requisição. Isso permite que o cliente (front-end, app, outro serviço) saiba como reagir sem precisar interpretar o corpo da resposta.

### 2xx — Sucesso

| Código | Nome        | Por que é usado                                                        |
| ------ | ----------- | ---------------------------------------------------------------------- |
| `200`  | OK          | A requisição foi bem-sucedida e há um corpo de resposta. Usado no `GET /task/`. |
| `201`  | Created     | Um novo recurso foi criado com sucesso. Usado no `POST /task/`. O corpo retorna o recurso criado (com o `id` gerado pelo banco). |
| `204`  | No Content  | Sucesso, mas sem corpo de resposta. Útil em `DELETE`/`PUT` que não retornam dados. |

Por que diferenciar `200` de `201`? O `201` avisa o cliente que **um registro novo passou a existir** e normalmente inclui o local/ID dele. O `200` apenas confirma que uma leitura ou operação existente deu certo.

### 4xx — Erro do cliente

| Código | Nome                 | Por que é usado                                                 |
| ------ | -------------------- | -------------------------------------------------------------- |
| `400`  | Bad Request          | A requisição está malformada ou viola uma regra de negócio.   |
| `401`  | Unauthorized         | Falta autenticação ou o token é inválido.                     |
| `403`  | Forbidden            | O usuário está autenticado, mas não tem permissão.            |
| `404`  | Not Found            | O recurso pedido não existe (ex.: `GET /task/999`).          |
| `422`  | Unprocessable Entity | Os dados enviados não passaram na validação do Pydantic (campo faltando, tipo errado). O FastAPI retorna isso automaticamente. |

A diferença entre `401` e `403`: `401` é "quem é você?" (não autenticado) e `403` é "eu sei quem você é, mas você não pode fazer isso" (autenticado sem permissão).

### 5xx — Erro do servidor

| Código | Nome                 | Por que é usado                                          |
| ------ | -------------------- | ------------------------------------------------------- |
| `500`  | Internal Server Error| Algo quebrou no servidor (ex.: banco fora do ar, bug). Não é culpa do cliente. |

> Regra prática: `4xx` = o cliente errou; `5xx` = o servidor errou.

---

