import os
import certifi
import truststore

truststore.inject_into_ssl()
os.environ.setdefault("SSL_CERT_FILE", certifi.where())

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_postgres import PGVector

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_CHAT_MODEL = "gpt-5-nano"

FALLBACK_RESPONSE = "Não tenho informações necessárias para responder sua pergunta."

PROMPT_TEMPLATE = """CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


def build_vector_store():
    embeddings = OpenAIEmbeddings(
        model=OPENAI_EMBEDDING_MODEL,
        api_key=OPENAI_API_KEY,
    )

    return PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=DATABASE_URL,
    )


def retrieve_context(question: str, k: int = 10):
    vector_store = build_vector_store()
    results = vector_store.similarity_search_with_score(question, k=k)

    if not results:
        return "", []

    docs = [doc for doc, _score in results]
    context = "\n\n---\n\n".join(doc.page_content for doc in docs if doc.page_content.strip())
    return context, results


def answer_question(question: str) -> str:
    context, results = retrieve_context(question, k=10)

    if not results or not context.strip():
        return FALLBACK_RESPONSE

    llm = ChatOpenAI(
        model=OPENAI_CHAT_MODEL,
        api_key=OPENAI_API_KEY,
        temperature=0,
    )

    prompt = PROMPT_TEMPLATE.format(
        contexto=context,
        pergunta=question,
    )

    response = llm.invoke(prompt)
    content = response.content if hasattr(response, "content") else str(response)

    if not content or not str(content).strip():
        return FALLBACK_RESPONSE

    return str(content).strip()


if __name__ == "__main__":
    pergunta = input("PERGUNTA: ").strip()
    resposta = answer_question(pergunta)
    print(f"RESPOSTA: {resposta}")