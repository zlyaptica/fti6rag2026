import chromadb
import uuid

client = None
collection = None

def init(dir: str = "./chroma_db", collection_name:str = "my_collection"):
    global client, collection
    try:
        client = chromadb.Client(chromadb.config.Settings(
            persist_directory=dir,
            anonymized_telemetry=False
        ))

        try:
            collection = client.get_collection(collection_name)
        except:
            collection = client.create_collection(collection_name)

        print("init successfully")
    except:
        print("init fail")

def select_query(text: str) -> str:
    print("Ищу")
    results = collection.query(query_texts=[text])
    if not results['documents'][0]:
        print("Не нашёл.")
        return ""
    context = "\n\n".join(results['documents'][0])
    print("Что-то нашёл! Смотри: " + context)
    return context

def insert_query(text: str, metadata: dict = None):
        doc_id = str(uuid.uuid4())
        collection.add(
            documents=[text],
            metadatas=[metadata or {}],
            ids=[doc_id]
        )
        print(f"Документ добавлен с ID: {doc_id}")

def delete_query(text: str = None, doc_id: str = None):
        if doc_id:
            collection.delete(ids=[doc_id])
            print(f"Документ {doc_id} удален")
        elif text:           
            results = select_query(text, n_results=10)
            ids_to_delete = [r['id'] for r in results]
            if ids_to_delete:
                collection.delete(ids=ids_to_delete)
                print(f"Удалено {len(ids_to_delete)} документов")
            else:
                print("Документы не найдены")  
