# Sistema Acadêmico Multiplataforma

Sistema acadêmico simples para cadastro de alunos e lançamento de notas, com front-end em React + TypeScript, back-end em FastAPI, persistência em MongoDB e cache/estruturas em Redis. O projeto está preparado para rodar tanto via Docker Compose (ambiente local) quanto via manifests Kubernetes (deploy em cluster).

## Stack

**Back-end**
- Python 3.13 + FastAPI
- [Beanie](https://beanie-odm.dev/) (ODM assíncrono para MongoDB)
- [redis-om](https://github.com/redis/redis-om-python) para os modelos espelhados no Redis
- Uvicorn como servidor ASGI

**Front-end**
- React + TypeScript
- Vite
- Tailwind CSS
- Axios para chamadas HTTP

**Infraestrutura**
- MongoDB 8.0
- Redis Stack
- Docker / Docker Compose
- Kubernetes (Deployments, Services, ConfigMap, PVC)

## Estrutura do projeto

```
.
├── backend/
│   ├── app.py                  # criação e configuração da aplicação FastAPI
│   ├── config.py                # leitura de variáveis de ambiente (Mongo, Redis, porta)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── src/
│       ├── database/            # conexão com MongoDB (Beanie) e Redis
│       ├── enums/                # enums da aplicação (ex.: situação da nota)
│       ├── exceptions/           # exceções customizadas
│       ├── handlers/             # tratamento global de exceções
│       ├── middleware/           # configuração de CORS
│       ├── models/               # documentos Beanie e modelos Redis (Aluno, Notas)
│       ├── routes/               # rotas HTTP (/aluno, /notas)
│       ├── schemas/              # schemas Pydantic (entrada/saída, paginação)
│       └── services/             # regras de negócio
├── frontend/
│   ├── src/
│   │   ├── components/           # formulários, tabelas, paginação, mensagens
│   │   ├── hooks/                 # useListaPaginada, useMensagem
│   │   ├── services/              # chamadas à API (alunoService, notaService)
│   │   ├── App.tsx
│   │   └── tipos.ts
│   ├── dockerfile
│   └── package.json
├── kubernetes/
│   ├── backend-deployment.yaml / backend-service.yaml
│   ├── frontend-deployment.yaml / frontend-service.yaml
│   ├── database-deployment.yaml / database-service.yaml / database-pvc.yaml
│   ├── redis-deployment.yaml / redis-service.yaml
│   └── configmap.yaml
└── docker-compose.yml
```

## Funcionalidades

- Cadastro, listagem (paginada), atualização e exclusão de **alunos** (`/aluno`)
- Cadastro, listagem (paginada), consulta e exclusão de **notas** (`/notas`), vinculadas a um aluno
- Cálculo de média e situação do aluno (`APROVADO`, `EXAME`, `REPROVADO`)
- Paginação via query params `page` e `size` (limite de 25 itens por página)
- Interface web para cadastro de alunos, lançamento de notas e visualização em tabelas

## Rotas da API

### Alunos (`/aluno`)
| Método | Rota | Descrição |
|---|---|---|
| POST | `/aluno/` | Cria um aluno |
| GET | `/aluno/` | Lista alunos (paginado) |
| GET | `/aluno/{id}` | Busca aluno por ID |
| PUT | `/aluno/{id}` | Atualiza aluno |
| DELETE | `/aluno/{id}` | Remove aluno |

### Notas (`/notas`)
| Método | Rota | Descrição |
|---|---|---|
| POST | `/notas/` | Cria uma nota (P1, P2, calcula média e situação) |
| GET | `/notas/` | Lista notas (paginado) |
| GET | `/notas/{id}` | Busca nota por ID |
| PUT | `/notas/{id}` | Atualiza nota |
| DELETE | `/notas/{id}` | Remove nota |

## Como rodar localmente (Docker Compose)

Pré-requisitos: Docker e Docker Compose instalados.

1. Crie o arquivo `backend/.env` com as variáveis necessárias, por exemplo:

   ```env
   DB_HOST=mongodb
   DB_PORT=27017
   DB_NAME=sistema_academico
   REDIS_HOST=redis
   REDIS_PORT=6379
   PORT=8000
   ```

2. Suba os serviços:

   ```bash
   docker compose up --build
   ```

3. Acesse:
   - Front-end: [http://localhost:5173](http://localhost:5173)
   - API (back-end): [http://localhost:8000](http://localhost:8000)
   - Documentação interativa da API (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)
   - Interface do Redis Stack: [http://localhost:8001](http://localhost:8001)

> Observação: o serviço MongoDB não usa autenticação por padrão neste projeto (`DB_USER`/`DB_PASSWORD` vazios); se preferir habilitar, defina essas variáveis tanto no `docker-compose.yml` quanto no `.env` do back-end.

## Como rodar sem Docker (desenvolvimento)

**Back-end**
```bash
cd backend
pip install -r requirements.txt
python app.py --dev
```
A flag `--dev` faz o back-end se conectar em `localhost` para Mongo e Redis, em vez dos hostnames usados nos containers.

**Front-end**
```bash
cd frontend
npm install
npm run dev
```

## Deploy em Kubernetes

Os manifests em `kubernetes/` cobrem os quatro componentes da aplicação (front-end, back-end, banco de dados e Redis), com configuração centralizada no `ConfigMap` (`app-config`) e armazenamento persistente do MongoDB via `PersistentVolumeClaim`.

Para aplicar todos os manifests:

```bash
kubectl apply -f kubernetes/
```

Isso cria, entre outros recursos:
- `Deployment` + `Service` do back-end (2 réplicas)
- `Deployment` + `Service` do front-end
- `Deployment` + `Service` + `PVC` do MongoDB
- `Deployment` + `Service` do Redis
- `ConfigMap` com as variáveis de conexão (`DB_HOST`, `DB_PORT`, `DB_NAME`, `REDIS_HOST`, `REDIS_PORT`, `PORT`)

> As imagens referenciadas nos deployments (por exemplo, `backend:v1`) precisam ser construídas e publicadas em um registro acessível pelo cluster antes do deploy, ou carregadas localmente caso esteja usando um cluster como Kind/Minikube.

## Variáveis de ambiente (back-end)

| Variável | Descrição | Padrão |
|---|---|---|
| `DB_HOST` | Host do MongoDB | `mongodb` |
| `DB_PORT` | Porta do MongoDB | `27017` |
| `DB_NAME` | Nome do banco | — |
| `DB_USER` / `DB_PASSWORD` | Credenciais do Mongo (opcionais) | — |
| `REDIS_HOST` | Host do Redis | `redis` |
| `REDIS_PORT` | Porta do Redis | `6379` |
| `REDIS_PASSWORD` | Senha do Redis (opcional) | — |
| `PORT` | Porta da API | `8000` |
