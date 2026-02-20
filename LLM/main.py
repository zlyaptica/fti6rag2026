from llm import ask_llm

def main():
    # Нужна локально установленная модель
    text = input("Запрос в LLM: ")
    answer = ask_llm(text)
    print(answer)

if __name__ == '__main__':
    main()