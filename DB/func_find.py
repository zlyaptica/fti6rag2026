import chromadb
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
#from langchain_community.embeddings import HuggingFaceEmbeddings

# Конфигурация (должна совпадать с init_db.py, возможно стоит куда-то вынести, например как функцию в init_db.py)
MODEL_NAME = "intfloat/multilingual-e5-small"
COLLECTION_NAME = "company_knowledge"
PERSIST_DIRECTORY = "./chroma_db"

# Подключение к существующей БД
client = chromadb.PersistentClient(path=PERSIST_DIRECTORY)
collection = client.get_collection(COLLECTION_NAME)

# LangChain Retriever
langchain_ef = HuggingFaceEmbeddings(model_name=MODEL_NAME)
vectorstore = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=langchain_ef,
    persist_directory=PERSIST_DIRECTORY
)

def search(query, filters=None, top_k=5):
    search_kwargs = {"k": top_k}
    if filters:
        search_kwargs["filter"] = filters
    retriever = vectorstore.as_retriever(search_kwargs=search_kwargs)
    docs = retriever.invoke(query)
    return [(doc.page_content, doc.metadata) for doc in docs]

if __name__ == "__main__":
    test_queries = [
        "как взять отпуск",
        "проблемы с 1С",
        "скидка для клиента",
        "настройка отчёта в 1С",
        "политика конфиденциальности"
    ]
    
    for query in test_queries:
        print("\n" + "="*42)
        print(f"ЗАПРОС: '{query}'")
        print("="*42)
        results = search(query, top_k=3)
        for i, (doc, meta) in enumerate(results, 1):
            print(f"{i}. {doc[:150]}...")
            print(f"   Метаданные: {meta}")
        
        # Пример использования фильтра
        #if "отпуск" in query.lower():
        #    print("\n Фильтр: только HR отдел")
        #    filtered = search(query, filters={"department": "HR"}, top_k=2)
        #    for i, (doc, meta) in enumerate(filtered, 1):
        #        print(f"{i}. {doc[:150]}...")
        #        print(f"   Метаданные: {meta}")