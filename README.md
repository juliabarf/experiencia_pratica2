# Connect API

API REST de prototipagem (MVP) para gerenciamento de usuarios, com persistencia
simulada em memoria (sem banco de dados real).

## Estrutura

```
connect-api/
├── app/
│   ├── __init__.py          # Factory da aplicacao Flask
│   ├── data/
│   │   └── db.py            # Estrutura em memoria + gerador de IDs
│   └── routes/
│       └── user_routes.py   # Rotas CRUD de usuarios (GET, POST, PUT, DELETE)
├── run.py                   # Ponto de entrada
├── requirements.txt
└── README.md
```

## Como rodar

1. Crie um ambiente virtual (opcional, mas recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

2. Instale as dependencias:

   ```bash
   pip install -r requirements.txt
   ```

3. Rode o servidor:

   ```bash
   python run.py
   ```

4. A API estara disponivel em `http://127.0.0.1:5000`.

## Endpoints

| Metodo | Rota            | Descricao                        | Status de sucesso |
|--------|-----------------|-----------------------------------|--------------------|
| GET    | `/users`        | Lista todos os usuarios           | 200                |
| GET    | `/users/<id>`   | Busca um usuario pelo ID          | 200 / 404          |
| POST   | `/users`        | Cria um novo usuario              | 201 / 400          |
| PUT    | `/users/<id>`   | Atualiza um usuario existente     | 200 / 400 / 404    |
| DELETE | `/users/<id>`   | Remove um usuario                 | 204 / 404          |

Todas as respostas seguem o envelope padrao `{"data": ...}` em sucesso ou
`{"error": "..."}` em falha.

## Exemplos de uso (curl)

Criar um usuario:

```bash
curl -X POST http://127.0.0.1:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Ana Souza", "email": "ana@email.com"}'
```

Listar usuarios:

```bash
curl http://127.0.0.1:5000/users
```

Buscar um usuario por ID:

```bash
curl http://127.0.0.1:5000/users/1
```

Atualizar um usuario:

```bash
curl -X PUT http://127.0.0.1:5000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Ana Souza Lima"}'
```

Remover um usuario:

```bash
curl -X DELETE http://127.0.0.1:5000/users/1
```

## Observacao importante

Os dados residem em memoria RAM enquanto o processo estiver ativo. Ao
reiniciar o servidor, todos os registros sao perdidos — comportamento
esperado nesta fase de MVP, ate que a persistencia real (banco de dados)
seja introduzida.
