import chromadb
from chromadb.utils import embedding_functions
import uuid

class ChromaDB:
    def __init__(self, dir: str = "./chroma_db", collection_name:str = "my_collection"):
        try:
            client = chromadb.PersistentClient(path=dir)

            self._collection = client.get_or_create_collection(
                name=collection_name,
            )
            print("init successfully")
        except Exception as e:
            print("init fail", e)

    def select_query(self, text: str) -> str:
        results = self._collection.query(query_texts=[text], n_results=1)
        if not results['documents'] or not results['documents'][0]:
            return ""

        return results['documents'][0][0]

    def insert_query(self, text: str, metadata: dict = None) -> None:
        doc_id = str(uuid.uuid4())
        self._collection.add(
            documents=[text],
            ids=[doc_id]
        )

    def get_facts(self) -> str:
        facts = self._collection.get()
        if not facts['documents']:
            return ""
        
        return "\n".join(facts['documents'])
    

chromadb_client = ChromaDB()