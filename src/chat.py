from search import answer_question

def main():
    print("Faça sua pergunta:")
    print("Digite 'sair' para encerrar.\n")

    while True:
        pergunta = input("PERGUNTA: ").strip()

        if pergunta.lower() in {"sair", "exit", "quit"}:
            print("Encerrando chat.")
            break

        if not pergunta:
            print("RESPOSTA: Digite uma pergunta válida.\n")
            continue

        resposta = answer_question(pergunta)
        print(f"RESPOSTA: {resposta}\n")


if __name__ == "__main__":
    main()