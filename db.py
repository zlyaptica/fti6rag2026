import chromadb
import uuid

client = None
collection = None

def init(dir: str = "./chroma_db", collection_name:str = "my_collection"):
    global client, collection
    try:
        client = chromadb.PersistentClient(path=dir)

        try:
            collection = client.get_collection(collection_name)
        except:
            collection = client.create_collection(collection_name)

        print("init successfully")
    except:
        print("init fail")

def select_query(text: str) -> str:
    results = collection.query(query_texts=[text])
    if not results['documents'][0]:
        return ""
    context = "\n\n".join(results['documents'][0])
    return context

def insert_query(text: str, metadata: dict = None):
        doc_id = str(uuid.uuid4())
        collection.add(
            documents=[text],
            metadatas=[metadata or {}],
            ids=[doc_id]
        )