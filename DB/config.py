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
    #Поиск в БД
    print("Ищу")

def insert_query(text: str, metadata: dict = None):
        doc_id = str(uuid.uuid4())
        collection.add(
            documents=[text],
            metadatas=[metadata or {}],
            ids=[doc_id]
        )
        print(f"Документ добавлен с ID: {doc_id}")

def delete_query(text: str):
    #Удалить из бд
    print("Удаляю")