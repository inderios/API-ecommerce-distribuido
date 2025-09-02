# API-ecommerce-distribuido
API de Gateway de pagamentos para ecommerce distribuído - FastAPI, NGNIX e Redis

# Estrutura de diretórios e arquivos
payment-gateway-api/
│
├── docker/
│   ├── nginx/
│   │   ├── nginx.conf                # Configuração do balanceador NGINX
│   │   └── Dockerfile                # Dockerfile do NGINX
│   ├── gateway/
│   │   └── Dockerfile                # Dockerfile do serviço FastAPI
│   └── redis/
│       └── redis.conf                # Configuração opcional do Redis
│
├── src/
│   ├── gateway/                      # Código da API dos Gateways
│   │   ├── main.py                   # Entry point da API
│   │   ├── routes/                   # Endpoints da aplicação
│   │   │   ├── auth.py               # Endpoints de autenticação
│   │   │   ├── payments.py           # Endpoints de processamento de pagamentos
│   │   │   ├── orders.py             # Endpoints de pedidos
│   │   │   └── health.py             # Endpoint de health check
│   │   ├── services/                 # Lógica de negócio
│   │   │   ├── payment_service.py    # Lógica para transações
│   │   │   ├── order_service.py      # Lógica de pedidos
│   │   │   └── cache_service.py      # Interação com Redis
│   │   ├── common/                   # Utilitários comuns
│   │   │   ├── database.py           # Conexão com banco relacional
│   │   │   ├── redis_client.py       # Conexão com Redis
│   │   │   ├── config.py             # Variáveis de ambiente e configs
│   │   │   └── logger.py             # Configuração de logs
│   │   └── models/                   # Modelos Pydantic e ORM
│   │       ├── transaction_model.py
│   │       ├── order_model.py
│   │       └── user_model.py
│   │
│   └── tests/                        # Testes unitários e de integração
│       ├── test_auth.py
│       ├── test_payments.py
│       ├── test_orders.py
│       └── conftest.py
│
├── scripts/
│   ├── demo.sh                       # Script de inicialização local
│   └── seed_db.py                    # Popular o banco com dados de exemplo
│
├── docker-compose.yml                # Orquestração dos containers
├── requirements.txt                  # Dependências Python
├── README.md                         # Documentação principal
└── .env                              # Variáveis de ambiente
