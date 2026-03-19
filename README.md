# Ingestão e Busca Semântica com LangChain e PostgreSQL + pgVector

Projeto desenvolvido para o desafio do MBA com os requisitos de:
- ingestão de PDF
- armazenamento vetorial em PostgreSQL com pgVector
- busca semântica via CLI
- resposta baseada apenas no conteúdo do PDF

## Tecnologias
- Python 3.11
- LangChain
- PostgreSQL
- pgVector
- Docker / Docker Compose
- OpenAI API

## Estrutura do projeto

```text
.
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── document.pdf
├── README.md
└── src/
    ├── ingest.py
    ├── search.py
    └── chat.py
```

## Pré-requisitos
Antes de executar, é necessário ter instalado:
Python 3.11
Docker Desktop
Git

## Configuração do ambiente

1. Clonar o repositório
```text
git clone https://github.com/SEU_USUARIO/mba-ia-desafio-ingestao-busca.git
cd mba-ia-desafio-ingestao-busca
```

2. Criar e ativar o ambiente virtual
```text
python3.11 -m venv venv
source venv/bin/activate
```

3. Instalar as dependências
```text
python -m pip install -r requirements.txt
python -m pip install truststore
Configuração das variáveis de ambiente
```

4. Criar o arquivo .env
Crie um arquivo .env na raiz do projeto com base no .env.example.
Exemplo:
OPENAI_API_KEY=sua_api_key_aqui
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/postgres
PG_VECTOR_COLLECTION_NAME=pdf_chunks
PDF_PATH=./document.pdf
Execução do projeto

5. Subir o banco PostgreSQL com pgVector
```text
docker compose up -d
```

6. Executar a ingestão do PDF
```text
export SSL_CERT_FILE=$(python -m certifi)
python src/ingest.py
```

7. Rodar o chat no terminal
```text
export SSL_CERT_FILE=$(python -m certifi)
python src/chat.py
```

## Exemplo de uso

Faça sua pergunta:
PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
RESPOSTA: O faturamento foi de 10 milhões de reais.

Perguntas fora do contexto:
PERGUNTA: Quantos clientes temos em 2024?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.

## Observações
- O projeto responde somente com base no conteúdo do PDF ingerido.
- O arquivo .env não deve ser versionado.
- É necessário possuir crédito ativo na API da OpenAI para executar embeddings e geração de resposta.

Autor
Thomas Lagos